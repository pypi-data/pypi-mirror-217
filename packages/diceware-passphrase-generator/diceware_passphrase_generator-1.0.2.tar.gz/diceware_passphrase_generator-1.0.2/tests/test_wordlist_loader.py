import sys
import pytest
from wordlist_loader import make_dict, load_lines_from_file, make_wordlist


sys.path.append("/home/sosaymon/Projects/diceware-password-generator/")


def test_make_dict():
    assert make_dict("1   one\n") == {"number": "1", "word": "one"}


def test_make_wordlist():
    assert make_wordlist(['1   one\n', '2   two\n', '3   three']) == [
        {"number": "1", "word": "one"},
        {"number": "2", "word": "two"},
        {"number": "3", "word": "three"}
    ]


def test_load_lines_from():
    assert load_lines_from_file("tests/test_wordlist.txt") == [
        {"number": "1", "word": "one"},
        {"number": "2", "word": "two"},
        {"number": "3", "word": "three"}
    ]


def test_wordlist_maker_exceptions():
    with pytest.raises(SystemExit):
        load_lines_from_file("tests/nonexistent_file.txt")
