# import our own 'python_basics' package
# import our own 'collections' package
import classes_oop
import collections_python
import csv_parsing
import functions_python
import python_basics
import string_object
from classes_oop.home_task import FILE_NAME, create_file


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


def execute_collections_home_task() -> None:
    # generate a list of random dicts due to 'generate_list_dicts' func and assign it to 'list_dicts" var
    list_dicts = collections_python.generate_list_dicts()
    # print 'list_dicts' var to a console
    print(list_dicts)
    # create a common dict with 'create_common_dict' func and assign the result to 'common_dict' var
    common_dict = collections_python.create_common_dict(list_dicts)
    # print 'common_dict' var to a console
    print(common_dict)


def execute_string_object_home_task() -> None:
    s = '''homEwork:

tHis iz your homeWork, copy these Text to variable.



You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''
    normalized_str = string_object.normalize_string(s)
    print(f'Normalized str:\n{normalized_str}\n')
    correct_str = string_object.replace_incorrect_value(normalized_str)
    print(f'Correct str:\n{correct_str}\n')
    special_sentence = string_object.get_special_sentence(correct_str)
    s_with_special_sentence = string_object.add_special_sentence(correct_str, special_sentence)
    print(f'Str with special sentence:\n{s_with_special_sentence}\n')
    count_whitespaces = string_object.count_whitespaces(correct_str)
    print(f'Count whitespaces:\n{count_whitespaces}')


def execute_functions_home_task() -> None:
    try:
        number = int(input('Input a number greater than or equal to 0: '))
        if number < 0:
            print('Number is less than 0')
            return None
    except ValueError:
        return None
    fibonacci_dict = functions_python.create_fibonacci_dict(number)

    sentence = input('Input any sentence: ')
    palindrome_count = functions_python.get_palindrome_count(sentence)
    uppercase_palindrome_sentence = functions_python.get_uppercase_palindrome_sentence(sentence)


def execute_classes_oop_home_task() -> None:
    news_feed_func = classes_oop.NEWS_FEEDS.get(
        input('Choose a data type\n1) News\n2) Private Ad\n3) Fake\nInput just a number: ')
    )
    if news_feed_func is None:
        print('There is no such news feed.')
        return None
    news_feed = news_feed_func()
    news_feed.write2file()
    execute_csv_parsing_home_task()


def execute_modules_home_task() -> None:
    text_file = create_file()
    text_file.write2file()
    text_file.remove_file()


def execute_csv_parsing_home_task() -> None:
    csv_parsing.create_word_count_csv(FILE_NAME)
    csv_parsing.create_detail_csv(FILE_NAME)


def execute_json_home_task() -> None:
    json_file = create_file()
    json_file.write2file()
    json_file.remove_file()


def execute_xml_home_task() -> None:
    xml_file = create_file()
    xml_file.write2file()
    xml_file.remove_file()


def execute_database_home_task() -> None:
    news_feed_func = classes_oop.NEWS_FEEDS.get(
        input('Choose a data type\n1) News\n2) Private Ad\n3) Fake\nInput just a number: ')
    )
    if news_feed_func is None:
        print('There is no such news feed.')
        return None
    news_feed = news_feed_func()
    news_feed.write2db()


def main() -> None:
    # execute_python_basics_home_task()
    # execute_collections_home_task()
    # execute_string_object_home_task()
    # execute_functions_home_task()
    # execute_classes_oop_home_task()
    # execute_modules_home_task()
    # execute_csv_parsing_home_task()
    # execute_json_home_task()
    # execute_xml_home_task()
    execute_database_home_task()


# execute 'main' func only if the main.py file is executed
if __name__ == '__main__':
    main()
