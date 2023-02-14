import re

PARAGRAPH_NUMBER = 3


def normalize_string(s: str) -> str:
    lst = s.split('\n')
    for i, sentence in enumerate(lst):
        sentence_lst = sentence.split('. ')
        lst[i] = '. '.join(list(map(str.capitalize, sentence_lst)))
    return '\n'.join(lst)


def add_special_sentence(s: str, special_sentence: str) -> str:
    lst = s.split('\n')
    whitespaces_count = 0
    for i, sentence in enumerate(lst):
        if sentence in ('', ' '):
            whitespaces_count += 1
        if is_paragraph_number(i, whitespaces_count):
            lst[i] = lst[i] + ' ' + special_sentence
            break
    return '\n'.join(lst)


def is_paragraph_number(i: int, whitespaces_count: int) -> bool:
    return i - whitespaces_count + 1 == PARAGRAPH_NUMBER


def get_special_sentence(s: str) -> str:
    return ' '.join(re.findall(r'\s(\w+)\.', s)).capitalize() + '.'


def replace_incorrect_value(s: str) -> str:
    return s.replace(' iz ', ' is ')


def count_whitespaces(s: str) -> int:
    return s.count(' ') + s.count('\n')
