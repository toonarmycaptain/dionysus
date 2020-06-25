import os

import pytest

from pathlib import Path

from definitions import ROOT_DIR
from dionysus_app.data_folder import DataFolder


class TestDataFolder:
    @pytest.mark.parametrize('relative_path_str',
                             [r'/dionysus_app',
                              r'/dionysus_app/app_data',
                              r'/dionysus_app/app_data/temp',
                              r'/dionysus_app/app_data/settings.py',
                              r'/dionysus_app/chart_generator',
                              r'/dionysus_app/chart_generator/default_avatar.png',
                              ])
    def test_generate_data_path_defaults(self, relative_path_str):
        """Key app relative paths returned as full paths."""
        os.chdir(ROOT_DIR)
        cwd_path = Path.cwd()
        path_result = DataFolder.generate_rel_path(relative_path_str)

        # Assert relative app paths in generated absolute paths:
        assert relative_path_str in path_result.as_uri()
        # Assert cwd in generated absolute paths:
        # Use .lower() to avoid casing issue (eg Windows user capitalised in cwd_path but not path_result).
        assert cwd_path.as_uri().lower() in path_result.as_uri().lower()

    @pytest.mark.parametrize('DataFolder_attr, relative_path_str',
                             [(DataFolder.APP.value, r'/dionysus_app'),
                              (DataFolder.APP_DATA.value, r'/dionysus_app/app_data'),
                              (DataFolder.TEMP_DIR.value, r'/dionysus_app/app_data/temp'),
                              (DataFolder.APP_SETTINGS.value, r'/dionysus_app/app_data/settings.py'),
                              (DataFolder.CHART_GENERATOR.value, r'/dionysus_app/chart_generator'),
                              (DataFolder.DEFAULT_AVATAR.value, r'/dionysus_app/chart_generator/default_avatar.png'),
                              ])
    def test_generate_data_path_defaults_dot_value(self, DataFolder_attr, relative_path_str):
        """DataFolder attrs generate full paths."""
        os.chdir(ROOT_DIR)
        cwd_path = Path.cwd()

        # path_result = DataFolder.generate_rel_path(DataFolder.attr.value)
        path_result = DataFolder.generate_rel_path(DataFolder_attr)

        assert path_result == cwd_path.joinpath(DataFolder_attr)

        # Assert relative app paths in generated absolute paths:
        assert relative_path_str in path_result.as_uri()
        # Assert cwd in generated absolute paths:
        # Use .lower() to avoid casing issue (eg Windows user capitalised in cwd_path but not path_result).
        assert cwd_path.as_uri().lower() in path_result.as_uri().lower()


    def test_generate_data_path_None(self):
        """Passing None returns current working directory."""
        assert DataFolder.generate_rel_path(None) == Path.cwd()
