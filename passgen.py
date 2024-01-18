# -S: character set
import argparse
import logging
import random
import string

VERBOSITY = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)


def main():
    """ Password Generator"""

    parser = argparse.ArgumentParser(prog="passgen",
                                     description="Utility for generating passwords according to a given template that "
                                                 "supports the CLI interface",
                                     epilog="Thanks for using %(prog)s! :)", )
    simple = parser.add_argument_group("simple method generate random password from set {small literal "
                                       "ASCII, big literal ASCII, digit}")
    simple.add_argument('-n', help="Set length of password", type=int, default=8)
    simple.add_argument("-S", help="define character set, you can use placeholders \\d for digits, \\l for small "
                                   "literal, \\u for big literal, \\L for combination small and big letters and \\p "
                                   "for punctuation symbols", default="\\L\\d")

    parser.add_argument("-t", help="Set template for generate passwords", default="LLllddpp")
    parser.add_argument("-f", help="Getting list of patterns from file and generate for each random password")
    parser.add_argument("-c", help="number of passwords", type=int, default=1)
    parser.add_argument("-v", help="set verbosity level", action="count", default=0)
    args = parser.parse_args()
    logging.basicConfig(level=VERBOSITY[args.v])
    logging.debug("argparse object = " + str(args))
    process_options(args)


def process_options(args):
    if args.n:
        random_based(args)


def random_based(args):
    logging.debug("starting random-based charset generation")
    charset = ""
    pos = 0
    while pos < len(args.S):
        if args.S[pos] == '\\':
            charset = charset + placeholder2charset(args.S[pos+1])
            pos = pos + 2
            continue
        charset = charset + args.S[pos]
        pos = pos + 1

    charset = dedup(charset)
    char_source = []

    for i in range(args.n):
        char_source.append(charset)
    print(generate(char_source))


def placeholder2charset(ph: str):
    if "d" in ph:
        return string.digits
    if "l" in ph:
        return string.ascii_lowercase
    if "u" in ph:
        return string.ascii_uppercase
    if "L" in ph:
        return string.ascii_letters
    if "p" in ph:
        return ",.;:"


def dedup(chars: str):
    logging.debug("charset before deduplication = " + chars)
    chars = list(set(chars))
    logging.debug("charset after deduplication = " + "".join(sorted(chars)))
    return chars


def generate(chr_set_list: list):
    password_lst = []
    for character in chr_set_list:
        password_lst.append(character[random.randrange(len(character))])
    return "".join(permutate(password_lst))


def permutate(lst: list):
    logging.debug("permutation")
    return random.sample(lst, len(lst))


if __name__ == "__main__":
    main()
