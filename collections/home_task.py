# import 'random' python library
import random

# define global constant (string) contains all letters of english alphabet
LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def generate_list_dicts() -> list[dict[str, int]]:
    # generate a list with a random number of dicts (from 2 to 10) with a random number of key-values (from 2 to 3)
    # that are represented by random letter from 'LETTERS' global constant due to 'random.choice' func like a key
    # and random integer due to 'random.randint' func (from 0 to 100)
    return [
        {
            random.choice(LETTERS): random.randint(0, 100)
            for _ in range(random.randint(2, 3))
        }
        for _ in range(random.randint(2, 10))
    ]


def create_common_dict(l: list[dict[str, int]]) -> dict[str, int]:
    # define local 'common_dict' dict var
    common_dict = {}
    # for each index and dict in random number of dicts
    for i, d in enumerate(l):
        # for each key and value in 'd' var
        for k, v in d.items():
            # if 'is_written' func's result is true
            if is_written(k, common_dict):
                # return to nested for-loop
                continue
            # assign the result of 'get_key_list' func to 'key_list' var
            key_list = get_key_list(k, l)
            # get max index and max value of 'k' in 'l' var by unpacking the last of tuple of 'key_list' var
            max_idx, max_value = key_list[-1]
            # if 'is_repeatable' func's result is true
            if is_repeatable(key_list):
                # create a new key-value in 'common_dict' var (key = 'k' letter + max idx, value = max_value)
                common_dict[f'{k}_{max_idx + 1}'] = max_value
            else:
                # create new key-value in 'common_dict' var (key = 'k' letter, value = max_value)
                common_dict[k] = max_value
    # returns a 'common_dict' var
    return common_dict


def is_written(k: str, d: dict[str, int]) -> bool:
    # returns true if any of keys in 'd' var contains 'k' var substring else false
    return any(
        k in key
        for key in d.keys()
    )


def get_key_list(key: str, l: list[dict[str, int]]) -> list[tuple[int, int]]:
    # returns a sorted list of tuples [index of 'k' var, value of 'k' var] by value of 'k' var
    return sorted([
        (i, v)
        for i, d in enumerate(l)
        for k, v in d.items()
        if k == key
    ], key=lambda t: t[1])


def is_repeatable(l: list[tuple[int, int]]) -> bool:
    # returns true if the length of l greater than 1 else false
    return len(l) > 1
