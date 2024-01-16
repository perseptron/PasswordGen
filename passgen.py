# CLI interface can support next commands:
# -vvv: Verbose mode (-v |-vv |-vvv )
# -h: help
# -S: character set

import argparse
import random

import time


def parse(args):
    n = int(args.n)
    print(generate([[1, 2, 3, 4, 5], ['a', 'b', 'c', 'd', 'e'], ['$', '%', '@', '&', '#']]))


def main():
    """ Password Generator"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="Set length of password and generate random password from set {small lateral "
                                   "ASCII, big lateral ASCII, digit}", default=8)
    parser.add_argument("-t", help="Set template for generate passwords", default="LLllddpp")
    parser.add_argument("-f", help="Getting list of patterns from file and generate for each random password")
    parser.add_argument("-c", help="number of passwords", type=int, default=1)
    # parser.add_argument("-h", help="here goes instruction how to use it")
    args = parser.parse_args()

    parse(args)


def generate(chr_set_list: list):
    password_lst = []
    for character in chr_set_list:
        password_lst.append(character[random.randrange(len(character) - 1)])
    return password_lst


def permutate(lst: list):
    return random.sample(lst, len(lst))


if __name__ == "__main__":
    main()
