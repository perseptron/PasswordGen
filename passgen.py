# CLI interface can support next commands:
# -vvv: Verbose mode (-v |-vv |-vvv )
# -h: help
# -S: character set
import argparse
import random
import string


def process_options(args):
    if args.n:
        random_based(args)


def main():
    """ Password Generator"""
    parser = argparse.ArgumentParser()
    # parser.add_argument('-n', help="Set length of password and generate random password from set {small lateral "
    #                                "ASCII, big lateral ASCII, digit}", type=int, default=8)
    parser.add_argument('/d', action='store_true', help="Use digits 0..9")
    parser.add_argument('/l', action='store_true', help="Use lowercase letters a..z")
    parser.add_argument('/u', action='store_true', help="Use uppercase letters A..Z")
    parser.add_argument('/L', action='store_true', help="Use mixed-case letters a..Z")
    parser.add_argument('/p', action='store_true', help="Use punctuation characters - ,.;:")

    # parser.add_argument("-t", help="Set template for generate passwords", default="LLllddpp")
    # parser.add_argument("-f", help="Getting list of patterns from file and generate for each random password")
    # parser.add_argument("-c", help="number of passwords", type=int, default=1)
    # parser.add_argument('-h', help="here goes instruction how to use it")
    args = parser.parse_args()

    process_options(args)


def random_based(args):
    charset = ""
    if args.d:
        charset = charset + string.digits
    if args.l:
        charset = charset + string.ascii_lowercase
    if args.u:
        charset = charset + string.ascii_uppercase
    if args.L:
        charset = charset + string.ascii_letters
    if args.p:
        charset = charset + ",.;:"

    charset = dedup(charset)
    char_source = []

    for i in range(args.n):
        char_source.append(charset)
    print(generate(char_source))


def dedup(chars: str):

    return list(set(chars))


def generate(chr_set_list: list):
    password_lst = []
    for character in chr_set_list:
        password_lst.append(character[random.randrange(len(character) - 1)])
    return "".join(permutate(password_lst))


def permutate(lst: list):
    return random.sample(lst, len(lst))


if __name__ == "__main__":
    main()
