"""Test settings functions.py"""
import os

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, mock_open

from dionysus_app.settings_functions import (APP_SETTINGS_FILE,
                                             app_start_set_default_chart_save_location,
                                             create_app_data__init__,
                                             create_app_settings_file,
                                             create_chart_save_folder,
                                             edit_app_settings_file,
                                             load_chart_save_folder,
                                             move_chart_save_folder,
                                             save_new_default_chart_save_location_setting,
                                             set_default_chart_save_location,
                                             write_settings_to_file,
                                             )


class TestAppStartSetDefaultChartSaveLocation(TestCase):
    @patch('dionysus_app.settings_functions.set_default_chart_save_location')
    @patch('dionysus_app.settings_functions.user_decides_to_set_default_location')
    def test_app_start_set_default_chart_save_location_user_set(
            self,
            mocked_user_decides_to_set_default_location,
            mocked_set_default_chart_save_location,
    ):
        mocked_user_decides_to_set_default_location.return_value = True

        assert app_start_set_default_chart_save_location() is None

        mocked_user_decides_to_set_default_location.assert_called_once_with()
        mocked_set_default_chart_save_location.assert_called_once_with(
            user_set=mocked_user_decides_to_set_default_location.return_value)

    @patch('dionysus_app.settings_functions.set_default_chart_save_location')
    @patch('dionysus_app.settings_functions.user_decides_to_set_default_location')
    def test_app_start_set_default_chart_save_location_app_set(
            self,
            mocked_user_decides_to_set_default_location,
            mocked_set_default_chart_save_location,
    ):
        mocked_user_decides_to_set_default_location.return_value = False

        assert app_start_set_default_chart_save_location() is None

        mocked_user_decides_to_set_default_location.assert_called_once_with()
        mocked_set_default_chart_save_location.assert_called_once_with(
            user_set=mocked_user_decides_to_set_default_location.return_value)


