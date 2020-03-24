import os

import pytest

from pathlib import Path

from dionysus_app import data_folder, initialise_app
from dionysus_app.initialise_app import (app_config,
                                         app_init,
                                         clear_temp,
                                         data_folder_check,
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
        monkeypatch.setattr(initialise_app, 'app_start_set_default_chart_save_location',
                            mocked_app_start_set_default_chart_save_location)

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


class TestClearTemp:
    def test_clear_temp_files_cleared(self, monkeypatch, tmpdir):
        test_temp_dir = Path(tmpdir, 'temp_dir')
        test_temp_dir.mkdir(parents=True)  # Make temp_dir.
        Path(test_temp_dir, 'some_dir').mkdir(parents=True)  # Make file in test_temp_dir.
        assert os.listdir(test_temp_dir)  # File in test_temp_dir.

        monkeypatch.setattr(initialise_app, 'TEMP_DIR', test_temp_dir)

        assert clear_temp() is None
        assert not test_temp_dir.exists()

    def test_clear_temp_dir_nonexistent(self, monkeypatch, tmpdir):
        test_temp_dir = Path(tmpdir, 'temp_dir')
        assert not test_temp_dir.exists()  # No temp dir.

        def mocked_rmtree(path):
            raise ValueError("rmtree should not be called temp directory doesn't exist.")

        monkeypatch.setattr(initialise_app, 'TEMP_DIR', test_temp_dir)
        monkeypatch.setattr(initialise_app.shutil, 'rmtree', mocked_rmtree)

        assert clear_temp() is None
        assert not test_temp_dir.exists()

    def test_clear_temp_no_files_not_removed(self, monkeypatch, tmpdir):
        test_temp_dir = Path(tmpdir, 'temp_dir')
        test_temp_dir.mkdir(parents=True)  # Make temp_dir
        assert not os.listdir(test_temp_dir)  # No files in test_temp_dir.

        def mocked_rmtree(path):
            raise ValueError("rmtree should not be called when no files in temp directory.")

        monkeypatch.setattr(initialise_app, 'TEMP_DIR', test_temp_dir)
        monkeypatch.setattr(initialise_app.shutil, 'rmtree', mocked_rmtree)

        assert clear_temp() is None
        assert test_temp_dir.exists()  # Directory not removed as already empty.


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
