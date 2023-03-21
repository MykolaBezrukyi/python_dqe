import datetime
import json
import os
import re
import sqlite3
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
from xml.etree import ElementTree

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

    @abstractmethod
    def write2db(self) -> None:
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

    def write2db(self) -> None:
        news = news_feed_database.read_query('SELECT text, city, date FROM news')
        fields = (self.text, self.city, self.date.strftime('%d/%m/%Y %H:%M'))
        if fields in news:
            print('Such news already exists.')
        news_feed_database.execute_query(
            '''
            INSERT INTO news(text, city, date) VALUES (?, ?, ?)
            ''', *fields
        )


def create_news() -> News:
    text = input('Input news text: ')
    while is_empty_string(text):
        print('Text input is empty.')
        text = input('Input news text: ')
    city = input('Input city name: ')
    while is_empty_string(city):
        print('City input is empty.')
        city = input('Input city name: ')
    return News(
        text=text,
        city=city
    )


def is_empty_string(string: str) -> bool:
    return string == ''


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

    def write2db(self) -> None:
        news = news_feed_database.read_query('SELECT text, expiration_date FROM private_ads')
        fields = (self.text, self.expiration_date.strftime('%d/%m/%Y'))
        if fields in news:
            print('Such private ad already exists.')
            return None
        news_feed_database.execute_query(
            '''
            INSERT INTO private_ads(text, expiration_date) VALUES (?, ?)
            ''', *fields
        )


def create_private_ad() -> PrivateAd:
    text = input('Input private ad text: ')
    while is_empty_string(text):
        print('Text input is empty.')
        text = input('Input private ad text: ')
    expiration_date = input_expiration_date()
    while is_paste_date(expiration_date):
        print('Expiration date is paste date.')
        expiration_date = input_expiration_date()
    return PrivateAd(
        text=text,
        expiration_date=expiration_date
    )


def input_expiration_date() -> datetime.date:
    expiration_date = None
    while expiration_date is None:
        try:
            expiration_date = parse_date(input('Input expiration date: '))
        except ValueError:
            ...
    return expiration_date


def is_paste_date(date: datetime.date) -> bool:
    return date < datetime.datetime.now().date()


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

    def write2db(self) -> None:
        news = news_feed_database.read_query('SELECT text, severity FROM fakes')
        fields = (self.text, self.severity.value)
        if fields in news:
            print('Such fake already exists.')
            return None
        news_feed_database.execute_query(
            '''
            INSERT INTO fakes(text, severity) VALUES (?, ?)
            ''', *fields
        )


def create_fake() -> Fake:
    text = input('Input fake text: ')
    while is_empty_string(text):
        print('Text input is empty.')
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
                for news_feed in data.values()
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


class XMLNewsFeedParser(NewsFeedParser):
    def parse_news_feeds(self, file_path: str) -> list[NewsFeed]:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = ElementTree.parse(file_path)
            return [
                self._parse_news_feed(news_feed)
                for news_feed in data.getroot()
            ]

    def _parse_news_feed(self, news_feed: ElementTree.Element) -> NewsFeed:
        news_feed_type = NewsFeedType(news_feed.attrib.get('type'))
        if news_feed_type == NewsFeedType.NEWS:
            text, city = news_feed.find('text').text, news_feed.find('city').text
            news = News(
                text=text,
                city=city
            )
            news.date = datetime.datetime.strptime(news_feed.find('date').text, '%d/%m/%Y %H.%M')
            return news
        elif news_feed_type == NewsFeedType.PRIVATE_AD:
            text, expiration_date_str = news_feed.find('text').text, news_feed.find('expiration_date').text
            expiration_date = parse_date(expiration_date_str)
            return PrivateAd(
                text=text,
                expiration_date=expiration_date
            )
        elif news_feed_type == NewsFeedType.FAKE:
            text, severity = news_feed.find('text').text, Severity(news_feed.find('severity').text)
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


class NewsFeedDatabase:
    DATABASE_NAME: str = 'newsfeed.db'

    def __init__(self):
        self.con = sqlite3.connect(self.DATABASE_NAME)
        self.cur = self.con.cursor()

    def create_news_table(self) -> None:
        self.execute_query(
            '''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                text TEXT,
                city TEXT,
                date TEXT
            );
            '''
        )

    def create_private_ads_table(self) -> None:
        self.execute_query(
            '''
            CREATE TABLE IF NOT EXISTS private_ads (
                id INTEGER PRIMARY KEY,
                text TEXT,
                expiration_date TEXT
            );
            '''
        )

    def create_fakes_table(self) -> None:
        self.execute_query(
            '''
            CREATE TABLE IF NOT EXISTS fakes (
                id INTEGER PRIMARY KEY,
                text TEXT,
                severity TEXT
            );
            '''
        )

    def execute_query(self, query: str, *options) -> None:
        self.cur.execute(query, options)
        self.con.commit()

    def read_query(self, query: str, *options) -> list[tuple[Any, ...]]:
        self.cur.execute(query, options)
        result = self.cur.fetchall()
        self.con.commit()
        return result


FILE_PARSERS = {
    'txt': TextFileNewsFeedParser,
    'json': JSONFileNewsFeedParser,
    'xml': XMLNewsFeedParser,
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

news_feed_database = NewsFeedDatabase()
news_feed_database.create_news_table()
news_feed_database.create_private_ads_table()
news_feed_database.create_fakes_table()

# check the result
# print(news_feed_database.read_query('SELECT * FROM news'))
