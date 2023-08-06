import dice
import wordlist_loader


def find_index(wordlist: list[dict[str, str]], number: str) -> int:
    for index, element in enumerate(wordlist):
        if element.get("number") == number:
            return index

    return -1


def get_word(wordlist: list[dict[str, str]], index: int) -> str:
    tmp = wordlist[index]
    return tmp.get("word")


def passphrase_generation(number_of_words: int, wordlist_name: str):
    wordlist = wordlist_loader.load_lines_from_file(wordlist_name)
    passphrase = ""

    for i in range(number_of_words):
        number = dice.generate_string_of_numbers()
        index = find_index(wordlist, number)
        word = get_word(wordlist, index).capitalize()
        passphrase += word

    print(passphrase)
