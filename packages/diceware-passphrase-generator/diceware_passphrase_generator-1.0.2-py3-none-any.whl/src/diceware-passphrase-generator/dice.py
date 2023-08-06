# IMPORTS
import random


def generate_numbers(number_of_numbers: int = 5) -> list[int]:
    num_arr = []
    i = 0
    while i < number_of_numbers:
        num = round(random.random() * 10)
        if num > 6 or num < 1:
            continue
        num_arr.append(num)
        i += 1
    return num_arr


def concat_all_numbers(num_array: list[int]) -> str:
    return ''.join(str(i) for i in num_array)


def generate_string_of_numbers(number_of_numbers: int = 5) -> str:
    return concat_all_numbers(generate_numbers(number_of_numbers))
