"""UI elements for settings"""
from pathlib import Path
from typing import Union

from dionysus_app.data_folder import DataFolder
from dionysus_app.UI_menus.UI_functions import (ask_user_bool,
                                                clear_screen,
                                                get_user_input,
                                                select_folder_dialogue,
                                                )

APP_DEFAULT_CHART_SAVE_DIR = DataFolder.generate_rel_path(
    DataFolder.APP_DEFAULT_CHART_SAVE_DIR.value)


def welcome_to_program() -> None:
    """
    Print welcome message on first program run, preface app config.

    :return: None
    """
    print('Welcome to dionysus.\n'
          'It looks like this is your first time running the program.\n'
          'Before getting started, there are some setup options: \n\n')


def welcome_set_default_location_message() -> None:
    """
    Welcome message prompting user to select default save chart dir.

    Prints welcome message prompting user to select a folder in which to
    save charts by default, if desired.

    :return: None
    """
    print('Would you like to set a default location to save your charts?\n'
          'You can do this later or change your selection in Settings.\n'
          )


def get_user_choice_to_set_location() -> bool:
    """
    Gets user choice to set default chart dir location.

    Returns True for some variation of Y or yes, otherwise returning False.

    :return: bool
    """
    selection = input("Type 'Y' for Yes or 'N' for No, and press enter: ")

    return selection.upper() in ['Y', 'YES']


def user_decides_to_set_default_location() -> bool:
    """
    Get user desire to set default chart location.

    Prints welcome message instructions, takes user choice to set a
    default location to save charts, clears screen for main_menu
    presentation, returns True/False.

    :return: bool
    """
    welcome_set_default_location_message()
    user_choice = get_user_choice_to_set_location()

    clear_screen()
    return user_choice


def user_set_chart_save_folder() -> Path:
    """
    Prompt user for dir to save created charts in.

    Returns default if user declines.

    :return: Path
    """
    dialogue_message = ('Please select location for chart save folder, or'
                        ' press cancel to use default.')
    new_default_save_location = select_folder_dialogue(title_str=dialogue_message, start_dir='..')

    if not new_default_save_location:  # User presses cancel, doesn't select a folder.
        return APP_DEFAULT_CHART_SAVE_DIR
    # else:
    print(f'Default chart save folder set to {new_default_save_location}')
    return new_default_save_location


def user_decides_to_set_database_backend() -> bool:
    """
    Ask user if they would like to select a database backend.

    :return: bool
    """
    return ask_user_bool(
        question="Would you like to select a database backend?\n"
                 "Type 'Y' for Yes or 'N' to use the default, and press enter [Y/N]: ",
        invalid_input_response='Invalid response, please try again.')


def user_set_database_backend() -> Union[str, bool]:
    """
    Display database backend choices and return user chosen option.

    Returns False if none is chosen.

    :return: str or False
    """
    display_database_backend_options()
    return take_database_choice_input()


def display_database_backend_options() -> None:
    """
    Display database backend options.

    :return: None
    """
    print("Dionysus - Select database backend\n")
    print("Please select a database backend by entering the corresponding number,"
          " and press return:\n"
          "     1. JSON database.\n"
          "     2. SQLite3 database.\n"
          "     3. SQLAlchemy wrapped SQLite3 database.\n"
          "     0. Cancel."
          )


def take_database_choice_input() -> Union[str, bool]:
    """
    Take user choice of database backends.

    Return string name of the chosen backend, or False if user does not
    choose a backend.

    Alternate implementation that pulls the choice list from those
    enabled in the persistence.database_functions module:

    from dionysus_app.persistence.database_functions import database_backends
    possible_options = dict(enumerate(database_backends, start=1))

    :return: str or False
    """
    possible_options = {
        '1': 'JSON',
        '2': 'SQLite',
        '3': 'SQLiteSQLAlchemy',
        '0': False,  # Cancel/return to menu.
        }

    chosen_option = get_user_input(prompt='>>> ',
                                   validation=lambda user_input: user_input in possible_options,
                                   validation_error_msg="Invalid input.")
    return possible_options[chosen_option]  # type: ignore
