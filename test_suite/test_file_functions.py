import os
import shutil

from unittest import TestCase

from dionysus_app.file_functions import convert_to_json, load_from_json
from dionysus_app.file_functions import copy_file, move_file
from test_suite.testing_class_data import test_load_class_data_class_data_set as test_json_class_data


class TestConvertToJson(TestCase):
    def test_convert_to_json(self):
        data_to_convert = {1: 'a', 'b': 2, 3: 'c', 'd': 4}
        json_converted_data = '{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}'

        assert convert_to_json(data_to_convert) == json_converted_data


class TestLoadFromJson(TestCase):
    def test_load_from_json(self):
        json_data_to_convert = '{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}'
        converted_json_data = {"1": 'a', 'b': 2, "3": 'c', 'd': 4}

        assert load_from_json(json_data_to_convert) == converted_json_data

    def test_load_from_json_test_class_data(self):
        assert test_json_class_data['loaded_dict'] == load_from_json(test_json_class_data['json_data_string'])


class TestCopyFile(TestCase):
    def setUp(self):
        self.original_filename = 'just_a_naughty_boy.png'
        self.new_folder_name = 'not_the_messiah'

        self.original_path = self.original_filename
        self.destination_path = os.path.join(self.new_folder_name, self.original_filename)

        with open(self.original_filename, 'w+') as good_file:
            pass

        os.mkdir(self.new_folder_name)

    def test_copy_file(self):
        assert os.path.exists(self.original_filename)
        assert not os.path.exists(self.destination_path)
        copy_file(self.original_path, self.destination_path)
        assert os.path.exists(self.destination_path)

    def tearDown(self):
        os.remove(self.original_filename)  # remove new file
        shutil.rmtree(self.new_folder_name)  # remove new dir


class TestMoveFile(TestCase):
    def setUp(self):
        self.original_filename = 'just_a_naughty_boy.png'
        self.new_folder_name = 'not_the_messiah'

        self.original_path = self.original_filename
        self.destination_path = os.path.join(self.new_folder_name, self.original_filename)

        with open(self.original_filename, 'w+') as test_file:
            pass

        os.mkdir(self.new_folder_name)

    def test_move_file(self):
        assert os.path.exists(self.original_filename)
        assert not os.path.exists(self.destination_path)
        move_file(self.original_path, self.destination_path)
        assert os.path.exists(self.destination_path)
        assert not os.path.exists(self.original_path)

    def tearDown(self):
        shutil.rmtree(self.new_folder_name)


class TestMoveDirectoryWithFileInIt(TestCase):
    def setUp(self):
        # Origin file, folder.
        self.original_filename = 'just_a_naughty_boy.png'
        self.original_folder_name = 'not_the_messiah'

        self.original_file_path = os.path.join(self.original_folder_name, self.original_filename)

        # Destination folder, filepath.
        self.destination_folder_name = 'a_boy_named_brian'
        self.destination_path = os.path.join(self.destination_folder_name, self.original_file_path)

        # Make origin folder, file, destination folder.
        os.mkdir(self.original_folder_name)
        with open(self.original_file_path, 'w+') as test_file:
            pass
        os.mkdir(self.destination_folder_name)

        # test setUp
        # confirm original files and folders exist
        assert os.path.exists(self.original_folder_name)
        assert os.path.exists(self.original_file_path)
        assert os.path.exists(self.destination_folder_name)

        # Confirm target not in destination folder:
        # Folder in new location.
        assert not os.path.exists(os.path.join(self.destination_folder_name, self.original_folder_name))
        assert not os.path.exists(self.destination_path)  # File in destination_folder/original_folder/file.

    def test_move_file(self):
        move_file(self.original_folder_name, self.destination_folder_name)
        assert os.path.exists(self.destination_path)
        assert not os.path.exists(self.original_file_path)

    def tearDown(self):
        shutil.rmtree(self.destination_folder_name)
