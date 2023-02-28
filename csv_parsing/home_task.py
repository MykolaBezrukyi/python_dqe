import re
from typing import Any

WORD_COUNT_CSV_FILE_NAME = 'word_count.csv'
DETAIL_CSV_FILE_NAME = 'detail.csv'


def create_word_count_csv(file_path: str) -> None:
    file_data = get_file_data(file_path).lower()
    word_count_dict = create_word_count_dict(file_data)

    with open(WORD_COUNT_CSV_FILE_NAME, 'w', encoding='utf-8') as file:
        for k, v in word_count_dict.items():
            file.write(f'{k},{v}\n')


def get_file_data(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def create_word_count_dict(data: str) -> dict[str, int]:
    words = re.findall(r'[^\d\W]+', data)
    return {
        word: data.count(word)
        for word in words
    }


def create_detail_csv(file_path: str) -> None:
    file_data = get_file_data(file_path)
    detail_dict = create_detail_dict(file_data)

    with open(DETAIL_CSV_FILE_NAME, 'w', encoding='utf-8') as file:
        file.write('letter,count_all,count_uppercase,percentage\n')
        for k, v in detail_dict.items():
            file.write(f'{k},{v["count_all"]},{v["count_upper"]},{v["percentage"]:.2f}\n')


def create_detail_dict(data: str) -> dict[str, dict[str, Any]]:
    letters = re.findall(r'[^\d\W]', data)
    data_lower = data.lower()
    detail_dict = {}
    for letter in letters:
        letter_lower = letter.lower()
        if letter_lower in detail_dict:
            continue
        letter_count = data_lower.count(letter_lower)
        detail_dict[letter_lower] = {
            'count_all': letter_count,
            'count_upper': data.count(letter.upper()),
            'percentage': (letter_count * 100) / len(letters),
        }
    return detail_dict
