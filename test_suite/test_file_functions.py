from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from dionysus_app import file_functions
from dionysus_app.file_functions import (convert_to_json,
                                         load_from_json,
                                         load_from_json_file,
                                         )
from dionysus_app.file_functions import copy_file, move_file
from test_suite.testing_class_data import test_full_class_data_set as test_json_class_data


@pytest.fixture
def test_file():
    """
    Return function that creates an arbitrary at a text file, test_file.txt in
    a given directory, return the path of the file.
    """

    def create_file(test_path):
        test_filepath = Path(test_path, 'test_file.txt')
        with open(test_filepath, 'w') as test_file:
            test_file.write('This is a placeholder file.')
        if not test_filepath.exists():
            raise FileNotFoundError('This file should exist now.')
        return test_filepath

    return create_file


def test_test_file_fixture(tmpdir, test_file):
    tf = test_file(tmpdir)

    assert isinstance(tf, Path)
    assert tf.exists()
    assert open(tf).read() == 'This is a placeholder file.'


class TestConvertToJson:
    @pytest.mark.parametrize(
        'loaded_object, json_str',
        [({"1": 'a', 'b': 2, "3": 'c', 'd': 4}, '{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}'),
         (test_json_class_data['json_dict_rep'], test_json_class_data['json_str_rep']),
         ])
    def test_convert_to_json(self, loaded_object, json_str):
        assert convert_to_json(loaded_object) == json_str


class TestLoadFromJson:
    @pytest.mark.parametrize(
        'json_str, loaded_object',
        [('{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}',
          {"1": 'a', 'b': 2, "3": 'c', 'd': 4}),
         (test_json_class_data['json_str_rep'],
          test_json_class_data['json_dict_rep']),
         ])
    def test_load_from_json(self, json_str, loaded_object):
        assert load_from_json(json_str) == loaded_object


class TestLoadFromJsonFile:
    @pytest.mark.parametrize(
        'json_file_data, loaded_object',
        [('{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}',
          {"1": 'a', 'b': 2, "3": 'c', 'd': 4}),
         (test_json_class_data['json_str_rep'],
          test_json_class_data['json_dict_rep']),
         ])
    def test_load_from_json_file(self, json_file_data, loaded_object):
        mock_file_path = Path('test_file_path')
        with patch('dionysus_app.file_functions.open', mock_open(read_data=json_file_data)):
            assert load_from_json_file(mock_file_path) == loaded_object


class TestCopyFile:
    def test_copy_file(self, tmpdir, test_file, monkeypatch):
        def mocked_copyfile(origin, destination):
            # Test copyfile called with expected arguments.
            assert (origin, destination) == (str(original_filepath), str(destination_filepath))

        original_filepath = test_file(tmpdir)

        destination_filepath = Path('some destination')
        monkeypatch.setattr(file_functions, 'copyfile', mocked_copyfile)

        assert not Path.exists(destination_filepath)
        copy_file(original_filepath, destination_filepath)

    def test_copy_file_copies_file(self, tmpdir, test_file):
        original_filepath = test_file(tmpdir)
        original_filename = original_filepath.name

        destination_dir = Path(tmpdir, 'new_directory')
        Path.mkdir(destination_dir)
        destination_filepath = Path(destination_dir, original_filename)

        assert not Path.exists(destination_filepath)
        copy_file(original_filepath, destination_filepath)

        # Assert file in destination and still in origin.
        assert Path.exists(destination_filepath) and Path.exists(original_filepath)

    def test_copy_file_non_existent_original(self, monkeypatch):
        def mocked_copyfile(origin, destination):
            # Should not be called.
            raise NotImplementedError

        monkeypatch.setattr(file_functions, 'copyfile', mocked_copyfile)

        copy_file('Non-existent origin', 'No destination')


class TestMoveFile:
    def test_move_file(self, tmpdir, test_file, monkeypatch):
        def mocked_move(origin, destination):
            # Test copyfile called with expected arguments.
            assert (origin, destination) == (str(original_filepath), str(destination_filepath))

        original_filepath = test_file(tmpdir)
        destination_filepath = Path('some destination')

        monkeypatch.setattr(file_functions, 'move', mocked_move)

        assert not Path.exists(destination_filepath)
        move_file(original_filepath, destination_filepath)

    def test_move_file_moves_file(self, tmpdir, test_file):
        original_filepath = test_file(tmpdir)
        original_filename = original_filepath.name

        destination_dir = Path(tmpdir, 'new_directory')
        Path.mkdir(destination_dir)
        destination_filepath = Path(destination_dir, original_filename)

        assert not Path.exists(destination_filepath)
        move_file(original_filepath, destination_filepath)

        # Assert file in destination and not in origin.
        assert Path.exists(destination_filepath) and not Path.exists(original_filepath)

    def test_move_file_non_existent_original(self, monkeypatch):
        def mocked_move(origin, destination):
            # Should not be called.
            raise NotImplementedError

        monkeypatch.setattr(file_functions, 'move', mocked_move)

        move_file('Non-existent origin', 'No destination')

    def test_move_file_directory_containing_file(self, tmpdir, test_file):
        # Create directory with file in it.
        original_dirname = 'original_dir'
        original_dir = Path(tmpdir, original_dirname)
        Path.mkdir(original_dir)
        original_filepath = test_file(original_dir)
        original_filename = original_filepath.name

        destination_dir = Path(tmpdir, 'new_directory')
        Path.mkdir(destination_dir)
        destination_filepath = Path(destination_dir, original_dirname, original_filename)

        assert not Path.exists(destination_filepath)
        # Move original folder with file in it.
        move_file(original_dir, destination_dir)

        # Assert original directory no longer exists, file in destination and not in origin.
        assert not Path.exists(original_dir)
        assert Path.exists(destination_filepath) and not Path.exists(original_filepath)
