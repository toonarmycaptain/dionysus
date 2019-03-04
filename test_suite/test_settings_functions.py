"""Test settings functions.py"""
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from dionysus_app.settings_functions import (app_start_set_default_chart_save_location,
                                             create_chart_save_folder,
                                             move_chart_save_folder,
                                             set_default_chart_save_location,
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
        assert mocked_definitions.DEFAULT_CHART_SAVE_FOLDER == str(self.user_set_location_fullpath)

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
        assert mocked_definitions.DEFAULT_CHART_SAVE_FOLDER == str(self.app_default_chart_save_folder_path)


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
