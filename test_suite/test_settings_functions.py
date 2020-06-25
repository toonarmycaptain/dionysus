"""Test settings functions.py"""
import pytest

from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

import definitions

from dionysus_app import settings_functions
from dionysus_app.settings_functions import (APP_DATA,
                                             APP_SETTINGS_FILE,
                                             app_start_set_database,
                                             app_start_set_default_chart_save_location,
                                             create_app_data__init__,
                                             create_app_settings_file,
                                             create_chart_save_folder,
                                             edit_app_settings_file,
                                             load_chart_save_folder,
                                             move_chart_save_folder,
                                             save_new_default_chart_save_location_setting,
                                             set_database_backend,
                                             set_default_chart_save_location,
                                             write_settings_to_file,
                                             )


class TestAppStartSetDefaultChartSaveLocation:
    @pytest.mark.parametrize('user_setting_location', [True, False])
    def test_app_start_set_default_chart_save_location(self, monkeypatch,
                                                       user_setting_location):
        def mocked_set_default_chart_save_location(user_set):
            if user_set is not user_setting_location:
                raise ValueError('Flag for user setting location is incorrect.')

        monkeypatch.setattr(settings_functions, 'user_decides_to_set_default_location', lambda: user_setting_location)
        monkeypatch.setattr(settings_functions, 'set_default_chart_save_location',
                            mocked_set_default_chart_save_location)

        assert app_start_set_default_chart_save_location() is None


class TestSetDefaultChartSaveLocation:
    @pytest.mark.parametrize('user_setting_location, user_supplied_location',
                             [(False, False),
                              (True, Path('a user set this location')),  # User provides location
                              (True, False),  # User does not provide location
                              ])
    def test_set_default_chart_save_location(self, monkeypatch,
                                             user_setting_location, user_supplied_location):

        def mocked_user_set_chart_save_folder():
            if not user_setting_location:
                raise ValueError('Should not be called if user input is not expected.')
            # On no user input, function returns the app default.
            return user_supplied_location or settings_functions.APP_DEFAULT_CHART_SAVE_DIR

        def mocked_save_new_default_chart_save_location_setting(new_chart_save_folder_path):
            if new_chart_save_folder_path != test_new_chart_save_location:
                raise ValueError(f'Wrong new location path: '
                                 f'{new_chart_save_folder_path=}!={test_new_chart_save_location}')

        def mocked_create_chart_save_folder(new_chart_save_folder_path, original_location):
            if new_chart_save_folder_path != test_new_chart_save_location:
                raise ValueError(f'Wrong new location path: '
                                 f'{new_chart_save_folder_path=}!={test_new_chart_save_location}')
            if original_location != test_original_chart_save_folder_location:
                raise ValueError(f'Wrong original chart save folder location: '
                                 f'{original_location}!={settings_functions.definitions.DEFAULT_CHART_SAVE_DIR}')

        # monkeypatch.setattr(settings_functions, 'APP_DEFAULT_CHART_SAVE_DIR',
        #                     Path('mock_APP_DEFAULT_CHART_SAVE_DIR'))
        monkeypatch.setattr(settings_functions, 'CHART_SAVE_DIR_NAME', 'mocked_CHART_SAVE_DIR_NAME')
        monkeypatch.setattr(settings_functions.definitions, 'DEFAULT_CHART_SAVE_DIR',
                            Path('mock_APP_DEFAULT_CHART_SAVE_DIR'))
        monkeypatch.setattr(settings_functions, 'user_set_chart_save_folder', mocked_user_set_chart_save_folder)
        monkeypatch.setattr(settings_functions, 'create_chart_save_folder', mocked_create_chart_save_folder)
        monkeypatch.setattr(settings_functions, 'save_new_default_chart_save_location_setting',
                            mocked_save_new_default_chart_save_location_setting)

        # Original chart save folder location:
        test_original_chart_save_folder_location = Path('mock_APP_DEFAULT_CHART_SAVE_DIR')
        # Pretest definitions.
        assert settings_functions.definitions.DEFAULT_CHART_SAVE_DIR == test_original_chart_save_folder_location
        # Expected new location:
        test_new_chart_save_location = Path(settings_functions.APP_DEFAULT_CHART_SAVE_DIR,
                                            settings_functions.CHART_SAVE_DIR_NAME)  # App default if no user input.
        if user_supplied_location:
            test_new_chart_save_location = Path.joinpath(user_supplied_location,
                                                         settings_functions.CHART_SAVE_DIR_NAME)

        assert set_default_chart_save_location(user_setting_location) is None
        # Runtime setting changed.
        assert settings_functions.definitions.DEFAULT_CHART_SAVE_DIR == test_new_chart_save_location


