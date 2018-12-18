"""Settings menu UI"""

from dionysus_app.settings_functions import set_default_chart_save_location


def run_settings_menu():

    while True:
        settings_menu_options()
        return_to_main = take_settings_menu_input()

        if return_to_main:  # User selects to return to main menu
            break


def settings_menu_options():
    print("Dionysus - Settings\n")
    print("Please select an option by entering the corresponding number, and press return:\n"
          "     1. Change default chart save location.\n"
          "     \n"
          "     0. Return to main menu."
          )


def take_settings_menu_input():
    """
    Takes input and runs chosen action.
    Flag for unselected/no option chosen used to exit the loop when chosen
    action finishes, returning to main menu run loop rather than option
    selection, which will reprint the menu options.

    :return: None
    """
    possible_options = {
        '1': call_set_default_chart_save_location,
        '0': return_to_main_menu
        }
    unselected = True
    chosen_option = None
    while unselected:
        chosen_option = input('>>> ')

        if chosen_option in possible_options:
            possible_options[chosen_option]()
            unselected = False  # Exiting the loop when chosen action finishes.
        else:
            print("Invalid input.")

    if chosen_option == '0':  # user selects to return to main menu
        return True
    return False


def call_set_default_chart_save_location():
    """
    Calls set_default_chart_save_location(user_set=True)
    :return: None
    """
    set_default_chart_save_location(user_set=True)
    print('\n\n')


def return_to_main_menu():
    """
    Prints return to main menu message.
    :return: False
    """
    print('Returning to main menu...\n\n\n')
    return False
