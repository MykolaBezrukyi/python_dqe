PARAGRAPH_NUMBER = 3


def normalize_string(s: str) -> str:
    l = s.split('\n')
    for i, sentence in enumerate(l):
        sentence_l = sentence.split('. ')
        l[i] = '. '.join(list(map(str.capitalize, sentence_l)))
    return '\n'.join(l)


def add_special_sentence(s: str, special_sentence: str) -> str:
    l = s.split('\n')
    whitespaces_count = 0
    for i, sentence in enumerate(l):
        if sentence in ('', ' '):
            whitespaces_count += 1
        if is_paragraph_number(i, whitespaces_count):
            l[i] = l[i] + ' ' + special_sentence
            break
    return '\n'.join(l)


def is_paragraph_number(i: int, whitespaces_count: int) -> bool:
    return i - whitespaces_count + 1 == PARAGRAPH_NUMBER


def get_special_sentence(s: str) -> str:
    return (' '.join(
        [
            sentence.split(' ')[-1]
            for sentence in s.split('.')
        ]
    ).strip() + '.').capitalize()


def replace_incorrect_value(s: str) -> str:
    return s.replace(' iz ', ' is ')


def count_whitespaces(s: str) -> int:
    return s.count(' ') + s.count('\n')
