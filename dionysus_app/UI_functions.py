"""
UI functions: user interface functions used throughout the application.
"""

HUNDRED_NEWLINES = '\n'*100


def clear_screen(clear_seq=HUNDRED_NEWLINES):

    print(clear_seq)


# User input and string processing functions:


def input_is_essentially_blank(subject_string: str):
    """
    Return True if string is empty or primarily composed of spaces, underscores,
    special characters (eg brackets, punctuation).

    Uses similar method to clean_for_filename to remove all except alphanumeric
    characters, then returns True if string is empty (is no numbers or letters.

    :param subject_string: str
    :return: bool
    """
    cleaned_string = "".join([c for c in subject_string if c.isalnum()]).rstrip()
    if cleaned_string == '':
        return True
    # else:
    return False


def clean_for_filename(some_string: str):
    """
    Cleans a string for use as a filename.
    eg student or classlist name

    Returns a string with only alphanumeric characters and underscores.

    # Possibly equivalent to: ''.join([c for c in text if re.match(r'\w', c)])

    :param some_string: str
    :return: str
    """
    cleaner_filename = scrub_candidate_filename(some_string)
    cleaned_filename = cleaner_filename.replace(' ', '_')  # no slashes either
    return cleaned_filename


def scrub_candidate_filename(dirty_string: str):
    """
    Cleans string of non-alpha-numeric characters, but leaves spaces, dashes,
    apostrophes, and underscores, stripping trailing spaces.

    If apostrophe causes problems, will have to replace with dash or similar,
    but they are frequently used in names, so allowing until a problem emerges.

    :param dirty_string: str
    :return: str
    """
    allowed_special_characters = [' ', '_', '-', "'"]  # TODO: test if apostrophe causes problems
    cleaned_string = "".join([c for c in dirty_string
                              if c.isalnum()
                              or c in allowed_special_characters]).rstrip()
    return cleaned_string
