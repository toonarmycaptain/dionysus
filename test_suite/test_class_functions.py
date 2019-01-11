"""Test functions in class_functions.py"""

import os
import shutil

from pathlib import Path
from unittest.mock import patch, mock_open
from unittest import TestCase

import definitions

from dionysus_app.class_functions import (avatar_path_from_string,
                                          CLASSLIST_DATA_PATH,
                                          copy_avatar_to_app_data,
                                          create_class_list_dict,
                                          create_student_list_dict,
                                          get_avatar_path,
                                          load_class_data,
                                          setup_class_data_storage,
                                          write_classlist_to_file,
                                          )
from test_suite.testing_class_data import test_load_class_data_class_data_set as test_json_class_data


class TestSetupClassDataStorage(TestCase):
    pass


class TestCopyAvatarToAppData(TestCase):
    def setUp(self):
        # arguments to copy_avatar_to_app_data
        self.test_classlist_name = 'arthurs_knights'
        self.test_avatar_filename = 'sir_lancelot_the_looker.image'
        self.copied_avatar_save_filename = 'sir_lancelot.png'

        # create test file and structure.
        with open(self.test_avatar_filename, 'w+') as avatar_file:
            pass

        # Mock out global for test:

        # Save original value to restore in tearDown
        self.DEFAULT_CHART_SAVE_FOLDER_value = definitions.DEFAULT_CHART_SAVE_FOLDER
        # Mock value
        definitions.DEFAULT_CHART_SAVE_FOLDER = '.'

        # Setup test class storage,
        setup_class_data_storage(self.test_classlist_name)
        self.test_class_datafolder_path = CLASSLIST_DATA_PATH.joinpath(self.test_classlist_name)
        self.test_class_avatar_subfolder_path = self.test_class_datafolder_path.joinpath('avatars')
        self.test_class_chart_data_subfolder_path = self.test_class_datafolder_path.joinpath('chart_data')

        self.copied_avatar_filepath = self.test_class_avatar_subfolder_path.joinpath(self.copied_avatar_save_filename)

        # assert test preconditions met
        assert os.path.exists(self.test_avatar_filename)
        assert os.path.exists(self.test_class_avatar_subfolder_path)

        assert not os.path.exists(self.copied_avatar_filepath)

    def test_copy_avatar_to_app_data(self):
        copy_avatar_to_app_data(self.test_classlist_name, self.test_avatar_filename, self.copied_avatar_save_filename)
        assert os.path.exists(self.copied_avatar_filepath)

    def tearDown(self):
        os.remove(self.test_avatar_filename)  # remove test avatar file

        shutil.rmtree(self.test_class_datafolder_path)  # remove class_datafolder
        os.rmdir(self.test_classlist_name)  # remove user_save_charts folder

        # Restore definitions.DEFAULT_CHART_SAVE_FOLDER to original value
        definitions.DEFAULT_CHART_SAVE_FOLDER = self.DEFAULT_CHART_SAVE_FOLDER_value


class TestWriteClasslistToFile(TestCase):
    mock_CLASSLIST_DATA_PATH = Path('.')
    mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'

    def setUp(self):
        self.mock_CLASSLIST_DATA_PATH = Path('.')
        self.mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'
        self.test_class_name = 'test_classname'
        self.test_class_json_string = test_json_class_data['json_data_string']
        self.test_class_data_dict = test_json_class_data['loaded_dict']

        self.test_class_filename = self.test_class_name + self.mock_CLASSLIST_DATA_FILE_TYPE
        self.test_class_data_path = self.mock_CLASSLIST_DATA_PATH.joinpath(self.test_class_name)
        self.test_class_data_file_path = self.test_class_data_path.joinpath(self.test_class_filename)

        os.makedirs(self.test_class_data_path, exist_ok=True)

    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('dionysus_app.class_functions.CLASSLIST_DATA_FILE_TYPE', mock_CLASSLIST_DATA_FILE_TYPE)
    def test_write_classlist_to_file(self):
        assert write_classlist_to_file(self.test_class_name, self.test_class_data_dict) is None
        assert os.path.exists(self.test_class_data_file_path)

        assert open(self.test_class_data_file_path, 'r').read() == self.test_class_json_string


    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('dionysus_app.class_functions.CLASSLIST_DATA_FILE_TYPE', mock_CLASSLIST_DATA_FILE_TYPE)
    @patch('dionysus_app.class_functions.convert_to_json')
    def test_write_classlist_to_file_mocking_called_functions(self, mocked_convert_to_json):
        mocked_convert_to_json.return_value = self.test_class_json_string

        mocked_open = mock_open()
        with patch('dionysus_app.class_functions.open', mocked_open):
            assert write_classlist_to_file(self.test_class_name, self.test_class_data_dict) is None

            mocked_convert_to_json.assert_called_once_with(self.test_class_data_dict)
            mocked_open.assert_called_once_with(self.test_class_data_file_path, 'w')

            opened_test_class_data_file = mocked_open()
            opened_test_class_data_file.write.assert_called_with(self.test_class_json_string)

    def tearDown(self):
        shutil.rmtree(self.test_class_data_path)
        assert not os.path.exists(self.test_class_data_file_path)
        assert not os.path.exists(self.test_class_data_path)


