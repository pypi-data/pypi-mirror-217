import passgen
import argparse

PassphraseWordLength = int
AvailableWords = str


def get_user_options() -> (PassphraseWordLength, AvailableWords):
    print("Welcome in diceware generation program")
    number_of_words = int(input("How many words should the passphrase contain?\n"))
    wordlist = input("What wordlist do you want to use? Leave blank if you want to use the default one.")

    return number_of_words, wordlist


def main():
    parser = argparse.ArgumentParser(prog="diceware.py",
                                     usage="python3 %(prog)s [-h] [-w NUMBER OF WORDS] [--wordlist=wordlist.txt]",
                                     description="Passphrase generator based on diceware method")
    parser.add_argument("-w", "--words", type=int, help="Number of words in passphrase")
    parser.add_argument("--wordlist", type=str, default="wordlist.txt", help="Wordlist used to generate the passphrase")

    args = parser.parse_args()
    number_of_words = args.words
    wordlist = args.wordlist

    if number_of_words is None:
        number_of_words, wordlist = get_user_options()
        if wordlist == "":
            wordlist = "wordlist.txt"

    passgen.passphrase_generation(number_of_words, wordlist)


if __name__ == '__main__':
    main()
