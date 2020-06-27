import pytest

from unittest.mock import patch


from dionysus_app.UI_menus import main_menu

from dionysus_app.UI_menus.main_menu import (main_menu_options,
                                             run_main_menu,
                                             take_main_menu_input,
                                             welcome_blurb,
                                             )


class TestWelcomeBlurb:
    def test_welcome_blurb(self, capsys):
        """Welcome statement printed."""
        welcome_blurb_print_stmt = "Welcome to Dionysus - student avatar chart generator\n"

        assert welcome_blurb() is None
        # Message printed.
        captured = capsys.readouterr()
        assert welcome_blurb_print_stmt in captured.out


class TestMainMenuOptions:
    def test_main_menu_options(self, capsys):
        """Options all printed."""
        menu_print_stmts = ["Dionysus - Main menu\n",
                            "Please select an option by entering the corresponding number, and press return:\n",
                            "     1. Create a classlist\n"
                            "     2. Edit a classlist\n"
                            "     3. Create a new chart\n"
                            "     \n"
                            "     9. Settings\n"
                            "     Enter Q to quit.\n",
                            ]

        assert main_menu_options() is None
        # Confirm options printed.
        captured = capsys.readouterr()
        assert all([output in captured.out for output in menu_print_stmts])


class TestTakeMainMenuInput:
    @pytest.mark.parametrize(
        'valid_input, called_function, returned_value',
        [(['1'], 'create_classlist', None),
         (['2'], 'edit_class_data', None),
         (['3'], 'new_chart', None),
         (['9'], 'run_settings_menu', None),
         (['q'], None, True),  # User quit, None because no function should be called.
         (['Q'], None, True),  # User quit, None because no function should be called.
         pytest.param(['1'], 'edit_class_data', '', marks=pytest.mark.xfail(reason='Wrong function called.')),
         pytest.param(['2'], '', True,
                      marks=pytest.mark.xfail(reason='Function not called.')),
         pytest.param(['Q'], 'create_classlist', True,  # Quit should return True.
                      marks=pytest.mark.xfail(reason='Quit, function not called.')),
         pytest.param(['Q'], 'create_classlist', None,  # Function should return None.
                      marks=pytest.mark.xfail(reason='Quit, function not called.')),
         pytest.param(['Q'], None, None,
                      marks=pytest.mark.xfail(reason='Quit, not returning True.')),
         pytest.param(['1'], 'create_classlist', True,
                      marks=pytest.mark.xfail(reason='Wrong return value.')),
         ])
    def test_take_main_menu_input_quit(self, monkeypatch,
                                       valid_input, called_function, returned_value, ):
        called = {called_function: False,  # Initialise called_function as False ie not called.
                  None: True}  # Initialise None=True: None won't be called (reset None=True if called_function=None).

        def mocked_create_classlist():
            if 'create_classlist' not in called_function:
                raise ValueError('This function should not have been called.')
            called['create_classlist'] = True

        def mocked_edit_class_data():
            if 'edit_class_data' not in called_function:
                raise ValueError('This function should not have been called.')
            called['edit_class_data'] = True

        def mocked_new_chart():
            if 'new_chart' not in called_function:
                raise ValueError('This function should not have been called.')
            called['new_chart'] = True

        def mocked_run_settings_menu():
            if 'run_settings_menu' not in called_function:
                raise ValueError('This function should not have been called.')
            called['run_settings_menu'] = True

        monkeypatch.setattr(main_menu, 'create_classlist', mocked_create_classlist)
        monkeypatch.setattr(main_menu, 'edit_class_data', mocked_edit_class_data)
        monkeypatch.setattr(main_menu, 'new_chart', mocked_new_chart)
        monkeypatch.setattr(main_menu, 'run_settings_menu', mocked_run_settings_menu)

        invalid_inputs = ['',  # No input, return pressed.
                          ' ',  # Space/blank input.
                          'slightly_silly',  # Bad string input.
                          '0',  # Zero input.
                          '1.0'  # Float of valid input.
                          '-2',  # Negative valid option input.
                          '99',  # Out of range int input.
                          ]
        with patch('builtins.input', side_effect=list(invalid_inputs + valid_input)):
            assert take_main_menu_input() is returned_value
        # Ensure function called, if expected:
        assert called[called_function]


class TestRunMainMenu:
    def test_run_main_menu(self, monkeypatch):
        called = {'main_menu_options_mock': False, 'welcome_blurb_mock': False}

        def mocked_main_menu_options():
            called['main_menu_options_mock'] = True

        def mocked_welcome_blurb():
            called['welcome_blurb_mock'] = True

        monkeypatch.setattr(main_menu, 'main_menu_options', mocked_main_menu_options)
        monkeypatch.setattr(main_menu, 'welcome_blurb', mocked_welcome_blurb)

        mocked_take_main_menu_input_returns = [None, None, True]  # 2 mock feature calls, call to quit.
        with patch('dionysus_app.UI_menus.main_menu.take_main_menu_input',
                   side_effect=list(mocked_take_main_menu_input_returns)):
            assert run_main_menu() is None

        assert all([called[func] for func in called])