class TestSetDefaultChartSaveLocation(TestCase):
    mocked_APP_DEFAULT_CHART_SAVE_FOLDER = Path('app_default')
    mocked_DEFAULT_CHART_SAVE_FOLDER = Path('set_default_location')
    mocked_CHART_SAVE_FOLDER_NAME = 'art_gallery'

    def setUp(self):
        # Preset app default
        self.mocked_APP_DEFAULT_CHART_SAVE_FOLDER = Path('app_default')
        # Location in settings
        self.mocked_DEFAULT_CHART_SAVE_FOLDER = Path('set_default_location')
        self.mocked_CHART_SAVE_FOLDER_NAME = 'art_gallery'

        self.app_default_chart_save_folder_path = Path(self.mocked_APP_DEFAULT_CHART_SAVE_FOLDER,
                                                       self.mocked_CHART_SAVE_FOLDER_NAME)

        self.user_supplied_location = r'britain\camelot\not_some_french_guys_house'
        self.user_set_location_fullpath = Path(self.user_supplied_location, self.mocked_CHART_SAVE_FOLDER_NAME)

    @patch('dionysus_app.settings_functions.APP_DEFAULT_CHART_SAVE_FOLDER', mocked_APP_DEFAULT_CHART_SAVE_FOLDER)
    @patch('dionysus_app.settings_functions.CHART_SAVE_FOLDER_NAME', mocked_CHART_SAVE_FOLDER_NAME)
    @patch('dionysus_app.settings_functions.definitions.DEFAULT_CHART_SAVE_FOLDER', mocked_DEFAULT_CHART_SAVE_FOLDER)
    @patch('dionysus_app.settings_functions.create_chart_save_folder')
    @patch('dionysus_app.settings_functions.save_new_default_chart_save_location_setting')
    @patch('dionysus_app.settings_functions.user_set_chart_save_folder')
    def test_set_default_chart_save_location_user_set_false(self,
                                                            mocked_user_set_chart_save_folder,
                                                            mocked_save_new_default_chart_save_location_setting,
                                                            mocked_create_chart_save_folder,
                                                            ):
        assert set_default_chart_save_location(False) is None

        mocked_user_set_chart_save_folder.assert_not_called()
        mocked_save_new_default_chart_save_location_setting.assert_called_once_with(
            self.app_default_chart_save_folder_path)
        mocked_create_chart_save_folder.assert_called_once_with(self.app_default_chart_save_folder_path,
                                                                self.mocked_DEFAULT_CHART_SAVE_FOLDER)

    @patch('dionysus_app.settings_functions.APP_DEFAULT_CHART_SAVE_FOLDER', mocked_APP_DEFAULT_CHART_SAVE_FOLDER)
    @patch('dionysus_app.settings_functions.CHART_SAVE_FOLDER_NAME', mocked_CHART_SAVE_FOLDER_NAME)
    @patch('dionysus_app.settings_functions.definitions')
    @patch('dionysus_app.settings_functions.create_chart_save_folder')
    @patch('dionysus_app.settings_functions.save_new_default_chart_save_location_setting')
    @patch('dionysus_app.settings_functions.user_set_chart_save_folder')
    def test_set_default_chart_save_location_user_set_true_location_supplied(
            self,
            mocked_user_set_chart_save_folder,
            mocked_save_new_default_chart_save_location_setting,
            mocked_create_chart_save_folder,
            mocked_definitions):
        mocked_definitions.DEFAULT_CHART_SAVE_FOLDER = self.mocked_DEFAULT_CHART_SAVE_FOLDER
        mocked_user_set_chart_save_folder.return_value = self.user_supplied_location
        assert set_default_chart_save_location(True) is None

        mocked_user_set_chart_save_folder.assert_called_once_with()
        mocked_save_new_default_chart_save_location_setting.assert_called_once_with(
            self.user_set_location_fullpath)
        mocked_create_chart_save_folder.assert_called_once_with(self.user_set_location_fullpath,
                                                                self.mocked_DEFAULT_CHART_SAVE_FOLDER)
        assert mocked_definitions.DEFAULT_CHART_SAVE_FOLDER == self.user_set_location_fullpath

    @patch('dionysus_app.settings_functions.APP_DEFAULT_CHART_SAVE_FOLDER', mocked_APP_DEFAULT_CHART_SAVE_FOLDER)
    @patch('dionysus_app.settings_functions.CHART_SAVE_FOLDER_NAME', mocked_CHART_SAVE_FOLDER_NAME)
    @patch('dionysus_app.settings_functions.definitions')
    @patch('dionysus_app.settings_functions.create_chart_save_folder')
    @patch('dionysus_app.settings_functions.save_new_default_chart_save_location_setting')
    @patch('dionysus_app.settings_functions.user_set_chart_save_folder')
    def test_set_default_chart_save_location_user_set_true_no_location_supplied(
            self,
            mocked_user_set_chart_save_folder,
            mocked_save_new_default_chart_save_location_setting,
            mocked_create_chart_save_folder,
            mocked_definitions):
        mocked_definitions.DEFAULT_CHART_SAVE_FOLDER = self.mocked_DEFAULT_CHART_SAVE_FOLDER
        mocked_user_set_chart_save_folder.return_value = self.mocked_APP_DEFAULT_CHART_SAVE_FOLDER
        assert set_default_chart_save_location(True) is None

        mocked_user_set_chart_save_folder.assert_called_once_with()
        mocked_save_new_default_chart_save_location_setting.assert_called_once_with(
            self.app_default_chart_save_folder_path)
        mocked_create_chart_save_folder.assert_called_once_with(self.app_default_chart_save_folder_path,
                                                                self.mocked_DEFAULT_CHART_SAVE_FOLDER)
        assert mocked_definitions.DEFAULT_CHART_SAVE_FOLDER == self.app_default_chart_save_folder_path


class TestCreateChartSaveFolder(TestCase):
    def setUp(self):
        self.test_original_location = 'mock_location'
        self.test_new_location = 'mock_new_location'

    @patch('dionysus_app.settings_functions.move_chart_save_folder')
    @patch('dionysus_app.settings_functions.Path')
    def test_create_chart_save_folder_test_correct_argument_passed_to_path(self,
                                                                           mocked_path,
                                                                           mocked_move_chart_save_folder,
                                                                           ):
        """Mocking call to path and mkdir method on Path class didn't work."""
        assert create_chart_save_folder(self.test_new_location) is None

        mocked_move_chart_save_folder.assert_not_called()
        mocked_path.assert_called_once_with(self.test_new_location)

    @patch('dionysus_app.settings_functions.move_chart_save_folder')
    @patch('dionysus_app.settings_functions.Path.mkdir')
    def test_create_chart_save_folder_no_original(self,
                                                  mocked_mkdir,
                                                  mocked_move_chart_save_folder,
                                                  ):
        assert create_chart_save_folder(self.test_new_location) is None

        mocked_move_chart_save_folder.assert_not_called()
        mocked_mkdir.assert_called_once_with(exist_ok=True, parents=True)

    @patch('dionysus_app.settings_functions.move_chart_save_folder')
    @patch('dionysus_app.settings_functions.Path.mkdir')
    def test_create_chart_save_folder_original_exists(self,
                                                      mocked_mkdir,
                                                      mocked_move_chart_save_folder,
                                                      ):
        assert create_chart_save_folder(self.test_new_location,
                                        self.test_original_location) is None

        mocked_move_chart_save_folder.assert_called_once_with(self.test_original_location,
                                                              Path(self.test_new_location))
        mocked_mkdir.assert_called_once_with(exist_ok=True, parents=True)


