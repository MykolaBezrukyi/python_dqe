import datetime
import json
import os
import re
from abc import ABC, abstractmethod
from enum import Enum

FILE_NAME = 'newsfeed.txt'


class Severity(Enum):
    CRITICAL = 'critical'
    MAJOR = 'major'
    MODERATE = 'moderate'
    MINOR = 'minor'


class NewsFeedType(Enum):
    NEWS = 'news'
    PRIVATE_AD = 'private ad'
    FAKE = 'fake'


class NewsFeed(ABC):
    @abstractmethod
    def write2file(self) -> None:
        raise NotImplementedError


class News(NewsFeed):
    def __init__(self, text: str, city: str):
        self.text = text
        self.city = city
        self.date = datetime.datetime.today()

    def write2file(self) -> None:
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            file.write('News -------------------------\n')
            file.write(
                f'{self.text}\n{self.city}, '
                f'{self.date.strftime("%d/%m/%Y %H.%M")}\n'
            )
            file.write('------------------------------\n\n')


def create_news() -> News:
    text = input('Input news text: ')
    city = input('Input city name: ')
    return News(
        text=text,
        city=city
    )


class PrivateAd(NewsFeed):
    def __init__(self, text: str, expiration_date: datetime.date):
        self.text = text
        self.expiration_date = expiration_date

    @property
    def day_left(self) -> int:
        return (self.expiration_date - datetime.date.today()).days

    def write2file(self) -> None:
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            file.write('Private Ad ------------------\n')
            file.write(
                f'{self.text}\nActual until: '
                f'{self.expiration_date.strftime("%d/%m/%Y")}, '
                f'{self.day_left} days left\n'
            )
            file.write('------------------------------\n\n')


def create_private_ad() -> PrivateAd:
    text = input('Input private ad text: ')
    expiration_date = None
    while expiration_date is None:
        try:
            expiration_date = parse_date(input('Input expiration date: '))
        except ValueError as e:
            print(e)
            continue
    return PrivateAd(
        text=text,
        expiration_date=expiration_date
    )


def parse_date(date_str: str) -> datetime.date:
    return datetime.datetime.strptime(date_str, '%d/%m/%Y').date()


class Fake(NewsFeed):
    def __init__(self, text: str, severity: Severity):
        self.text = text
        self.severity = severity

    def write2file(self) -> None:
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            file.write('Fake -------------------------\n')
            file.write(f'{self.text}\nSeverity: {self.severity.value}\n')
            file.write('------------------------------\n\n')


def create_fake() -> Fake:
    text = input('Input fake text: ')
    severity_str = None
    while severity_str not in [s.value for s in Severity]:
        severity_str = input('Input a severity (critical, major, moderate, minor): ').lower()
    severity = Severity(severity_str)
    return Fake(
        text=text,
        severity=severity
    )


class NewsFeedParser(ABC):
    @abstractmethod
    def parse_news_feeds(self, file_path: str) -> list[NewsFeed]:
        raise NotImplementedError


class TextFileNewsFeedParser(NewsFeedParser):
    def parse_news_feeds(self, file_path: str) -> list[NewsFeed]:
        with open(file_path, 'r', encoding='utf-8') as file:
            news_feeds = file.read().strip().split('\n\n')
            return [
                self._parse_news_feed(news_feed.strip())
                for news_feed in news_feeds
            ]

    def _parse_news_feed(self, news_feed: str) -> NewsFeed:
        news_feed_strings = news_feed.split('\n')
        news_feed_type = NewsFeedType(' '.join(re.findall(r'\w+[^ ]', news_feed_strings[0])).lower())
        news_feed_pattern = NEWS_FEED_PATTERNS.get(news_feed_type)
        news_feed_fields = '\n'.join(news_feed_strings[1:-1])
        news_feed_data = re.findall(news_feed_pattern, news_feed_fields)[0]
        if news_feed_type == NewsFeedType.NEWS:
            text, city = news_feed_data[0], news_feed_data[1]
            news = News(
                text=text,
                city=city
            )
            news.date = datetime.datetime.strptime(news_feed_data[2], '%d/%m/%Y %H.%M')
            return news
        elif news_feed_type == NewsFeedType.PRIVATE_AD:
            text, expiration_date_str = news_feed_data
            expiration_date = parse_date(expiration_date_str)
            return PrivateAd(
                text=text,
                expiration_date=expiration_date
            )
        elif news_feed_type == NewsFeedType.FAKE:
            text, severity_str = news_feed_data
            return Fake(
                text=text,
                severity=Severity(severity_str)
            )


class JSONFileNewsFeedParser(NewsFeedParser):
    def parse_news_feeds(self, file_path: str) -> list[NewsFeed]:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [
                self._parse_news_feed(news_feed)
                for news_feed in data
            ]

    def _parse_news_feed(self, news_feed: dict[str, str]) -> NewsFeed:
        news_feed_type = NewsFeedType(news_feed.get('type'))
        if news_feed_type == NewsFeedType.NEWS:
            text, city = news_feed.get('text'), news_feed.get('city')
            news = News(
                text=text,
                city=city
            )
            news.date = datetime.datetime.strptime(news_feed.get('date'), '%d/%m/%Y %H.%M')
            return news
        elif news_feed_type == NewsFeedType.PRIVATE_AD:
            text, expiration_date_str = news_feed.get('text'), news_feed.get('expiration_date')
            expiration_date = parse_date(expiration_date_str)
            return PrivateAd(
                text=text,
                expiration_date=expiration_date
            )
        elif news_feed_type == NewsFeedType.FAKE:
            text, severity = news_feed.get('text'), Severity(news_feed.get('severity'))
            return Fake(
                text=text,
                severity=severity
            )


class File:
    def __init__(self, file_path: str, news_feed_parser: NewsFeedParser):
        self.file_path = file_path
        self.news_feeds = news_feed_parser.parse_news_feeds(file_path)

    def write2file(self) -> None:
        for news_feed in self.news_feeds:
            news_feed.write2file()

    def remove_file(self) -> None:
        os.remove(self.file_path)


def create_file() -> File:
    file_path = input('Input a path to file: ')
    file_extension = file_path.split('.')[-1]
    return File(
        file_path=file_path,
        news_feed_parser=FILE_PARSERS[file_extension]()
    )


FILE_PARSERS = {
    'txt': TextFileNewsFeedParser,
    'json': JSONFileNewsFeedParser,
}

NEWS_FEEDS = {
    '1': create_news,
    '2': create_private_ad,
    '3': create_fake,
}

NEWS_FEED_PATTERNS = {
    NewsFeedType.NEWS: r'(.*?)\n(.*?), (.*?)$',
    NewsFeedType.PRIVATE_AD: r'(.*?)\nActual until: (.*?),',
    NewsFeedType.FAKE: r'(.*?)\nSeverity: (.*?)$',
}
