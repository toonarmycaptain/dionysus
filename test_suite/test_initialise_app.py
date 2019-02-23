import os
from unittest import TestCase
from unittest.mock import patch

from dionysus_app.data_folder import DataFolder
from dionysus_app.initialise_app import (app_config,
                                         data_folder_check,
                                         app_init,
                                         )


class TestAppConfig(TestCase):
    def setUp(self):
        pass

    @patch('dionysus_app.initialise_app.app_start_set_default_chart_save_location')
    @patch('dionysus_app.initialise_app.os.path.exists')
    def test_app_config_no_settings_file(self,
                                         mocked_os_path_exists,
                                         mocked_app_start_set_default_chart_save_location,
                                         ):
        mocked_os_path_exists.return_value = True

        assert app_config() is None

        assert mocked_app_start_set_default_chart_save_location.called_once_with()

    @patch('dionysus_app.initialise_app.app_start_set_default_chart_save_location')
    @patch('dionysus_app.initialise_app.os.path.exists')
    def test_app_config_settings_file_exists(self,
                                             mocked_os_path_exists,
                                             mocked_app_start_set_default_chart_save_location,
                                             ):
        mocked_os_path_exists.return_value = False

        assert app_config() is None

        assert mocked_app_start_set_default_chart_save_location.not_called()


class TestDataFolderCheck(TestCase):

    def setUp(self):
        self.default_paths = [
            r'./dionysus_app/app_data',
            r'./dionysus_app/app_data/class_data',
            ]

    def test_data_folder_check_default(self):
        os.chdir(os.path.join(os.getcwd(), '.'))
        data_folder_check()
        for path in self.default_paths:
            data_folder_path = DataFolder.generate_rel_path(path)
            assert os.path.exists(data_folder_path)


class TestAppInit(TestCase):
    def setUp(self):
        pass

    @patch('dionysus_app.initialise_app.app_config')
    @patch('dionysus_app.initialise_app.data_folder_check')
    def test_app_init(self,
                      mocked_data_folder_check,
                      mocked_app_config,
                      ):
        assert app_init() is None

        mocked_data_folder_check.assert_called_once_with()
        mocked_app_config.assert_called_once_with()
