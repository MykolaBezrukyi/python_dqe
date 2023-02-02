# import 'random' python package
import random

# define global constant describes the length of random list
RANDOM_LIST_LENGTH: int = 100


def generate_random_list() -> list[int]:
    # generate the list of random numbers with 'RANDOM_LIST_LENGTH'
    # using 'randint' func from 'random' package with arguments
    # 0 (min random number) and 1000 (max random number)
    return [
        random.randint(0, 1000)
        for _ in range(RANDOM_LIST_LENGTH)
    ]


def sort_list(l: list[int]) -> None:
    # get the index and corresponding value of 'l' var using 'enumerate' built-in func
    for ind_i, i in enumerate(l):
        # get the index and corresponding value of 'l' var using 'enumerate' built-in func
        for ind_j, j in enumerate(l):
            # check if the index of external cycle is greater than index of nested one
            if ind_i >= ind_j:
                # back to the start of nested cycle
                continue
            # check if the value of nested cycle is less than external one
            if l[ind_j] < l[ind_i]:
                # swap values
                l[ind_i], l[ind_j] = l[ind_j], l[ind_i]


def get_avg_even(l: list[int]) -> float:
    # generate the list contains even numbers by checking remainder from division by 2 is equal to zero
    even_numbers = [
        i
        for i in l
        if i % 2 == 0
    ]
    # return the result of division of sum all numbers in 'even_numbers' list and its length
    return sum(even_numbers) / len(even_numbers)


def get_avg_odd(l: list[int]) -> float:
    # generate the list contains odd numbers by checking remainder from division by 2 is not equal to zero
    odd_numbers = [
        i
        for i in l
        if i % 2 != 0
    ]
    # return the result of division of sum all numbers in 'odd_numbers' list and its length
    return sum(odd_numbers) / len(odd_numbers)
