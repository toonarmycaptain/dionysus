import unittest
import os
from app_main import generate_rel_path, data_folder_check


class TestAppMain(unittest.TestCase):

    def setUp(self):
        self.default_paths = [
            r'/dionysus_app/app_data',
            r'/dionysus_app/app_data/class_data',
            r'dionysus_app/app_data/image_data'
        ]

    def test_generate_data_path_defaults(self):

        os.chdir(os.path.join(os.getcwd(), '..'))
        for path in self.default_paths:

            path_result = generate_rel_path(path)
            assert path in path_result and os.getcwd() in path_result

    def test_generate_data_path_None(self):
        path_result = generate_rel_path(None)
        assert os.getcwd() in path_result


    def test_data_folder_check_default(self):
        default_paths = [
            r'/dionysus_app/app_data',
            r'/dionysus_app/app_data/class_data',
            r'dionysus_app/app_data/image_data'
        ]
        data_folder_check()
        for path in default_paths:
            data_folder_path = generate_rel_path(path)
            assert os.path.exists(data_folder_path)
