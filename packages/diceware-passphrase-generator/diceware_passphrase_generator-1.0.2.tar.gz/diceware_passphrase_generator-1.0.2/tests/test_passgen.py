import sys

import pytest

sys.path.append("/home/sosaymon/Projects/diceware-password-generator/")

from passgen import find_index, get_word

test_inputs = ["1", "2", "3", "4"]
expected_values_test_find_index = [0, 1, 2, -1]


@pytest.mark.parametrize("test_input,expected", zip(test_inputs, expected_values_test_find_index))
def test_find_index(test_input: str, expected: int):
    wordlist = [
        {"number": "1", "word": "a"},
        {"number": "2", "word": "b"},
        {"number": "3", "word": "c"},
    ]
    assert find_index(wordlist, test_input) == expected


def test_get_word():
    assert get_word([{"word": "a"}], 0) == "a"
