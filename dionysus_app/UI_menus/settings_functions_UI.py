"""UI elements for settings"""

from dionysus_app.data_folder import DataFolder
from dionysus_app.UI_menus.UI_functions import (clear_screen,
                                                select_folder_dialogue
                                                )

APP_DEFAULT_CHART_SAVE_FOLDER = DataFolder.generate_rel_path(
    DataFolder.APP_DEFAULT_CHART_SAVE_FOLDER.value)


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


def user_set_chart_save_folder():
    dialogue_message = ('Please select location for chart save folder, or'
                        ' press cancel to use default.')
    new_default_save_location = select_folder_dialogue(title_str=dialogue_message, start_dir='..')

    if not new_default_save_location:  # User presses cancel, doesn't select a folder.
        return APP_DEFAULT_CHART_SAVE_FOLDER
    # else:
    print(f'Default chart save folder set to {new_default_save_location}')
    return new_default_save_location