class TestAppStartSetDatabase:
    @pytest.mark.parametrize('user_setting_location', [True, False])
    def test_app_start_set_database_backend(self, monkeypatch,
                                            user_setting_location):
        def mocked_set_database_backend(user_set):
            if user_set is not user_setting_location:
                raise ValueError('Flag for user setting location is incorrect.')

        monkeypatch.setattr(settings_functions, 'user_decides_to_set_database_backend', lambda: user_setting_location)
        monkeypatch.setattr(settings_functions, 'set_database_backend', mocked_set_database_backend)

        assert app_start_set_database() is None


class TestSetDatabaseBackend:
    @pytest.mark.parametrize('user_setting_backend, user_selected_backend',
                             [(True, 'some database'),
                              (True, False),
                              (False, False),
                              ])
    def test_set_database_backend(self, monkeypatch,
                                  user_setting_backend, user_selected_backend):
        assert definitions.DATABASE is None  # Uninitialised runtime setting.

        def mocked_edit_app_settings_file(new_setting):
            assert new_setting['database'] == user_selected_backend or definitions.DEFAULT_DATABASE_BACKEND
            if new_setting['database'] != (user_selected_backend or definitions.DEFAULT_DATABASE_BACKEND):
                raise ValueError(
                    f"Wrong new setting: {new_setting['database']=} "
                    f"!= {user_selected_backend or definitions.DEFAULT_DATABASE_BACKEND=}")

        monkeypatch.setattr(settings_functions, 'user_set_database_backend', lambda: user_selected_backend)
        monkeypatch.setattr(settings_functions, 'edit_app_settings_file', mocked_edit_app_settings_file)

        assert set_database_backend(user_setting_backend) is None


class TestCreateChartSaveFolder:
    @pytest.mark.parametrize('test_original_location',
                             [None,  # No original location passed.
                              Path('some_location')  # New location.
                              ])
    def test_create_chart_save_folder(self, monkeypatch,
                                      test_original_location):
        mkdir_mock, move_chart_save_folder_mock = {'called': False}, {'called': False}
        test_new_save_folder_path = Path('somewhere else')

        def mocked_move_chart_save_folder(original_location, new_location):
            assert test_original_location  # Should not be called if no original location.
            assert (original_location, new_location) == (test_original_location, test_new_save_folder_path)
            move_chart_save_folder_mock['called'] = True

        def mocked_mkdir(path_arg, **kwargs):
            assert path_arg == test_new_save_folder_path
            assert kwargs['parents'] and kwargs['exist_ok']
            mkdir_mock['called'] = True

        monkeypatch.setattr(settings_functions, 'move_chart_save_folder', mocked_move_chart_save_folder)
        monkeypatch.setattr(settings_functions.Path, 'mkdir', mocked_mkdir)

        assert create_chart_save_folder(test_new_save_folder_path, test_original_location) is None

        assert mkdir_mock['called']  # Should always be called.
        if test_original_location:
            assert move_chart_save_folder_mock['called']
        else:
            assert not move_chart_save_folder_mock['called']


class TestMoveChartSaveFolder:
    @pytest.mark.parametrize('original_location_exists', [True, False])
    def test_move_chart_save_folder(self, monkeypatch,
                                    original_location_exists):
        test_original_save_folder_path = Path('somewhere')
        test_new_save_folder_path = Path('somewhere else')
        move_file_mock = {'called': False}

        def mocked_move_file(original_location, new_location):
            assert (original_location, new_location) == (test_original_save_folder_path, test_new_save_folder_path)
            move_file_mock['called'] = True

        monkeypatch.setattr(settings_functions.Path, 'exists', lambda path: original_location_exists)
        monkeypatch.setattr(settings_functions, 'move_file', mocked_move_file)

        assert move_chart_save_folder(test_original_save_folder_path,
                                      test_new_save_folder_path) is None

        assert move_file_mock['called'] == original_location_exists


class TestSaveNewDefaultChartSaveLocationSetting:
    def test_save_new_default_chart_save_location_setting(self, monkeypatch):
        test_new_location = Path(r'camelot\holy_grail')

        def mocked_edit_app_settings_file(chart_setting):
            assert chart_setting == {'user_default_chart_save_folder': str(test_new_location)}

        monkeypatch.setattr(settings_functions, 'edit_app_settings_file', mocked_edit_app_settings_file)

        assert save_new_default_chart_save_location_setting(test_new_location) is None


