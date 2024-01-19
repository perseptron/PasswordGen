
import argparse
import logging
import random
import re
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
    simple.add_argument('-n', help="Set length of password", type=int)
    simple.add_argument("-S", help="define character set, you can use placeholders \\d for digits, \\l for small "
                                   "literal, \\u for big literal, \\L for combination small and big letters and \\p "
                                   "for punctuation symbols", default="\\L\\d")

    parser.add_argument("-t", help="Set template for generate passwords", default="LLllddpp")
    parser.add_argument("-f", help="Getting list of patterns from file and generate for each random password")
    parser.add_argument("-c", help="number of passwords", type=int, default=1)
    parser.add_argument("-m", help="do not mix up (permutate) final result ", action="store_false")
    parser.add_argument("-v", help="set verbosity level", action="count", default=0)
    args = parser.parse_args()
    logging.basicConfig(level=VERBOSITY[args.v])
    logging.debug("argparse object = " + str(args))
    process_options(args)


def process_options(args):
    if args.n:
        random_based(args)
    if args.t:
        pattern_based(args)


def random_based(args):
    logging.debug("starting random-based charset generation")
    charset = ""
    password = []
    pos = 0
    while pos < len(args.S):
        if args.S[pos] == '\\':
            charset = charset + placeholder2charset(args.S[pos + 1])
            pos = pos + 2
            continue
        charset = charset + args.S[pos]
        pos = pos + 1

    charset = dedup(charset)
    for _ in range(args.n):
        password.append(generate_char(charset))
    print("".join(password))
    exit(0)


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


def pattern_based(args):
    logging.debug("starting pattern-based password generation")
    charset = None
    password = []
    pos = 0
    while pos < len(args.t):
        if args.t[pos] in "dluLp":
            charset = placeholder2charset(args.t[pos])
        if args.t[pos] == "\\":
            pos += 1
            charset = args.t[pos]
        if args.t[pos] == "[":
            start_pos = pos
            end_pos = args.t[pos:].find("]")
            pos = pos + end_pos
            charset = unbracketing(args.t[start_pos + 1:pos])
        if charset is None:
            logging.error("wrong template")
            break
        rep = find_repeat(args.t[pos + 1:])
        for _ in range(rep):
            password.append(generate_char(list(charset)))
        pos = pos + 1 if rep == 1 else pos + len(str(rep)) + 3
    print("".join(password))
    exit(0)


def unbracketing(bracket:str):
    pos = 0
    charset = ""
    while pos < len(bracket):
        if bracket[pos] in "dluLp":
            charset = charset + placeholder2charset(bracket[pos])
        if bracket[pos] == "\\":
            pos += 1
            charset = charset + bracket[pos]
        if bracket[pos] == "^":
            pos += 2
            charset = charset.replace(bracket[pos], "")
        pos += 1
    return charset


def find_repeat(st: str):
    match = re.search(r'^\{(\d+)\}', st)
    return int(match.group(1)) if match else 1


def dedup(chars: str):
    logging.debug("charset before deduplication = " + chars)
    chars = list(set(chars))
    logging.debug("charset after deduplication = " + "".join(sorted(chars)))
    return chars


def generate_char(charset: list):
    return charset[random.randrange(len(charset))]


def permutate(lst: list, args):
    if args.m:
        logging.debug("permutation")
        random.sample(lst, len(lst))
    return "".join(lst)


if __name__ == "__main__":
    main()
