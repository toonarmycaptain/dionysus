"""
Application main menu.
"""

import sys


def welcome_blurb():
    print("Welcome to Dionysus - student avatar graph generator\n")


def main_menu_options():
    print("Please select an option by entering the corresponding number, and press return:\n"
          "     1. Create a classlist\n"
          "     2. Edit a classlist\n"
          "     3. Create a new graph\n"
          "     Enter Q to quit.\n")


def take_main_menu_input():
    possible_options = {
        '1': 'create_classlist()',
        '2': 'edit_classlist()',
        '3': 'create_graph()',
    }

    while True:

        chosen_option = input('>>> ')


        if chosen_option == 'Q' or chosen_option == 'q':
            break
        try:
            possible_options[chosen_option]
        except KeyError:
            print("Invalid input.")

    sys.exit()


# Create a classlist
    # enter name and avatar file location

# Edit a class list
    # edit list entries
    # edit individual student data (eg name spelling, change image)


def run_main_menu():
    welcome_blurb()
    main_menu_options()
    take_main_menu_input()


if __name__ == "__main__":
    run_main_menu()
