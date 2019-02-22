from unittest import TestCase, mock
from unittest.mock import patch

from dionysus_app.UI_menus.main_menu import (main_menu_options,
                                             run_main_menu,
                                             take_main_menu_input,
                                             welcome_blurb,
                                             )


class TestWelcomeBlurb(TestCase):
    def setUp(self):
        self.welcome_blurb_print_stmt = "Welcome to Dionysus - student avatar chart generator\n"

    @patch('dionysus_app.UI_menus.main_menu.print')
    def test_welcome_blurb(self, mocked_print):
        assert welcome_blurb() is None
        mocked_print.assert_called_once_with(self.welcome_blurb_print_stmt)


class TestMainMenuOptions(TestCase):
    def setUp(self):
        self.menu_print_stmts = ["Dionysus - Main menu\n",
                                 "Please select an option by entering the corresponding number, and press return:\n",
                                 "     1. Create a classlist\n"
                                 "     2. Edit a classlist\n"
                                 "     3. Create a new chart\n"
                                 "     \n"
                                 "     9. Settings\n"
                                 "     Enter Q to quit.\n",
                                 ]

    @patch('dionysus_app.UI_menus.main_menu.print')
    def test_main_menu_options(self, mocked_print):
        assert main_menu_options() is None
        assert mocked_print.call_args_list == [mock.call(print_stmt) for print_stmt in self.menu_print_stmts]


class TestTakeMainMenuInput(TestCase):
    def setUp(self):
        self.quit_inputs = ['q',
                            'Q',
                            ]
        self.valid_input_option_mock = [('1', 'dionysus_app.UI_menus.main_menu.create_classlist'),
                                        ('2', 'dionysus_app.UI_menus.main_menu.edit_class_data'),
                                        ('3', 'dionysus_app.UI_menus.main_menu.new_chart'),
                                        ('9', 'dionysus_app.UI_menus.main_menu.run_settings_menu'),
                                        ]

        self.invalid_inputs = ['',  # No input, return pressed.
                               ' ',  # Space/blank input.
                               'slightly_silly',  # Bad string input.
                               '0',  # Zero input.
                               '1.0'  # Float of valid input.
                               '-2',  # Negative valid option input.
                               '99',  # Out of range int input.
                               ]
        self.final_valid_input = ['Q']  # Mock a valid input to call quit_app.

        self.bad_input_user_inputs = self.invalid_inputs + self.final_valid_input

        self.invalid_input_print_stmt = 'Invalid input.'

    @patch('dionysus_app.UI_menus.main_menu.input')
    def test_take_main_menu_input_quit(self, mocked_input):
        for quit_input in self.quit_inputs:
            with self.subTest(msg=f'Quit input {quit_input} should return True.'):
                mocked_input.return_value = quit_input

                assert take_main_menu_input() is True

    @patch('dionysus_app.UI_menus.main_menu.input')
    def test_take_main_menu_input_non_quit_option_selected(self, mocked_input):
        for user_input, called_function in self.valid_input_option_mock:
            with self.subTest(msg=f'input={user_input}, should call {called_function}'
                              ), patch(called_function) as mock_called_option:
                mocked_input.return_value = user_input

                # Returns None when feature function is called.
                assert take_main_menu_input() is None

                mock_called_option.assert_called_once()

                mocked_input.reset_mock(return_value=True)

    @patch('dionysus_app.UI_menus.main_menu.print')
    @patch('dionysus_app.UI_menus.main_menu.input')
    def test_take_main_menu_input_bad_input(self, mocked_input, mocked_print):
        mocked_input.side_effect = self.bad_input_user_inputs

        assert take_main_menu_input() is True  # Final return valid quit input.
        assert mocked_print.call_args_list == [mock.call(self.invalid_input_print_stmt)
                                               for invalid_input in self.invalid_inputs]


class TestRunMainMenu(TestCase):
    def setUp(self):
        self.valid_input_to_quit = 'Q'  # Mock a valid input to call quit_app.

    @patch('dionysus_app.UI_menus.main_menu.take_main_menu_input')  # Mock call to take_main_menu_input.
    @patch('dionysus_app.UI_menus.main_menu.main_menu_options')  # Mock call to main_menu_options.
    @patch('dionysus_app.UI_menus.main_menu.welcome_blurb')  # Mock call to welcome_blurb.
    def test_run_main_menu(self,
                           mocked_welcome_blurb,
                           mocked_main_menu_options,
                           mocked_take_main_menu_input,
                           ):
        mocked_take_main_menu_input_returns = [None, None, True]  # 2 mock feature calls, call to quit.
        mocked_take_main_menu_input.side_effect = mocked_take_main_menu_input_returns

        assert run_main_menu() is None

        mocked_welcome_blurb.assert_called_once()

        main_menu_calls = [mock.call() for each_call in mocked_take_main_menu_input_returns]
        assert mocked_main_menu_options.call_args_list == main_menu_calls
        assert mocked_take_main_menu_input.call_args_list == main_menu_calls

    @patch('dionysus_app.UI_menus.main_menu.main_menu_options')  # Mock call to main_menu_options.
    @patch('dionysus_app.UI_menus.main_menu.welcome_blurb')  # Mock call to welcome_blurb.
    @patch('dionysus_app.UI_menus.main_menu.input')
    def test_run_main_menu_call_unmocked_take_menu_input(self,
                                                         mocked_input,
                                                         mocked_welcome_blurb,
                                                         mocked_main_menu_options,
                                                         ):
        mocked_input.return_value = self.valid_input_to_quit

        assert run_main_menu() is None

        mocked_welcome_blurb.assert_called_once()
        mocked_main_menu_options.assert_called_once()
