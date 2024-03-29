"""
Application main menu.
"""
from typing import Callable, Optional

from dionysus_app.chart_generator.create_chart import new_chart
from dionysus_app.class_functions import create_classlist
from dionysus_app.UI_menus.edit_class_data_UI import edit_class_data
from dionysus_app.UI_menus.settings_menu import run_settings_menu
from dionysus_app.UI_menus.UI_functions import get_user_input


def welcome_blurb() -> None:
    """
    Print welcome statement to console.

    :return: None
    """
    print("Welcome to Dionysus - student avatar chart generator\n")


def main_menu_options() -> None:
    """
    Print main menu options to console.

    :return: None
    """
    print("Dionysus - Main menu\n")
    print("Please select an option by entering the corresponding number, and press return:\n")
    print("     1. Create a classlist\n"
          "     2. Edit a classlist\n"
          "     3. Create a new chart\n"
          "     \n"
          "     9. Settings\n"
          "     Enter Q to quit.\n"
          )


def take_main_menu_input() -> Optional[bool]:
    """
    Takes input and runs chosen action.

    Loop broken when chosen action completes, returning None and
    returning to the loop in run_main_menu, which will reprint the menu
    options. If 'Q' is entered to quit app, returns True, triggering the
    flag in run_main_menu, breaking that loop, and proceeding to app
    quit/shutdown code.

    possible_options must be type hinted or mypy will complain about:
        "error: Cannot call function of unknown type"

    :return: None or True
    """
    possible_options: dict[str, Callable] = {
        '1': create_classlist,
        '2': edit_class_data,
        '3': new_chart,
        '9': run_settings_menu,
        }

    def input_validator(user_input: str) -> bool:
        return user_input in possible_options or user_input.upper() == 'Q'

    chosen_option = get_user_input(prompt='>>> ', validation=input_validator,
                                   validation_error_msg='Invalid input.')
    if chosen_option.upper() == 'Q':
        return True  # Quit app.
    possible_options[chosen_option]()
    return None


def run_main_menu() -> None:
    """
    Display welcome blurb, start main menu.

    :return: None
    """
    welcome_blurb()

    while True:
        main_menu_options()
        quit_app = take_main_menu_input()
        if quit_app:
            break
