import os, shutil

from unittest import TestCase

from dionysus_app.file_functions import convert_to_json, copy_file, move_file


class TestConvertToJson(TestCase):
    def test_convert_to_json(self):
        data_to_convert = {1: 'a', 'b': 2, 3: 'c', 'd': 4}
        json_converted_data = '{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}'

        assert convert_to_json(data_to_convert) == json_converted_data


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

# TODO: test moving a directory with files in it.
