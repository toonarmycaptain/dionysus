import os
import shutil

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, mock_open

from dionysus_app.file_functions import (convert_to_json,
                                         load_from_json,
                                         load_from_json_file,
                                         )
from dionysus_app.file_functions import copy_file, move_file
from test_suite.testing_class_data import testing_class_data_set as test_json_class_data


class TestConvertToJson(TestCase):
    def setUp(self):
        self.data_to_convert = {1: 'a', 'b': 2, 3: 'c', 'd': 4}
        self.json_converted_data = '{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}'

    def test_convert_to_json(self):
        assert convert_to_json(self.data_to_convert) == self.json_converted_data


class TestLoadFromJson(TestCase):
    def setUp(self):
        self.json_data_to_convert = '{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}'
        self.converted_json_data = {"1": 'a', 'b': 2, "3": 'c', 'd': 4}
        self.test_json_class_data = test_json_class_data

    def test_load_from_json(self):
        assert load_from_json(self.json_data_to_convert) == self.converted_json_data

    def test_load_from_json_test_class_data(self):
        assert load_from_json(self.test_json_class_data['json_data_string']) == self.test_json_class_data['loaded_dict']


class TestLoadFromJsonFile(TestCase):
    def setUp(self):
        self.test_file_json_data_to_convert = '{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}'
        self.mock_file_path = Path('test_file_path')
        self.converted_json_data = {"1": 'a', 'b': 2, "3": 'c', 'd': 4}

    def test_load_from_json_file(self):
        with patch('dionysus_app.file_functions.open', mock_open(read_data=self.test_file_json_data_to_convert)):

            assert load_from_json_file(self.mock_file_path) == self.converted_json_data


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
        assert not os.path.exists(self.original_filename)
        shutil.rmtree(self.new_folder_name)  # remove new dir
        assert not os.path.exists(self.new_folder_name)


class TestCopyFileMockingCopyfile(TestCase):
    def setUp(self):
        self.original_filename = 'just_a_naughty_boy.png'
        self.new_folder_name = 'not_the_messiah'

        self.original_path = self.original_filename
        self.destination_path = os.path.join(self.new_folder_name, self.original_filename)

    def test_copy_file_mocking_copyfile(self):
        with patch('dionysus_app.file_functions.copyfile') as mock_copyfile:
            copy_file(self.original_path, self.destination_path)
            mock_copyfile.assert_called_once_with(str(self.original_path), str(self.destination_path))


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
        assert not os.path.exists(self.new_folder_name)
        assert not os.path.exists(self.original_filename)


class TestMoveFileMockingMove(TestCase):
    def setUp(self):
        self.original_filename = 'just_a_naughty_boy.png'
        self.new_folder_name = 'not_the_messiah'

        self.original_path = self.original_filename
        self.destination_path = os.path.join(self.new_folder_name, self.original_filename)

    def test_move_file_mocking_move(self):
        with patch('dionysus_app.file_functions.move') as mock_move:
            move_file(self.original_path, self.destination_path)
            mock_move.assert_called_once_with(str(self.original_path), str(self.destination_path))


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

    def test_move_file_directory_containing_file(self):
        move_file(self.original_folder_name, self.destination_folder_name)
        assert os.path.exists(self.destination_path)
        assert not os.path.exists(self.original_file_path)
        assert not os.path.exists(self.original_folder_name)

    def tearDown(self):
        shutil.rmtree(self.destination_folder_name)
        assert not os.path.exists(self.destination_folder_name)
