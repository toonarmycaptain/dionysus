"""
UI functions: user interface functions used throughout the application.
"""

import tkinter as tk
from tkinter import filedialog

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


def select_file_dialogue(title_str=None, filetypes=None):
    """
    Prompts user to select a file. Calls tkinter filedialog.askopenfilename
    with title (if provided), and filetype argument (if provided) eg '*.png'.

    filetypes is a list of tuples with 2 values, a label and a pattern
    eg for png and all files: [('.png', '*.png'), ("all files", "*.*")]

    Returns None instead of empty string if no file is selected.

    :param title_str: str
    :param filetypes: list
    :return: str
    """
    root = tk.Tk()
    root.withdraw()

    default_filetypes = [("all files", "*.*")]
    if not filetypes:
        filetypes = default_filetypes
    filepath_str = filedialog.askopenfilename(title=title_str, filetype=filetypes)

    if filepath_str == '':
        return None
    return filepath_str


def select_folder_dialogue(title_str=None, initial_dir='..'):
    """
    Prompts user to select a file. Calls tkinter filedialog.askopenfilename
    with title (if provided), and filetype argument (if provided) eg '*.png'.

    filetypes is a list of tuples with 2 values, a label and a pattern
    eg for png and all files: [('.png', '*.png'), ("all files", "*.*")]

    Returns None instead of empty string if no file is selected.

    :param title_str: str
    :param initial_dir: str - Path for dialogue to start in.
    :return: str
    """
    root = tk.Tk()
    root.withdraw()

    dir_path_str = filedialog.askdirectory(initialdir=initial_dir, title=title_str)

    if dir_path_str == '':
        return None
    return dir_path_str


if __name__ == '__main__':
    pass
