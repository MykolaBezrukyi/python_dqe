from typing import Callable, Any


def welcome_func(foo: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        foo_res = foo(*args, **kwargs)
        foo_name = foo.__name__
        print(f'Starting {foo_name}')
        print(foo_res)
        print(f'Function {foo_name} is completed\n')
        return foo_res

    return wrapper


@welcome_func
def create_fibonacci_dict(n: int) -> dict[int, int]:
    if n == 0:
        return {0: 0}
    fibonacci_list = [0, 1, ]
    for i in range(1, n):
        fibonacci_list.append(fibonacci_list[i - 1] + fibonacci_list[i])
    return {
        i: fibonacci_list[i]
        for i in range(n)
    }


@welcome_func
def get_palindrome_count(s: str) -> int:
    palindrome_count = 0
    for w in s.split():
        if is_palindrome(w):
            palindrome_count += 1
    return palindrome_count


def is_palindrome(w: str) -> bool:
    w_low = w.lower()
    return w_low == w_low[::-1]


@welcome_func
def get_uppercase_palindrome_sentence(s: str) -> str:
    s_list = s.split()
    for i, w in enumerate(s_list):
        if is_palindrome(w):
            s_list[i] = w.upper()
    return ' '.join(s_list)
