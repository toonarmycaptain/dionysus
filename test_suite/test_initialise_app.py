import os
import unittest
from dionysus_app.initialise_app import data_folder_check
from dionysus_app.data_folder import DataFolder


class TestAppMain(unittest.TestCase):

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
