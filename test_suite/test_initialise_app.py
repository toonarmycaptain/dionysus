import pytest

from pathlib import Path

from dionysus_app import data_folder, initialise_app
from dionysus_app.initialise_app import (app_config,
                                         data_folder_check,
                                         app_init,
                                         )


class TestAppConfig:
    def test_app_config_no_settings_file(self, monkeypatch):
        def mocked_path_exists(path):
            return False

        def mocked_app_start_set_default_chart_save_location():
            pass

        monkeypatch.setattr(initialise_app.Path, 'exists', mocked_path_exists)
        monkeypatch.setattr(initialise_app, 'app_start_set_default_chart_save_location',
                            mocked_app_start_set_default_chart_save_location)
        assert app_config() is None

    def test_app_config_settings_file_exists(self, monkeypatch):
        def mocked_path_exists(path):
            return True

        def mocked_app_start_set_default_chart_save_location():
            raise ValueError('Should not be called if settings file exists.')

        monkeypatch.setattr(initialise_app.Path, 'exists', mocked_path_exists)
        monkeypatch.setattr(initialise_app, 'app_start_set_default_chart_save_location', mocked_app_start_set_default_chart_save_location)

        assert app_config() is None


class TestDataFolderCheck:
    @pytest.mark.parametrize(
        'default_path',
        [r'./dionysus_app/app_data',
         r'./dionysus_app/app_data/class_data',
         r'./dionysus_app/app_data/temp'
         ])
    def test_data_folder_check_default(self, monkeypatch, tmpdir,
                                       default_path):
        monkeypatch.setattr(data_folder, 'ROOT_DIR', tmpdir)
        assert data_folder_check() is None
        assert Path(tmpdir, default_path).exists()


class TestAppInit:
    def test_app_init(self, monkeypatch):
        data_folder_check_mock, app_config_mock = {'called': False}, {'called': False}

        def mocked_data_folder_check():
            data_folder_check_mock['called'] = True

        def mocked_app_config():
            app_config_mock['called'] = True

        monkeypatch.setattr(initialise_app, 'app_config', mocked_app_config)
        monkeypatch.setattr(initialise_app, 'data_folder_check', mocked_data_folder_check)

        assert app_init() is None
        assert data_folder_check_mock['called'] and app_config_mock['called']
