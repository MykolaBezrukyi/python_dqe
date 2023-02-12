import datetime
from abc import ABC, abstractmethod
from enum import Enum

FILE_NAME = 'newsfeed.txt'


class Severity(Enum):
    CRITICAL = 'critical'
    MAJOR = 'major'
    MODERATE = 'moderate'
    MINOR = 'minor'


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


def parse_date(date_str: str) -> datetime.date:
    return datetime.datetime.strptime(date_str, '%d/%m/%Y').date()


NEWS_FEEDS = {
    '1': create_news,
    '2': create_private_ad,
    '3': create_fake,
}
