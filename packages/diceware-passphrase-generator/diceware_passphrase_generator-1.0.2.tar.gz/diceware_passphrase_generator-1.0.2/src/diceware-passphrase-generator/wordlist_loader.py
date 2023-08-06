def make_dict(line: str) -> dict[str, str]:
    t = line.split()
    word_dict = {
        "number": t[0],
        "word": t[1]
    }
    return word_dict


def make_wordlist(wordlist: list[str]) -> list[dict[str, str]]:
    dict_list = []
    for i in range(len(wordlist)):
        dict_list.append(make_dict(wordlist[i]))
    return dict_list


def load_lines_from_file(filename: str) -> list[dict[str, str]]:
    try:
        with open(filename, "r") as f:
            wordlist = f.readlines()
    except FileNotFoundError:
        use_default = input("File not found. Use default wordlist? (y/n) ")
        if use_default.lower() == "y":
            with open("wordlist.txt", "r") as f:
                wordlist = f.readlines()
        else:
            exit(1)
    return make_wordlist(wordlist)
