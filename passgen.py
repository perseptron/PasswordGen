import argparse
import logging
import re
import utils

VERBOSITY = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)


def main():
    """ Password Generator"""

    parser = argparse.ArgumentParser(prog="passgen",
                                     description="Utility for generating passwords according to a given template that "
                                                 "supports the CLI interface",
                                     epilog="Thanks for using %(prog)s! :)", )
    simple = parser.add_argument_group("simple method generate random password from set {small literal "
                                       "ASCII, big literal ASCII, digit}")
    simple.add_argument('-n', help="Set length of the password", type=int)
    simple.add_argument("-S", help="Define character set, you can use placeholders \\d for digits, \\l for small "
                                   "literal, \\u for big literal, \\L for combination small and big letters and \\p "
                                   "for punctuation symbols", default="\\L\\d")

    parser.add_argument("-t", help="Set template for passwords")
    parser.add_argument("-f", help="Getting list of patterns from file and generate for each random password")
    parser.add_argument("-c", help="Number of passwords to generate", type=int, default=1)
    parser.add_argument("-m", help="Do not mix up (permutate) final result ", action="store_true")
    parser.add_argument("-v", help="Set verbosity level", action="count", default=0)
    args = parser.parse_args()
    logging.basicConfig(level=VERBOSITY[args.v])
    logging.debug("argparse object = " + str(args))
    process_options(args)


def process_options(args):
    if args.n:
        random_based(args)
    if args.t:
        pattern_based(args)
    if args.f:
        file_based(args)
    exit(0)


def random_based(args):
    """ This method generate passwords using predefined charsets with the help of placeholders,
    use -n <length of the password> -S <template>
    <template> can be something like ABC\\d"""
    logging.debug("starting random-based charset generation")
    for _ in range(args.c):
        charset = ""
        password = []
        pos = 0
        while pos < len(args.S):
            if args.S[pos] == '\\':  # for example '\d'
                charset = charset + utils.placeholder2charset(args.S[pos + 1])
                pos = pos + 2  # moving 2 position because extra char "\"
                continue
            charset = charset + args.S[pos]
            pos = pos + 1

        charset = utils.dedup(charset)
        for _ in range(args.n):
            password.append(utils.generate_char(charset))
        print(utils.permutate(password, args))


def pattern_based(args):
    """ This method generate passwords using patterns. Pattern can include a character as is,
    or placeholder from method placeholder2charset(char), and also additional structures as {num} -
    it indicates how many times to use previous charset, or [<template>] - we could define a complex charset here.
    For example, this pattern 'u{4}[dl]{3}-l{2}' should give us something like DHRF3s4-st | FHGFds4-vt | DERS774-sd """
    logging.debug("starting pattern-based password generation")
    for _ in range(args.c):
        charset = None
        password = []
        pos = 0
        while pos < len(args.t):
            if args.t[pos] in "dluLpaAUhHvVZcCzbspx":  # character must insist in existing placeholder
                charset = utils.placeholder2charset(args.t[pos])
            if args.t[pos] == "\\":  # char starting with \ will be included in password as is
                pos += 1
                charset = args.t[pos]
            if args.t[pos] == "[":  # everything inside "[ ]" need to be "unpacked"
                start_pos = pos
                try:
                    end_pos = args.t[pos:].index("]")
                except ValueError:
                    logging.error("custom charset lacks a closing bracket ']'")
                    exit(1)
                pos = pos + end_pos
                charset = unbracketing(args.t[start_pos + 1:pos])
            if charset is None:
                logging.error("wrong template")
                break
            if pos + 1 < len(args.t) and args.t[pos + 1] == "{":  # {num} repeat previous charset <num> times
                rep = find_repeat(args.t[pos + 1:])
                pos = pos + len(str(rep)) + 3  # moving 3 position because of '{' and '}'
            else:
                rep = 1
                pos += 1
            for _ in range(rep):
                password.append(utils.generate_char(list(utils.dedup(charset))))

        print(utils.permutate(password, args))


def file_based(args):
    """This method generate passwords using list of patterns from the file. Rules for patterns are the same as in
    pattern-based method"""
    filename = args.f
    try:
        with open(filename, "r") as file:
            while line := file.readline():
                logging.debug("file pattern = {}".format(line.rstrip()))
                args.t = line.rstrip()
                pattern_based(args)
    except FileNotFoundError as error:
        logging.error("Can't proceed with file-based mode {}".format(error))
        exit(1)


def unbracketing(bracket: str):
    logging.debug("unbracketing complex charset [{}]".format(bracket))
    pos = 0
    charset = ""
    while pos < len(bracket):
        if bracket[pos] in "dluLpaAUhHvVZcCzbspx":
            charset = charset + utils.placeholder2charset(bracket[pos])
        if bracket[pos] == "\\":
            pos += 1
            charset = charset + bracket[pos]
        if bracket[pos] == "^":
            pos += 2
            charset = charset.replace(bracket[pos], "")
        pos += 1
    if charset == "":
        logging.warning("complex charset is wrong")
    logging.debug("unpacked charset = {}".format(charset))
    return charset


def find_repeat(st: str):
    match = re.search(r'^{(\d+)}', st)
    if not match:
        logging.error("repeat sequence lacks a closing brace '}'")
        exit(1)
    return int(match.group(1))


if __name__ == "__main__":
    main()