class TestCreateClassListDict(TestCase):
    mock_definitions_registry = ['First class', 'Second class', 'Third class']

    def setUp(self):
        self.mock_definitions_registry = ['First class', 'Second class', 'Third class']
        self.enumerated_class_registry = {'1': 'First class', '2': 'Second class', '3': 'Third class'}

    @patch('dionysus_app.class_functions.definitions.REGISTRY', mock_definitions_registry)
    def test_create_class_list_dict_patching_REGISTRY(self):
        assert create_class_list_dict() == self.enumerated_class_registry


class TestCreateStudentListDict(TestCase):
    def setUp(self):
        self.class_data_dict = test_json_class_data['loaded_dict']
        self.enumerated_class_data_dict = test_json_class_data['enumerated_dict']

    @patch('dionysus_app.class_functions.load_class_data')
    def test_create_student_list_dict_patching_load_class_data(self, mock_load_class_data):
        mock_load_class_data.return_value = self.class_data_dict
        assert create_student_list_dict(self.class_data_dict) == self.enumerated_class_data_dict


class TestLoadClassData(TestCase):
    mock_CLASSLIST_DATA_PATH = Path('.')
    mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'

    def setUp(self):
        self.mock_CLASSLIST_DATA_PATH = Path('.')
        self.mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'

        self.test_class_name = 'my_test_class'
        self.test_class_data_filename = self.test_class_name + self.mock_CLASSLIST_DATA_FILE_TYPE
        self.test_classlist_data_path = self.mock_CLASSLIST_DATA_PATH.joinpath(self.test_class_name,
                                                                               self.test_class_data_filename)

        self.test_class_json_data = test_json_class_data['json_data_string']
        self.test_class_loaded_data = test_json_class_data['loaded_dict']

        # create class data_file
        os.mkdir(self.test_class_name)
        with open(self.test_classlist_data_path, 'w+') as my_test_class_data:
            my_test_class_data.write(self.test_class_json_data)

    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('dionysus_app.class_functions.CLASSLIST_DATA_FILE_TYPE', mock_CLASSLIST_DATA_FILE_TYPE)
    def test_load_class_data_from_disk(self):
        loaded_json_data = load_class_data(self.test_class_name)
        assert isinstance(loaded_json_data, dict)
        assert self.test_class_loaded_data == loaded_json_data

    def test_load_class_data_mocked_open(self):
        with patch('dionysus_app.class_functions.open', mock_open(read_data=self.test_class_json_data)):
            assert isinstance(self.test_class_loaded_data, dict)
            assert load_class_data(self.test_class_name) == self.test_class_loaded_data

    def tearDown(self):
        shutil.rmtree(self.test_class_name)
        assert not os.path.exists(self.test_classlist_data_path)
        assert not os.path.exists(self.test_class_name)


class TestGetAvatarPath(TestCase):
    mock_DEFAULT_AVATAR_PATH = Path('mocked_default_avatar_path')
    mock_CLASSLIST_DATA_PATH = Path('mocked_classlist_data_path')

    def setUp(self):
        self.mock_DEFAULT_AVATAR_PATH = Path('mocked_default_avatar_path')
        self.mock_CLASSLIST_DATA_PATH = Path('mocked_classlist_data_path')
        self.my_class_name = 'my_class'
        self.my_avatar_path = 'my_avatar_path'

    @patch('dionysus_app.class_functions.DEFAULT_AVATAR_PATH', mock_DEFAULT_AVATAR_PATH)
    def test_get_avatar_path_when_None(self):
        assert get_avatar_path(self.my_class_name, None) == self.mock_DEFAULT_AVATAR_PATH

    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('dionysus_app.class_functions.DEFAULT_AVATAR_PATH', mock_DEFAULT_AVATAR_PATH)
    def test_get_avatar_path_returning_avatar_path_from_string(self):
        return_val = Path(self.mock_CLASSLIST_DATA_PATH, self.my_class_name, 'avatars', self.my_avatar_path)
        assert get_avatar_path(self.my_class_name, self.my_avatar_path) == return_val

    @patch('dionysus_app.class_functions.avatar_path_from_string')
    def test_get_avatar_path_calls_avatar_path_from_string(self, mock_avatar_path_from_string):
        mock_avatar_path_from_string.return_value = True
        assert get_avatar_path(self.my_class_name, self.my_avatar_path)


class TestAvatarPathFromString(TestCase):
    mock_CLASSLIST_DATA_PATH = Path('mocked_classlist_data_path')

    def setUp(self):
        self.mock_CLASSLIST_DATA_PATH = Path('mocked_classlist_data_path')

    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    def test_avatar_path_from_string(self):
        class_name = 'test_classname'
        avatar_filename = 'test_avatar.file'

        return_val = Path(self.mock_CLASSLIST_DATA_PATH, class_name, 'avatars', avatar_filename)
        assert avatar_path_from_string(class_name, avatar_filename) == return_val
