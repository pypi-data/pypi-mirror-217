# Diceware Passphrase Generator

This is a command-line tool for generating secure passphrases based on the diceware method. The diceware method uses a list of words and random dice rolls to create strong and memorable passwords.

## Prerequisites

To use this tool, you need to have Python 3 installed on your system.

## Installation

1. Download the code from the [release page](https://github.com/SoSaymon/diceware-passphrase-generator/releases/)
2. Unzip the code

## Usage

Run the `diceware.py` script with the desired options to generate a passphrase.
```bash
python diceware.py [-h] [-w NUMBER OF WORDS] [--wordlist=wordlist.txt]
```
### Options

- `-h, --help`: Show the help message and exit.
- `-w NUMBER OF WORDS, --words=NUMBER OF WORDS`: Specify the number of words in the passphrase.
- `--wordlist=wordlist.txt`: Specify the wordlist file to use for generating the passphrase. If not provided, the default wordlist (`wordlist.txt`) will be used.

If you don't specify the options when running the script, an interactive prompt will ask you for the number of words and the wordlist.

## Wordlist

The tool uses a wordlist file containing a set of words. If you want to use a custom wordlist, make sure it is a text file where each word is on a separate line. The default wordlist (`wordlist.txt`) is used if no custom wordlist is specified.

## Example

Here's an example of how to use the tool:

```bash
python diceware.py -w 6
```
This command will generate a passphrase consisting of 6 random words from the default wordlist.

## Disclaimer

Please note that the security of your generated passphrase depends on the quality and randomness of the wordlist used. Use a trusted wordlist and ensure that it has enough entropy to provide adequate security.
## Contribution

Contributions to the Diceware Passphrase Generator are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

Please ensure that your code follows the existing style and conventions used in the project. Also, remember to write tests for any new functionality you add.

## Contact

If you have any questions or suggestions regarding the BMI Calculator, please feel free to reach out:

- Author: SoSaymon
- Email: [szymon.chirowski@protonmail.com](mailto:szymon.chirowski@protonmail.com)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
