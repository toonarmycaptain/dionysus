"""UI elements for settings"""
from dionysus_app.UI_menus.UI_functions import clear_screen


def welcome_set_default_location_message():
    """
    Prints welcome message prompting user to select a folder to save
    charts by default, if desired.

    :return: None
    """
    print('Welcome to dionysus.\n'
          'It looks like this is your first time running the program.\n\n'
          'Would you like to set a default location to save your charts?\n'
          'You can do this later or change your selection in Settings.\n'
          )


def get_user_choice_to_set_location():
    """
    Gets user choice, returning True for some variation of Y or yes,
    otherwise returning False.

    :return: bool
    """
    selection = input("Type 'Y' for Yes or 'N' for No, and press enter: ")

    if selection.upper() == 'Y' or selection.upper() == 'YES':
        return True
    # else: user entered 'N' (or anything else), or pressed return without entry (which returns '')
    return False


def user_decides_to_set_default_location():
    """
    Prints welcome message instructions, takes user choice to set a
    default location to save charts, clears screen for main_menu
    presentation, returns True/False.

    :return: bool
    """
    welcome_set_default_location_message()
    user_choice = get_user_choice_to_set_location()

    clear_screen()
    return user_choice
