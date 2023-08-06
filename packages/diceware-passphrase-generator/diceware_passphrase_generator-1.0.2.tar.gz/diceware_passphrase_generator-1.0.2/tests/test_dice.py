import sys
import pytest

sys.path.append("/home/sosaymon/Projects/diceware-password-generator/")

from dice import generate_numbers, concat_all_numbers, generate_string_of_numbers

expected_values_test_generate_numbers = [5, 0, 0]
test_inputs = [5, 0, -1]


@pytest.mark.parametrize("test_input,expected", zip(test_inputs, expected_values_test_generate_numbers))
def test_generate_numbers(test_input: int, expected: int):
    assert len(generate_numbers(test_input)) == expected
    assert all([i in range(1, 7) for i in generate_numbers(test_input)])


def test_concat_all_numbers():
    result = concat_all_numbers([1, 2, 3, 4, 5])
    assert result == '12345'


def test_generate_string_of_numbers():
    result = generate_string_of_numbers(5)
    assert len(result) == 5
    for char in result:
        assert "1" <= char <= "6"