class TestMoveChartSaveFolder(TestCase):
    def setUp(self):
        self.test_original_location = 'mock_location'
        self.test_new_location = 'mock_new_location'

    @patch('dionysus_app.settings_functions.Path')
    def test_move_chart_save_folder_path_called_on_correct_argument(self,
                                                                    mocked_path,
                                                                    ):
        """Mocking call to path and mkdir method on Path class didn't work."""
        assert move_chart_save_folder(self.test_original_location,
                                      self.test_new_location) is None

        mocked_path.assert_called_once_with(self.test_original_location)

    @patch('dionysus_app.settings_functions.move_file')
    @patch('dionysus_app.settings_functions.Path.exists')
    def test_move_chart_save_folder_original_nonexistent(self,
                                                         mocked_path_exists,
                                                         mocked_move_file,
                                                         ):
        mocked_path_exists.return_value = False

        assert move_chart_save_folder(self.test_original_location,
                                      self.test_new_location) is None

        mocked_move_file.assert_not_called()

    @patch('dionysus_app.settings_functions.move_file')
    @patch('dionysus_app.settings_functions.Path.exists')
    def test_move_chart_save_folder_original_existent(self,
                                                      mocked_path_exists,
                                                      mocked_move_file,
                                                      ):
        mocked_path_exists.return_value = True

        assert move_chart_save_folder(self.test_original_location,
                                      self.test_new_location) is None

        mocked_move_file.assert_called_once_with(self.test_original_location,
                                                 self.test_new_location)


class TestSaveNewDefaultChartSaveLocationSetting(TestCase):
    def setUp(self):
        self.test_new_location = Path(r'camelot\holy_grail')
        self.test_new_setting_dict = {'user_default_chart_save_folder': str(self.test_new_location)}

    @patch('dionysus_app.settings_functions.edit_app_settings_file')
    def test_save_new_default_chart_save_location_setting(self,
                                                          mocked_edit_app_settings_file):
        assert save_new_default_chart_save_location_setting(self.test_new_location) is None

        mocked_edit_app_settings_file.assert_called_once_with(self.test_new_setting_dict)


class TestWriteSettingsToFile(TestCase):
    mock_APP_SETTINGS_FILE = Path(r'rome\camelot\king_of_britons_castle')

    def setUp(self):
        self.mock_APP_SETTINGS_FILE = Path(r'rome\camelot\king_of_britons_castle')

        self.test_settings_dict = {'knight': 'sir lancelot'}
        self.test_settings_write_str = 'dionysus_settings = ' + str(self.test_settings_dict)

    @patch('dionysus_app.settings_functions.APP_SETTINGS_FILE', mock_APP_SETTINGS_FILE)
    def test_write_settings_to_file(self):
        with patch('dionysus_app.settings_functions.open', mock_open(read_data=None)) as mocked_open:
            assert write_settings_to_file(self.test_settings_dict) is None

            mocked_open.assert_called_once_with(self.mock_APP_SETTINGS_FILE, 'w+')
            mocked_settings_file = mocked_open()
            mocked_settings_file.write.assert_called_once_with(self.test_settings_write_str)


class TestCreateAppSettingsFile(TestCase):
    def setUp(self):
        self.default_blank_settings_dict = {}
        self.test_settings_dict = {'system of government': 'Strange women lying in ponds distributing swords.'}

    @patch('dionysus_app.settings_functions.write_settings_to_file')
    @patch('dionysus_app.settings_functions.create_app_data__init__')
    def test_create_app_settings_file_no_settings_dict(self,
                                                       mocked_create_app_data__init__,
                                                       mocked_write_settings_to_file
                                                       ):
        assert create_app_settings_file() is None

        mocked_create_app_data__init__.assert_called_once_with()
        mocked_write_settings_to_file.assert_called_once_with(self.default_blank_settings_dict)

        # Check default settings argument passed to write_settings_to_file is a dict:
        # call_args_list[first call][positional args][first positional arg]
        assert isinstance(mocked_write_settings_to_file.call_args_list[0][0][0], dict)

    @patch('dionysus_app.settings_functions.write_settings_to_file')
    @patch('dionysus_app.settings_functions.create_app_data__init__')
    def test_create_app_settings_file_with_settings_dict(self,
                                                         mocked_create_app_data__init__,
                                                         mocked_write_settings_to_file
                                                         ):
        assert create_app_settings_file(self.test_settings_dict) is None

        mocked_create_app_data__init__.assert_called_once_with()
        mocked_write_settings_to_file.assert_called_once_with(self.test_settings_dict)


