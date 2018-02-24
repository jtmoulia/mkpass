import os.path
import random
import sys

import xkcdpass.xkcd_password as xp


def random_capitalization(s, chance):
    new_str = []
    for i, c in enumerate(s):
        new_str.append(c.upper() if random.random() < chance else c)
    return "".join(new_str)


def capitalize_first_letter_randomly(word):
    if bool(random.randint(0, 1)):
        return word.capitalize()
    return word


def add_digit_randomly(word):
    """
    Return word with a digit maybe added to the word in the front or the back.
    """
    is_digited = bool(random.randint(0, 1))
    if is_digited:
        is_prefix = bool(random.randint(0, 1))
        digit = str(random.randint(0, 9))
        return digit + word if is_prefix else word + digit
    return word


def yield_words(wordlist, options):
    """Yield the specified number of passwords."""
    count = options.count
    while count > 0:
        yield xp.generate_xkcdpassword(
            wordlist,
            interactive=options.interactive,
            numwords=options.numwords,
            acrostic=options.acrostic,
            delimiter=options.delimiter).split(options.delimiter)
        count -= 1


def apply_transforms(target, transforms=None):
    transforms = transforms or [
        capitalize_first_letter_randomly,
        add_digit_randomly,
    ]
    for transform in transforms:
        target = transform(target)
    return target


def main(argv=None):
    """Mainline code for mkpass."""
    if argv is None:
        argv = sys.argv

    exit_status = 0
    try:
        program_name = os.path.basename(argv[0])
        parser = xp.XkcdPassArgumentParser(prog=program_name)
        parser.add_argument(
            "-D", "--digits",
            action="store_true", dest="digits", default=False,
            help="Include random digits between words.")

        options = parser.parse_args(argv[1:])
        xp.validate_options(parser, options)

        my_wordlist = xp.generate_wordlist(
            wordfile=options.wordfile,
            min_length=options.min_length,
            max_length=options.max_length,
            valid_chars=options.valid_chars)

        if options.verbose:
            xp.verbose_reports(my_wordlist, options)

        for words in yield_words(my_wordlist,options):
            xwords = [apply_transforms(word) for word in words]
            print(options.delimiter.join(xwords))

    except SystemExit as exc:
        exit_status = exc.code

    return exit_status


if __name__ == '__main__':
    exit_status = main(sys.argv)
    sys.exit(exit_status)
