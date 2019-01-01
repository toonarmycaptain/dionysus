import os
import unittest
from pathlib import Path
from dionysus_app.data_folder import DataFolder


class TestDataFolder(unittest.TestCase):

    def setUp(self):
        self.default_paths = [
            r'/dionysus_app'  
            r'/dionysus_app/app_data',
            r'/dionysus_app/app_data/class_data',
            r'/dionysus_app/app_data/class/registry.index',
            r'/dionysus_app/app_data/settings.py',
            r'/dionysus_app/chart_generator',
            r'/dionysus_app/chart_generator/default_avatar.png',
        ]

    def test_generate_data_path_defaults(self):
        os.chdir(os.path.join(os.getcwd(), '..'))
        cwd_path = Path.cwd().as_uri()  # cwd path OS agnostic for assertion
        for path in self.default_paths:
            path_result = DataFolder.generate_rel_path(path).as_uri()
            assert path in path_result and cwd_path in path_result

    def test_generate_data_path_None(self):
        path_result = DataFolder.generate_rel_path(None)
        cwd_path = Path.cwd().as_uri()  # cwd path OS agnostic for assertion
        assert cwd_path in path_result
