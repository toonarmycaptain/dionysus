"""
Application main menu.
"""

import sys

from dionysus_app.class_functions import create_classlist
from dionysus_app.chart_generator.create_chart import new_chart
from dionysus_app.UI_menus.edit_class_data import edit_class_data
from dionysus_app.UI_menus.settings_menu import run_settings_menu


def welcome_blurb():
    print("Welcome to Dionysus - student avatar chart generator\n")


def main_menu_options():
    print("Dionysus - Main menu\n")
    print("Please select an option by entering the corresponding number, and press return:\n"
          "     1. Create a classlist\n"
          "     2. Edit a classlist\n"
          "     3. Create a new chart\n"
          "     \n"
          "     9. Settings\n"
          "     Enter Q to quit.\n")


def take_main_menu_input():
    """
    Takes input and runs chosen action.
    Flag for unselected/no option chosen used to exit the loop when chosen
    action finishes, returning to main menu run loop rather than option
    selection, which will reprint the menu options.
     
    :return: None
    """
    possible_options = {
        '1': create_classlist,
        '2': edit_class_data,
        '3': new_chart,
        '9': run_settings_menu,
        'q': quit_app,
        'Q': quit_app,
        }
    unselected = True
    while unselected:
        chosen_option = input('>>> ')

        if chosen_option in possible_options:
            possible_options[chosen_option]()
            unselected = False  # Exiting the loop when chosen action finishes.
        else:
            print("Invalid input.")


def quit_app():
    sys.exit()


# Create a classlist
    # enter name and avatar file location

# Edit a class list
    # edit list entries
    # edit individual student data (eg name spelling, change image)


def run_main_menu():
    welcome_blurb()

    while True:
        main_menu_options()
        take_main_menu_input()
    quit_app()


if __name__ == "__main__":
    run_main_menu()
