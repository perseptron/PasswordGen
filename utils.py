import logging
import random
import string


def placeholder2charset(ph: str):
    if ph == "d": return string.digits
    if ph == "l": return string.ascii_lowercase
    if ph == "u": return string.ascii_uppercase
    if ph == "L": return string.ascii_letters
    if ph == "p": return ",.;:"
    logging.warning("wrong placeholder")
    return ""


def dedup(chars: str):
    logging.debug("charset before deduplication = " + chars)
    chars = list(set(chars))
    logging.debug("charset after deduplication = " + "".join(sorted(chars)))
    return chars


def permutate(lst: list, args):
    if args.m:
        logging.debug("permutation")
        random.shuffle(lst)
    return "".join(lst)


def generate_char(charset: list):
    try:
        pass_char = charset[random.randrange(len(charset))]
    except ValueError as error:
        logging.warning('can\'t generate character because of "{}", skipping'.format(error))
        pass_char = ""
    logging.debug("generating password character '{}' using next charset {}".format(pass_char, "".join(charset)))
    return pass_char