class TestWriteSettingsToFile:
    def test_write_settings_to_file(self):
        test_settings_dict = {'knight': 'sir lancelot'}

        with patch('dionysus_app.settings_functions.open', mock_open(read_data=None)) as mocked_open:
            assert write_settings_to_file(test_settings_dict) is None

            mocked_open.assert_called_once_with(APP_SETTINGS_FILE, 'w+')
            mocked_settings_file = mocked_open()
            mocked_settings_file.write.assert_called_once_with(f'dionysus_settings = {test_settings_dict}')


class TestCreateAppSettingsFile:
    @pytest.mark.parametrize(
        'new_settings_dict, dict_to_write',
        [(None, {}),  # No settings dict passed.
         ({'Knight statement': 'Ni!'}, {'Knight statement': 'Ni!'}),
         ])
    def test_create_app_settings_file(self, monkeypatch,
                                      new_settings_dict, dict_to_write):
        create_app_data__init__mock, write_settings_to_file_mock = {'called': False}, {'called': False}

        def mocked_create_app_data__init__():
            create_app_data__init__mock['called'] = True

        def mocked_write_settings_to_file(settings_dict):
            assert settings_dict == dict_to_write
            write_settings_to_file_mock['called'] = True

        monkeypatch.setattr(settings_functions, 'write_settings_to_file', mocked_write_settings_to_file)
        monkeypatch.setattr(settings_functions, 'create_app_data__init__', mocked_create_app_data__init__)

        assert create_app_settings_file(new_settings_dict) is None

        assert create_app_data__init__mock['called'] and write_settings_to_file_mock['called']


class TestCreateAppDataInit:
    def test_create_app_data__init__(self):
        with patch('dionysus_app.settings_functions.open', mock_open(read_data=None)) as mocked_open:
            assert create_app_data__init__() is None

            mocked_open.assert_called_once_with(Path(APP_DATA, '__init__.py'), 'w+')
            mocked_settings_file = mocked_open()
            mocked_settings_file.write.assert_called_once_with('"""__init__.py so that settings.py may be imported."""')


class TestEditAppSettingsFile:
    @pytest.mark.parametrize(
        'settings_file_exists, existing_settings_dict',
        [(False, {}),  # No existing settings dict, created empty dict.
         (True, {}),  # Existing empty settings dict.
         (True, {'some': 'setting'}),  # Existing setting
         (True, {'some': 'setting'}),  # Existing settings, changing setting.
         (True, {'some': 'setting', 'system of government': 'random.random'}),
         ])
    def test_edit_app_settings_file(self, monkeypatch,
                                    settings_file_exists, existing_settings_dict):
        settings_dict_to_write = {'system of government': 'Strange women lying in ponds distributing swords.'}

        def mocked_create_app_settings_file():
            assert not settings_file_exists  # Should not be called if file exists.

        def mocked_write_settings_to_file(dionysus_settings):
            assert dionysus_settings == {**existing_settings_dict, **settings_dict_to_write}

        monkeypatch.setattr(settings_functions.Path, 'exists', lambda path: settings_file_exists)
        monkeypatch.setattr(settings_functions, 'create_app_settings_file', mocked_create_app_settings_file)
        monkeypatch.setattr(settings_functions, 'write_settings_to_file', mocked_write_settings_to_file)

        # Mock out app_data/settings -> dir/package may not exist in testing.
        mocked_settings = MagicMock()
        mocked_settings.dionysus_settings = existing_settings_dict
        with patch.dict('sys.modules', {'dionysus_app.app_data.settings': mocked_settings}):
            assert edit_app_settings_file(settings_dict_to_write) is None


class TestLoadChartSaveFolder:
    @pytest.mark.parametrize('test_setting',
                             [r'some/path',  # *nix
                              r'some\path',  # Windows
                              pytest.param(None, marks=pytest.mark.xfail),
                              ])
    def test_load_chart_save_folder(self, test_setting):
        # Mock out app_data/settings -> dir/package may not exist in testing.
        mocked_settings = MagicMock()
        mocked_settings.dionysus_settings = {'user_default_chart_save_folder': test_setting}
        with patch.dict('sys.modules', {'dionysus_app.app_data.settings': mocked_settings}):
            assert load_chart_save_folder() == Path(test_setting)
