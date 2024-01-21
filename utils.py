import logging
import random
import string


def placeholder2charset(ph: str):
    if ph == "d": return string.digits
    if ph == "l": return string.ascii_lowercase
    if ph == "u": return string.ascii_uppercase
    if ph == "L": return string.ascii_letters
    if ph == "p": return ",.;:"
    if ph == "a": return string.ascii_lowercase + string.digits
    if ph == "A": return string.ascii_letters + string.digits
    if ph == "U": return string.ascii_uppercase + string.digits
    if ph == "h": return '0123456789abcdef'
    if ph == "H": return '0123456789ABCDEF'
    if ph == "v": return 'aeiou'
    if ph == "V": return 'AEIOUaeiou'
    if ph == "Z": return 'AEIOU'
    if ph == "c": return 'bcdfghjklmnpqrstvwxyz'
    if ph == "C": return 'BCDFGHJKLMNPQRSTVWXYZ bcdfghjklmnpqrstvwxyz'
    if ph == "z": return 'BCDFGHJKLMNPQRSTVWXYZ'
    if ph == "b": return '()[]{}<>'
    if ph == "s": return string.punctuation
    if ph == "S": return string.ascii_letters + string.digits + string.punctuation
    if ph == "x": return r"""¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"""
    if ph == "Q": return 'ABCEHIKMOPTX'

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