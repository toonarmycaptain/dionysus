"""Test settings_menu."""
import pytest

from unittest.mock import patch

from dionysus_app.UI_menus import settings_menu
from dionysus_app.UI_menus.settings_menu import (call_set_database_backend,
                                                 call_set_default_chart_save_location,
                                                 return_to_main_menu,
                                                 run_settings_menu,
                                                 settings_menu_options,
                                                 take_settings_menu_input,
                                                 )


class TestRunSettingsMenu:
    def test_run_settings_menu(self, monkeypatch):
        input_calls = (action for action in [None, None, True])

        def mocked_take_settings_menu_input():
            return next(input_calls)

        monkeypatch.setattr(settings_menu, 'settings_menu_options', lambda: None)
        monkeypatch.setattr(settings_menu, 'take_settings_menu_input', mocked_take_settings_menu_input)

        assert run_settings_menu() is None
        # Ensure all actions were taken and loop did not exit early:
        with pytest.raises(StopIteration):
            mocked_take_settings_menu_input()


class TestSettingsMenuOptions:
    def test_settings_menu_options(self, capsys):
        assert settings_menu_options() is None
        # Keyword check:
        assert 'Settings' in capsys.readouterr().out


class TestTakeSettingsMenuInput:
    @pytest.mark.parametrize(
        'valid_input, called_function, returned_value',
        [(['1'], 'call_set_default_chart_save_location', None),
         (['2'], 'call_set_database_backend', None),
         (['0'], None, True),  # Return to menu without choosing option, None as no function called.
         pytest.param(['1'], 'call_set_database_backend', None,
                      marks=pytest.mark.xfail(reason='Wrong function called.')),
         pytest.param(['2'], '', True,
                      marks=pytest.mark.xfail(reason='Function not called.')),
         pytest.param(['0'], 'call_set_default_chart_save_location', True,
                      marks=pytest.mark.xfail(reason='Return to menu, function not called.')),
         ])
    def test_take_settings_menu_input(self, monkeypatch,
                                      valid_input, called_function, returned_value):
        called = {called_function: False}  # Initialise called_function as False ie not called.
        called[None] = True  # Initialise None=True: None won't be called (reset None=True if called_function is None).

        # Monkeypatched functions ensure correct function was called:
        def mocked_call_set_default_chart_save_location():
            if 'call_set_default_chart_save_location' not in called_function:
                raise ValueError('This function should not have been called')
            called['call_set_default_chart_save_location'] = True

        def mocked_call_set_database_backend():
            if 'call_set_database_backend' not in called_function:
                raise ValueError('This function should not have been called')
            called['call_set_database_backend'] = True

        monkeypatch.setattr(settings_menu, 'call_set_default_chart_save_location',
                            mocked_call_set_default_chart_save_location)
        monkeypatch.setattr(settings_menu, 'call_set_database_backend', mocked_call_set_database_backend)

        invalid_inputs = ['',  # No input, return pressed.
                          ' ',  # Space/blank input.
                          'slightly_silly',  # Bad string input.
                          '1.0'  # Float of valid input.
                          '-2',  # Negative valid option input.
                          '99',  # Out of range int input.
                          ]
        with patch('builtins.input', side_effect=list(invalid_inputs + valid_input)):
            assert take_settings_menu_input() is returned_value
        # Ensure function called, if expected:
        assert called[called_function]


class TestCallSetDefaultChartSaveLocation:
    def test_call_set_default_chart_save_location(self, monkeypatch):
        def mocked_set_default_chart_save_location(user_set):
            if not user_set:
                raise ValueError('user_set should be True')

        monkeypatch.setattr(settings_menu, 'set_default_chart_save_location', mocked_set_default_chart_save_location)
        assert call_set_default_chart_save_location() is None


class TestCallSetDatabaseBackend:
    def test_call_set_database_backend(self, capsys):
        assert call_set_database_backend() is None
        # Keyword check:
        assert 'not yet implemented' in capsys.readouterr().out


class TestReturnToMainMenu:
    def test_return_to_main_menu(self, capsys):
        assert return_to_main_menu() is False
        # Keyword checks:
        assert 'return' in capsys.readouterr().out.lower()
