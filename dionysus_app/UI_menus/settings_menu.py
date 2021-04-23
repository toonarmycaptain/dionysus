"""Settings menu UI"""
from typing import Optional

from dionysus_app.settings_functions import set_default_chart_save_location
from dionysus_app.UI_menus.UI_functions import get_user_input


def run_settings_menu() -> None:
    """
    Runs settings menu.

    :return: None
    """
    while True:
        settings_menu_options()
        return_to_main = take_settings_menu_input()

        if return_to_main:  # User selects to return to main menu
            break


def settings_menu_options() -> None:
    """
    Print settings menu options to console.

    :return: None
    """
    print("Dionysus - Settings\n")
    print("Please select an option by entering the corresponding number, and press return:\n"
          "     1. Change default chart save location.\n"
          "     2. Change database backend.\n"
          "     \n"
          "     0. Return to main menu."
          )


def take_settings_menu_input() -> Optional[bool]:
    """
    Takes input and runs chosen action.

    Loop broken when chosen action completes, returning None and
    returning to the loop in run_settings_menu, which will reprint the
    menu options. If '0' is entered to return to the main menu, the loop
    returns True, triggering the
    flag in run_settings_menu, breaking that loop, and returning to the
    loop in run_main_menu.

    :return: None or True
    """
    possible_options = {
        '1': call_set_default_chart_save_location,
        '2': call_set_database_backend,  # Future option.
        '0': return_to_main_menu,
        }

    chosen_option = get_user_input(prompt='>>> ',
                                   validation=lambda choice: choice in possible_options,
                                   validation_error_msg="Invalid input.")
    possible_options[chosen_option]()
    if chosen_option == '0':  # User selects to return to main menu.
        return True
    # else:
    return None


def call_set_default_chart_save_location() -> None:
    """
    Calls set_default_chart_save_location(user_set=True)

    :return: None
    """
    set_default_chart_save_location(user_set=True)
    print('\n\n')


def call_set_database_backend() -> None:
    """
    Calls set_database_backend. Current prints unimplemented message.

    :return: None
    """
    print("This feature is not yet implemented.\n"
          "Please contact the developer and ply him with liquor, coffee, and\n"
          "other desirables if you would like to see this feature.\n")


def return_to_main_menu() -> bool:
    """
    Prints return to main menu message.

    Returns False to indicate user returning to main menu, rather than
    choosing another option.

    :return: False
    """
    print('Returning to main menu...\n\n\n')
    return False