class TestCreateAppDataInit(TestCase):
    mock_APP_DATA = Path(r'all\the\data')

    def setUp(self):
        self.mock_APP_DATA = Path(r'all\the\data')

        self.test_init_py_filename = '__init__.py'
        self.test_init_py_path = os.path.join(self.mock_APP_DATA, self.test_init_py_filename)

        self.test_init_py_write_string = '"""__init__.py so that settings.py may be imported."""'

    @patch('dionysus_app.settings_functions.APP_DATA', mock_APP_DATA)
    def test_create_app_data__init__(self):
        with patch('dionysus_app.settings_functions.open', mock_open(read_data=None)) as mocked_open:
            assert create_app_data__init__() is None

            mocked_open.assert_called_once_with(self.test_init_py_path, 'w+')
            mocked_settings_file = mocked_open()
            mocked_settings_file.write.assert_called_once_with(self.test_init_py_write_string)


class TestEditAppSettingsFile(TestCase):
    mock_APP_SETTINGS_FILE = Path(r'rome\camelot\king_of_britons_castle')
    mock_dionysus_settings = {'user_default_chart_save_folder': r'some\path'}

    def setUp(self):
        self.mock_APP_SETTINGS_FILE = Path(r'rome\camelot\king_of_britons_castle')
        self.mock_dionysus_settings = {'user_default_chart_save_folder': r'some\path'}

        self.test_new_settings = {'my_new_setting': 'some setting'}
        self.new_dionysus_settings_write = {**self.mock_dionysus_settings, **self.test_new_settings}

        # Create file such that mocking it does not fail.
        if not Path.exists(APP_SETTINGS_FILE):
            self.created_app_settings = True
            create_app_settings_file()
        else:
            self.created_app_settings = False

    @patch('dionysus_app.app_data.settings.dionysus_settings', mock_dionysus_settings)
    @patch('dionysus_app.settings_functions.APP_SETTINGS_FILE', mock_APP_SETTINGS_FILE)
    @patch('dionysus_app.settings_functions.write_settings_to_file')
    @patch('dionysus_app.settings_functions.create_app_settings_file')
    @patch('dionysus_app.settings_functions.Path.exists')
    def test_edit_app_settings_file_no_settings_file(self,
                                                     mock_path_exists,
                                                     mock_create_app_settings_file,
                                                     mock_write_settings_to_file,
                                                     ):
        mock_path_exists.return_value = False

        assert edit_app_settings_file(self.test_new_settings) is None

        mock_path_exists.assert_called_once_with(self.mock_APP_SETTINGS_FILE)
        # New settings file is created.
        mock_create_app_settings_file.assert_called_once_with()

        mock_write_settings_to_file.assert_called_once_with(self.new_dionysus_settings_write)

    @patch('dionysus_app.app_data.settings.dionysus_settings', mock_dionysus_settings)
    @patch('dionysus_app.settings_functions.APP_SETTINGS_FILE', mock_APP_SETTINGS_FILE)
    @patch('dionysus_app.settings_functions.write_settings_to_file')
    @patch('dionysus_app.settings_functions.create_app_settings_file')
    @patch('dionysus_app.settings_functions.Path.exists')
    def test_edit_app_settings_file_existent_settings_file(self,
                                                           mock_path_exists,
                                                           mock_create_app_settings_file,
                                                           mock_write_settings_to_file,
                                                           ):
        mock_path_exists.return_value = True

        assert edit_app_settings_file(self.test_new_settings) is None

        mock_path_exists.assert_called_once_with(self.mock_APP_SETTINGS_FILE)
        # New settings file is not created.
        mock_create_app_settings_file.assert_not_called()

        mock_write_settings_to_file.assert_called_once_with(self.new_dionysus_settings_write)

    def tearDown(self):
        # Remove settings file if created for test.
        if self.created_app_settings:
            os.remove(APP_SETTINGS_FILE)


class TestLoadChartSaveFolder(TestCase):
    mock_dionysus_settings = {'user_default_chart_save_folder': r'some\path'}

    def setUp(self):
        self.mock_dionysus_settings = {'user_default_chart_save_folder': r'some\path'}

        self.test_load_chart_save_folder_return = Path(self.mock_dionysus_settings['user_default_chart_save_folder'])

        # Create file such that mocking it does not fail.
        if not Path.exists(APP_SETTINGS_FILE):
            self.created_app_settings = True
            create_app_settings_file()
        else:
            self.created_app_settings = False

    @patch('dionysus_app.app_data.settings.dionysus_settings', mock_dionysus_settings)
    def test_load_chart_save_folder(self):
        assert load_chart_save_folder() == self.test_load_chart_save_folder_return

    def tearDown(self):
        # Remove settings file if created for test.
        if self.created_app_settings:
            os.remove(APP_SETTINGS_FILE)
