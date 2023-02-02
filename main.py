# import our own 'python_basics' package
import python_basics


def execute_python_basics_home_task() -> None:
    # assign the result of 'generate_random_list' func to 'random_list' var
    random_list = python_basics.generate_random_list()
    print(f'Initial list:\n{random_list}\n')
    # call 'sort_list' func for random_list var
    python_basics.sort_list(random_list)
    print(f'Sorted list:\n{random_list}\n')
    # print to console 'get_avg_even' func's result
    print(f'{python_basics.get_avg_even(random_list):.2f}')
    # print to console 'get_avg_odd' func's result
    print(f'{python_basics.get_avg_odd(random_list):.2f}')


def main() -> None:
    execute_python_basics_home_task()


# execute 'main' func only if the main.py file is executed
if __name__ == '__main__':
    main()
