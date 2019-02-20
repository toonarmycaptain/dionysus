"""Test settings_menu."""

from unittest import TestCase, mock
from unittest.mock import patch

from dionysus_app.UI_menus.settings_menu import (run_settings_menu,
                                    )


class TestRunSettingsMenu(TestCase):
    def setUp(self):
        self.return_to_main_menu_input = '0'



    @patch('dionysus_app.UI_menus.settings_menu.take_settings_menu_input')
    @patch('dionysus_app.UI_menus.settings_menu.settings_menu_options')
    def test_run_settings_menu(self,
                               mocked_settings_menu_options,
                               mocked_take_settings_menu_input
                               ):

        mocked_take_settings_menu_input_returns = [None, None, True] # 2 mock feature calls, return to main menu.
        mocked_take_settings_menu_input.side_effect = mocked_take_settings_menu_input_returns

        assert run_settings_menu() is None

        main_menu_calls = [mock.call() for each_call in mocked_take_settings_menu_input_returns]
        assert mocked_settings_menu_options.call_args_list == main_menu_calls
        assert mocked_take_settings_menu_input.call_args_list == main_menu_calls





class TestTakeSettingsMenuInput(TestCase):
    def setUp(self):
        self.return_to_main_menu_input = '0'

        self.valid_input_option_mock = [
            ('1', 'dionysus_app.UI_menus.settings_menu.call_set_default_chart_save_location'),
            ('0', 'dionysus_app.UI_menus.settings_menu.return_to_main_menu'),
            ]

        self.invalid_inputs = ['',  # No input, return pressed.
                               ' ',  # Space/blank input.
                               'slightly_silly',  # Bad string input.
                               '0',  # Zero input.
                               '1.0'  # Float of valid input.
                               '-2',  # Negative valid option input.
                               '99',  # Out of range int input.
                               ]

        self.final_valid_input = self.return_to_main_menu_input
"""

    possible_options = {
        '1': call_set_default_chart_save_location,
        '0': return_to_main_menu,
        }

    while True:
        chosen_option = input('>>> ')

        if chosen_option in possible_options:
            possible_options[chosen_option]()
            break  # Exit loop when chosen action finishes. Returns None.
        if chosen_option == '0':  # User selects to return to main menu.
            return True
        # else:
        print("Invalid input.")
"""