"""Tests for settings_functions_UI.py"""
from pathlib import Path
from unittest.mock import patch

import pytest

from dionysus_app.UI_menus import settings_functions_UI
from dionysus_app.UI_menus.settings_functions_UI import (display_database_backend_options,
                                                         get_user_choice_to_set_location,
                                                         take_database_choice_input,
                                                         user_decides_to_set_database_backend,
                                                         user_decides_to_set_default_location,
                                                         user_set_chart_save_folder,
                                                         user_set_database_backend,
                                                         welcome_set_default_location_message,
                                                         welcome_to_program,
                                                         )


class TestWelcomeToProgram:
    def test_welcome_to_program(self, capsys):
        assert welcome_to_program() is None
        # Check message output contains keyword.
        assert 'welcome' in capsys.readouterr().out.lower()


class TestWelcomeSetDefaultLocationMessage:
    def test_app_start_set_default_chart_save_location_user_set(self, capsys):
        assert welcome_set_default_location_message() is None
        # Check message output contains keyword.
        assert 'default location' in capsys.readouterr().out.lower()


class TestGetUserChoiceToSetLocation:
    @pytest.mark.parametrize(
        'mocked_input, expected_return_value',
        [('y', True),  # affirmative_inputs
         ('Y', True),
         ('yes', True),
         ('Yes', True),
         ('YES', True),
         ('yEs', True),
         ('YeS', True),
         # negative_inputs
         ('', False),  # Blank input/user hits return without input.
         (' ', False),
         ('  ', False),
         ('n', False),
         ('N', False),
         ('No', False),
         ('NO', False),
         ('No thanks', False),
         ('Your mother was an hamster', False),
         ])
    def test_get_user_choice_to_set_location(self, monkeypatch,
                                             mocked_input, expected_return_value):
        with patch('builtins.input', side_effect=[mocked_input]):
            # Mocked input string placed inside a list because otherwise it is read one char at a time.
            assert get_user_choice_to_set_location() is expected_return_value


class TestUserDecidesToSetDefaultLocation:
    @pytest.mark.parametrize('user_choice', [True, False])
    def test_user_decides_to_set_default_location(self, monkeypatch,
                                                  user_choice):
        monkeypatch.setattr(settings_functions_UI, 'welcome_set_default_location_message', lambda: None)
        monkeypatch.setattr(settings_functions_UI, 'get_user_choice_to_set_location', lambda: user_choice)
        monkeypatch.setattr(settings_functions_UI, 'clear_screen', lambda: None)

        assert user_decides_to_set_default_location() == user_choice


class TestUserSetChartSaveFolder:
    @pytest.mark.parametrize(
        'user_folder_selection, mock_APP_DEFAULT_CHART_SAVE_FOLDER, expected_return',
        [('', Path('app_default'), Path('app_default')),
         (Path('camelot'), 'app default should not be used...', Path('camelot')),
         ])
    def test_user_set_set_chart_folder_blank_input(self, monkeypatch,
                                                   user_folder_selection, mock_APP_DEFAULT_CHART_SAVE_FOLDER,
                                                   expected_return):
        monkeypatch.setattr(settings_functions_UI, 'select_folder_dialogue', lambda **args: user_folder_selection)
        monkeypatch.setattr(settings_functions_UI, 'APP_DEFAULT_CHART_SAVE_DIR', mock_APP_DEFAULT_CHART_SAVE_FOLDER)

        assert user_set_chart_save_folder() == expected_return


class TestUserDecidesToSetDatabaseBackend:
    @pytest.mark.parametrize('user_input', [True, False])
    def test_user_decides_to_set_database_backend(self, monkeypatch, user_input):
        monkeypatch.setattr(settings_functions_UI, 'ask_user_bool', lambda **args: user_input)

        assert user_decides_to_set_database_backend() is user_input


class TestUserSetDatabaseBackend:
    @pytest.mark.parametrize('user_input', ['database chosen', False])
    def test_user_set_database_backend(self, monkeypatch, user_input):
        monkeypatch.setattr(settings_functions_UI, 'take_database_choice_input', lambda: user_input)

        assert user_set_database_backend() is user_input


class TestDisplayDatabaseBackendOptions:
    def test_display_database_backend_options(self, capsys):
        assert display_database_backend_options() is None
        # Check message output contains keyword.
        assert 'database backend' in capsys.readouterr().out.lower()


class TestTakeDatabaseChoiceInput:
    @pytest.mark.parametrize(
        'mocked_input, expected_return_value',
        [('1', 'JSON'),  # Choose option
         (('invalid input', '0'), False),  # Invalid input, then cancel.
         ('0', False),
         ])
    def test_take_database_choice_input(self, mocked_input, expected_return_value):
        with patch('builtins.input', side_effect=list(mocked_input)):
            assert take_database_choice_input() == expected_return_value
