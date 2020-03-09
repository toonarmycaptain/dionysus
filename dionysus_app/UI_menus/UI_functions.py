"""
UI functions: user interface functions used throughout the application.
"""

import tkinter as tk

from pathlib import Path
from tkinter import filedialog


def clear_screen(num_lines=50):
    clear_seq = '\n' * num_lines

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
    and underscores, stripping trailing spaces.

    Replace disallowed characters with underscores to preserve form.

    >>> scrub_candidate_filename(r"Les méµoires¬de¬M. d'Ar∫@gnåñ  /\/\ 'abc∂éåß®∆˚__˙©¬ñ√ƒµ©∆∫ø'")
    'Les méµoires_de_M_ d_Ar__gnåñ  ____ _abc_éåß________ñ_ƒµ___ø_'

    # Which at least makes distinct words clear, rather than:
    'Les méµoiresdeM dArgnåñ   abcéåßñƒµø'  # Which is completely unreadable.


    :param dirty_string: str
    :return: str
    """
    allowed_special_characters = [' ', '_', '-', ]
    cleaned_string = "".join([c if c.isalnum()
                                   or c in allowed_special_characters
                              else '_'
                              for c in dirty_string
                              ]).rstrip()

    return cleaned_string


def save_as_dialogue(title_str=None,
                     default_file_extension=None,
                     filetypes=None,
                     suggested_filename=None,
                     start_dir=None
                     ):
    """
    Prompts user to select a directory and filename to save a file to.
    Calls tkinter filedialog.asksaveasfilename with title (if provided), and
    filetype argument (if provided) eg '*.png'.

    title_str is string to be displayed in popup's title bar.
    NB if none provided, or is None - title displayed is "Save as".

    default_filetype is a string to be added as an extension (eg '.png, but can
        be anything (eg 'dead_parrot', '_chart.png' in the event user does not
        input a name with an extension.
        If no default_filetype is provided, but optional filetypes are provided,
        convention will be for default extension to be listed first.
        eg if all files option: [('.png', '*.png'), ("all files", "*.*")]
            - .png will be default extension
        eg if default filetypes display (the first to appear in drop down) is to
        be all files, user must pass a default extension.

    start_dir is a path string for the folder to start the dialogue box in.

    filetypes is a list of tuples with 2 values, a label and a pattern
        eg for png and all files: [('.png', '*.png'), ("all files", "*.*")]

    suggested_filename is a string displayed in popup as suggested filename,
        user can change/alter as desired.

    Returns None instead of empty string if no file is selected.



    NB When default_file_extension is given, but not in filetypes, if
    the first filetype in filetypes is NOT ("all files", "*.*"), that
    first filetype in filetypes will by appended rather than the default
    extension. If ("all files", "*.*") is the first filetype, the
    default_file_extension will be appended as expected.

    :param title_str: str
    :param default_file_extension: list
    :param suggested_filename: str
    :param filetypes: list
    :param start_dir: str
    :return: str
    """
    root = tk.Tk()
    root.withdraw()

    if filetypes and not default_file_extension:
        # Make extension of first listed filetype default save extension.
        first_extension_without_wildcard = filetypes[0][1].strip('*')
        if first_extension_without_wildcard != '.':
            default_file_extension = first_extension_without_wildcard

    default_filetypes = [("all files", "*.*")]
    if not filetypes:
        filetypes = default_filetypes
    filepath_str = filedialog.asksaveasfilename(title=title_str,
                                                defaultextension=default_file_extension,
                                                filetypes=filetypes,
                                                initialfile=suggested_filename,
                                                initialdir=start_dir,
                                                )

    if filepath_str == '':
        return None
    return filepath_str


def select_file_dialogue(title_str=None,
                         filetypes=None,
                         start_dir=None,
                         ):
    """
    Prompts user to select a file. Calls tkinter filedialog.askopenfilename
    with title (if provided), and filetype argument (if provided) eg '*.png'.

    filetypes is a list of tuples with 2 values, a label and a pattern
    eg for png and all files: [('.png', '*.png'), ("all files", "*.*")]

    Returns None instead of empty string if no file is selected.

    NB If no title is passed to filedialog.askopenfilename, the window
    title will be "Open".

    :param title_str: str
    :param filetypes: list
    :param start_dir: str
    :return: str
    """
    root = tk.Tk()
    root.withdraw()

    default_filetypes = [("all files", "*.*")]
    if not filetypes:
        filetypes = default_filetypes
    filepath_str = filedialog.askopenfilename(title=title_str,
                                              filetype=filetypes,
                                              initialdir=start_dir,
                                              )

    if filepath_str == '':
        return None
    return Path(filepath_str)


def select_folder_dialogue(title_str=None, start_dir='..'):
    """
    Prompts user to select a file. Calls tkinter filedialog.askopenfilename
    with title (if provided), and filetype argument (if provided) eg '*.png'.

    filetypes is a list of tuples with 2 values, a label and a pattern
    eg for png and all files: [('.png', '*.png'), ("all files", "*.*")]

    Returns None instead of empty string if no file is selected.

    :param title_str: str
    :param start_dir: str - Path for dialogue to start in.
    :return: str
    """
    root = tk.Tk()
    root.withdraw()

    dir_path_str = filedialog.askdirectory(initialdir=start_dir, title=title_str)

    if dir_path_str == '':
        return None
    return Path(dir_path_str)


if __name__ == '__main__':
    pass
