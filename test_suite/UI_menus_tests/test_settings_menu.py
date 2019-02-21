"""Test settings_menu."""

from unittest import TestCase, mock
from unittest.mock import patch

from dionysus_app.UI_menus.settings_menu import (call_set_default_chart_save_location,
                                                 return_to_main_menu,
                                                 run_settings_menu,
                                                 settings_menu_options,
                                                 take_settings_menu_input,
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

        mocked_take_settings_menu_input_returns = [None, None, True]  # 2 mock feature calls, return to main menu.
        mocked_take_settings_menu_input.side_effect = mocked_take_settings_menu_input_returns

        assert run_settings_menu() is None

        main_menu_calls = [mock.call() for each_call in mocked_take_settings_menu_input_returns]
        assert mocked_settings_menu_options.call_args_list == main_menu_calls
        assert mocked_take_settings_menu_input.call_args_list == main_menu_calls


class TestSettingsMenuOptions(TestCase):
    def setUp(self):
        self.expected_print_stmts = [
            "Dionysus - Settings\n",
            ("Please select an option by entering the corresponding number, and press return:\n"
             "     1. Change default chart save location.\n"
             "     \n"
             "     0. Return to main menu."
             ),
             ]

    @patch('dionysus_app.UI_menus.settings_menu.print')
    def test_settings_menu_options(self, mocked_print):
        assert settings_menu_options() is None

        mocked_print_call_args_list = [mock.call(print_stmt)
                                       for print_stmt in self.expected_print_stmts]
        assert mocked_print.call_args_list == mocked_print_call_args_list


class TestTakeSettingsMenuInput(TestCase):
    def setUp(self):
        self.return_to_main_menu_input = '0'

        self.valid_input_option_mock = [
            ('1', 'dionysus_app.UI_menus.settings_menu.call_set_default_chart_save_location', None),
            # ('0', 'dionysus_app.UI_menus.settings_menu.return_to_main_menu', True),
            ]

        self.invalid_inputs = ['',  # No input, return pressed.
                               ' ',  # Space/blank input.
                               'slightly_silly',  # Bad string input.
                               '1.0'  # Float of valid input.
                               '-2',  # Negative valid option input.
                               '99',  # Out of range int input.
                               ]

        self.final_valid_input = self.return_to_main_menu_input

        self.bad_input_user_inputs = self.invalid_inputs + [self.final_valid_input]

        self.invalid_input_print_stmt = 'Invalid input.'

    @patch('dionysus_app.UI_menus.settings_menu.return_to_main_menu')
    @patch('dionysus_app.UI_menus.settings_menu.input')
    def test_take_settings_menu_input_return_to_main_menu(self,
                                                          mocked_input,
                                                          mocked_return_to_main_menu):
        with self.subTest(msg=f'Return to main menu input: '
                              f'{self.return_to_main_menu_input} should return True.'):
            mocked_input.return_value = '0'  # self.return_to_main_menu_input

            assert take_settings_menu_input() is True

            assert mocked_return_to_main_menu.called_once_with()

    @patch('dionysus_app.UI_menus.settings_menu.input')
    def test_take_main_menu_input_all_valid_inputs(self, mocked_input):
        for user_input, called_function, returned_value in self.valid_input_option_mock:
            with self.subTest(msg=f'input={user_input}, should call {called_function}'
                              ), patch(called_function) as mock_called_option:
                mocked_input.return_value = user_input

                assert take_settings_menu_input() is returned_value

                mock_called_option.assert_called()

                mocked_input.reset_mock(return_value=True)

    @patch('dionysus_app.UI_menus.settings_menu.print')
    @patch('dionysus_app.UI_menus.settings_menu.input')
    def test_take_settings_menu_input_bad_input(self, mocked_input, mocked_print):
        mocked_input.side_effect = self.bad_input_user_inputs

        assert take_settings_menu_input() is True  # Final return valid quit input.
        assert mocked_print.call_args_list == [mock.call(self.invalid_input_print_stmt)
                                               for invalid_input in self.invalid_inputs]


class TestCallSetDefaultChartSaveLocation(TestCase):
    def setUp(self):
        self.after_call_print_stmt = '\n\n'

    @patch('dionysus_app.UI_menus.settings_menu.print')
    @patch('dionysus_app.UI_menus.settings_menu.set_default_chart_save_location')
    def test_call_set_default_chart_save_location(self,
                                                  mocked_set_default_chart_save_location,
                                                  mocked_print):
        assert call_set_default_chart_save_location() is None

        mocked_set_default_chart_save_location.assert_called_once_with(user_set=True)
        mocked_print.assert_called_once_with(self.after_call_print_stmt)


class TestReturnToMainMenu(TestCase):
    def setUp(self):
        self.return_to_main_menu_print_stmt = 'Returning to main menu...\n\n\n'

    @patch('dionysus_app.UI_menus.settings_menu.print')
    def test_return_to_main_menu(self, mocked_print):
        assert return_to_main_menu() is False

        mocked_print.assert_called_once_with(self.return_to_main_menu_print_stmt)
