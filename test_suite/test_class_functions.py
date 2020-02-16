"""Test functions in class_functions.py"""

import os
import shutil

from pathlib import Path
from unittest.mock import patch, mock_open

from unittest import mock, TestCase  # this is needed to use mock.call, since from mock import call causes an error.

import pytest

from dionysus_app import class_functions, class_registry_functions
from dionysus_app.chart_generator import create_chart
from dionysus_app.class_ import Class
from dionysus_app.class_functions import (avatar_path_from_string,
                                          compose_classlist_dialogue,
                                          copy_avatar_to_app_data,
                                          create_chart_with_new_class,
                                          create_classlist,
                                          create_classlist_data,
                                          create_class_list_dict,
                                          edit_classlist,
                                          get_avatar_path,
                                          load_chart_data,
                                          load_class_from_disk,
                                          select_classlist,
                                          select_student,
                                          setup_class,
                                          setup_class_data_storage,
                                          take_class_data_input,
                                          take_student_avatar,
                                          write_classlist_to_file,
                                          )
from dionysus_app.student import Student
from test_suite.test_class import (test_class_name_only,
                                   test_full_class)
from dionysus_app.UI_menus.UI_functions import clean_for_filename
from test_suite.testing_class_data import (testing_registry_data_set as test_registry_data_set,
                                           test_full_class_data_set,
                                           )


class TestCreateClasslist:
    def test_create_classlist(self, monkeypatch, test_full_class):
        def mocked_take_classlist_name_input():
            return test_full_class.name

        def mocked_compose_classlist_dialogue(test_class_name):
            if test_class_name != test_full_class.name:
                raise ValueError
            return test_full_class

        def mocked_create_classlist_data(test_class):
            if test_class != test_full_class:
                raise ValueError

        def mocked_time_sleep(seconds):
            pass

        def mocked_create_chart_with_new_class(test_class_name):
            if test_class_name != test_full_class.name:
                raise ValueError

        monkeypatch.setattr(class_functions, 'take_classlist_name_input', mocked_take_classlist_name_input)
        monkeypatch.setattr(class_functions, 'compose_classlist_dialogue', mocked_compose_classlist_dialogue)
        monkeypatch.setattr(class_functions, 'create_classlist_data', mocked_create_classlist_data)
        monkeypatch.setattr(class_functions.time, 'sleep', mocked_time_sleep)
        monkeypatch.setattr(class_functions, 'create_chart_with_new_class', mocked_create_chart_with_new_class)
        assert create_classlist() is None


class TestSetupClass(TestCase):
    def setUp(self):
        self.test_classlist_name = 'the_knights_who_say_ni'

    @patch('dionysus_app.class_functions.setup_class_data_storage')
    @patch('dionysus_app.class_functions.register_class')
    def test_setup_class(self, mock_register_class, mock_setup_class_data_storage):
        assert setup_class(self.test_classlist_name) is None
        mock_setup_class_data_storage.assert_called_once_with(self.test_classlist_name)
        mock_register_class.assert_called_once_with(self.test_classlist_name)


class TestSetupClassDataStorage(TestCase):
    mock_CLASSLIST_DATA_PATH = Path('a_shrubbery')
    mock_DEFAULT_CHART_SAVE_FOLDER = Path('Camelot')

    def setUp(self):
        self.mock_CLASSLIST_DATA_PATH = Path('a_shrubbery')
        self.mock_DEFAULT_CHART_SAVE_FOLDER = Path('Camelot')
        self.test_class_name = 'the_knights_who_say_ni'

        # Created paths
        self.test_avatar_path = self.mock_CLASSLIST_DATA_PATH.joinpath(self.test_class_name, 'avatars')
        self.test_chart_path = self.mock_CLASSLIST_DATA_PATH.joinpath(self.test_class_name, 'chart_data')
        self.test_user_chart_save_folder = Path(self.mock_DEFAULT_CHART_SAVE_FOLDER).joinpath(self.test_class_name)

        self.created_directory_paths = [self.test_avatar_path,
                                        self.test_chart_path,
                                        self.test_user_chart_save_folder,
                                        ]

    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('definitions.DEFAULT_CHART_SAVE_FOLDER', mock_DEFAULT_CHART_SAVE_FOLDER)
    def test_setup_class_data_storage(self):
        with patch('dionysus_app.class_functions.Path.mkdir', autospec=True) as mock_mkdir:
            setup_class_data_storage(self.test_class_name)

            mkdir_calls = [mock.call(directory_path, exist_ok=True, parents=True)
                           for directory_path in self.created_directory_paths]
            assert mock_mkdir.mock_calls == mkdir_calls


def test_setup_class_data_storage_raising_error(monkeypatch):
    monkeypatch.setattr(class_registry_functions.definitions, 'DEFAULT_CHART_SAVE_FOLDER', None)
    with pytest.raises(ValueError):
        setup_class_data_storage('some_class')


class TestCreateClasslistData:
    def test_create_classlist_data(self, monkeypatch, test_full_class):
        def mocked_setup_class(test_class_name):
            if test_class_name != test_full_class.name:
                raise ValueError

        def mocked_write_classlist_to_file(test_class):
            if test_class != test_full_class:
                raise ValueError

        monkeypatch.setattr(class_functions, 'setup_class', mocked_setup_class)
        monkeypatch.setattr(class_functions, 'write_classlist_to_file', mocked_write_classlist_to_file)

        assert create_classlist_data(test_full_class) is None


class TestComposeClasslistDialogue:
    def test_compose_classlist_dialogue_full_class(self, monkeypatch, test_full_class):
        def mocked_take_class_data_input(test_class_name):
            if test_class_name != test_full_class.name:
                raise ValueError
            return test_full_class

        def mocked_blank_class_dialogue():
            raise ValueError  # Should not be called.

        def mocked_class_data_feedback(test_class):
            if test_class != test_full_class:
                raise ValueError

        monkeypatch.setattr(class_functions, 'take_class_data_input', mocked_take_class_data_input)
        monkeypatch.setattr(class_functions, 'blank_class_dialogue', mocked_blank_class_dialogue)
        monkeypatch.setattr(class_functions, 'class_data_feedback', mocked_class_data_feedback)
        assert compose_classlist_dialogue(test_full_class.name).json_dict() == test_full_class.json_dict()

    def test_compose_classlist_dialogue_create_empty_class(self, monkeypatch, test_class_name_only):
        def mocked_take_class_data_input(test_class_name):
            if test_class_name != test_class_name_only.name:
                raise ValueError
            return test_class_name_only

        def mocked_blank_class_dialogue():
            return True

        def mocked_class_data_feedback(test_class):
            if test_class != test_class_name_only:
                raise ValueError

        monkeypatch.setattr(class_functions, 'take_class_data_input', mocked_take_class_data_input)
        monkeypatch.setattr(class_functions, 'blank_class_dialogue', mocked_blank_class_dialogue)
        monkeypatch.setattr(class_functions, 'class_data_feedback', mocked_class_data_feedback)

        assert compose_classlist_dialogue(test_class_name_only.name).json_dict() == test_class_name_only.json_dict()


class TestComposeClasslistDialogueMockMultipleInputCalls(TestCase):
    """This is necessary to mock multiple returns from take_class_data_input."""

    def setUp(self) -> None:
        self.full_class_return = Class.from_dict(test_full_class_data_set['json_dict_rep'])
        self.empty_class_return = Class(name=self.full_class_return.name)

    @patch('dionysus_app.class_functions.blank_class_dialogue')
    @patch('dionysus_app.class_functions.take_class_data_input')
    def test_compose_classlist_dialogue_empty_class(self, mock_take_class_data_input,
                                                    mock_blank_class_dialogue):
        mock_take_class_data_input.side_effect = [self.empty_class_return,
                                                  self.full_class_return]
        mock_blank_class_dialogue.return_value = False

        assert compose_classlist_dialogue(self.full_class_return.name).json_dict() == self.full_class_return.json_dict()


class TestTakeClassDataInput(TestCase):
    """Unittest used to mock multiple returns from student_name_input."""

    def setUp(self) -> None:
        self.test_class_name = 'my test class'
        self.test_student_name_input_returns = ['test_student', 'END']
        self.take_student_avatar_return = 'my_student_avatar.jpg'

        self.test_class = Class(name=self.test_class_name,
                                students=[Student(name=self.test_student_name_input_returns[0],
                                                  avatar_filename=self.take_student_avatar_return),
                                          ])

    @patch('dionysus_app.class_functions.take_student_avatar')
    @patch('dionysus_app.class_functions.take_student_name_input')
    def test_take_class_data_input(self, mock_take_student_name_input,
                                   mock_take_student_avatar):
        mock_take_student_name_input.side_effect = self.test_student_name_input_returns
        mock_take_student_avatar.return_value = self.take_student_avatar_return

        assert take_class_data_input(self.test_class_name).json_dict() == self.test_class.json_dict()


class TestTakeStudentAvatar:
    def test_take_student_avatar_no_avatar(self, monkeypatch):
        def mocked_select_avatar_file_dialogue():
            return None  # No file selected

        monkeypatch.setattr(class_functions, 'select_avatar_file_dialogue', mocked_select_avatar_file_dialogue)

        # Ensure calls to other funcs will cause error.
        monkeypatch.delattr(class_functions, 'clean_for_filename')
        monkeypatch.delattr(class_functions, 'copy_avatar_to_app_data')

        assert take_student_avatar('some class', 'some student') is None

    def test_take_student_avatar_pre_clean_name(self, monkeypatch):
        test_class_name = 'some class'
        test_student_name = 'clean name'
        test_avatar_filename = 'avatar file name'
        cleaned_student_name = 'file name was already clean'
        returned_filename = f'{cleaned_student_name}.png'

        def mocked_select_avatar_file_dialogue():
            return test_avatar_filename

        def mocked_clean_for_filename(student_name):
            if student_name != test_student_name:
                raise ValueError  # Ensure called with correct arg.
            return cleaned_student_name

        def mocked_copy_avatar_to_app_data(class_name, avatar_filename, target_filename):
            if (class_name, avatar_filename, target_filename) != (
                    test_class_name, test_avatar_filename, returned_filename):
                raise ValueError  # Ensure called with correct args.
            return None

        monkeypatch.setattr(class_functions, 'select_avatar_file_dialogue', mocked_select_avatar_file_dialogue)
        monkeypatch.setattr(class_functions, 'clean_for_filename', mocked_clean_for_filename)
        monkeypatch.setattr(class_functions, 'copy_avatar_to_app_data', mocked_copy_avatar_to_app_data)

        assert take_student_avatar(test_class_name, test_student_name) == returned_filename

    def test_take_student_avatar_dirty_name(self, monkeypatch):
        test_class_name = 'some class'
        test_student_name = r'very unsafe */^@ :$ name'
        test_avatar_filename = 'avatar file name'

        returned_filename = f'{clean_for_filename(test_student_name)}.png'

        def mocked_select_avatar_file_dialogue():
            return test_avatar_filename

        def mocked_copy_avatar_to_app_data(class_name, avatar_filename, target_filename):
            if (class_name, avatar_filename, target_filename) != (
                    test_class_name, test_avatar_filename, returned_filename):
                raise ValueError  # Ensure called with correct args.
            return None

        monkeypatch.setattr(class_functions, 'select_avatar_file_dialogue', mocked_select_avatar_file_dialogue)
        monkeypatch.setattr(class_functions, 'copy_avatar_to_app_data', mocked_copy_avatar_to_app_data)

        assert take_student_avatar(test_class_name, test_student_name) == returned_filename


class TestCopyAvatarToAppData(TestCase):
    mock_CLASSLIST_DATA_PATH = Path('.')
    mock_DEFAULT_CHART_SAVE_FOLDER = Path('my_charts')

    # Need to mock globals in setUp call of setup_class_data_storage
    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('dionysus_app.class_functions.definitions.DEFAULT_CHART_SAVE_FOLDER', mock_DEFAULT_CHART_SAVE_FOLDER)
    def setUp(self):
        self.mock_CLASSLIST_DATA_PATH = Path('.')
        self.mock_DEFAULT_CHART_SAVE_FOLDER = Path('my_charts')

        # arguments to copy_avatar_to_app_data
        self.test_classlist_name = 'arthurs_knights'
        self.test_avatar_filename = 'sir_lancelot_the_looker.image'
        self.copied_avatar_save_filename = 'sir_lancelot.png'

        # create test file and structure.
        with open(self.test_avatar_filename, 'w+') as avatar_file:
            pass

        # Setup test class storage,
        setup_class_data_storage(self.test_classlist_name)
        self.test_class_datafolder_path = self.mock_CLASSLIST_DATA_PATH.joinpath(self.test_classlist_name)
        self.test_class_avatar_subfolder_path = self.test_class_datafolder_path.joinpath('avatars')
        self.test_class_chart_data_subfolder_path = self.test_class_datafolder_path.joinpath('chart_data')

        self.copied_avatar_filepath = self.test_class_avatar_subfolder_path.joinpath(self.copied_avatar_save_filename)

        # assert test preconditions met
        assert os.path.exists(self.test_avatar_filename)
        assert os.path.exists(self.test_class_avatar_subfolder_path)

        assert not os.path.exists(self.copied_avatar_filepath)

    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('dionysus_app.class_functions.definitions.DEFAULT_CHART_SAVE_FOLDER', mock_DEFAULT_CHART_SAVE_FOLDER)
    def test_copy_avatar_to_app_data(self):
        copy_avatar_to_app_data(self.test_classlist_name, self.test_avatar_filename, self.copied_avatar_save_filename)
        assert os.path.exists(self.copied_avatar_filepath)

    def tearDown(self):
        os.remove(self.test_avatar_filename)  # Remove test avatar file
        assert not os.path.exists(self.test_avatar_filename)

        # Remove tree created in setup_class_data_storage
        shutil.rmtree(self.test_class_datafolder_path)
        assert not os.path.exists(self.test_class_datafolder_path)
        shutil.rmtree(self.mock_DEFAULT_CHART_SAVE_FOLDER)
        assert not os.path.exists(self.mock_DEFAULT_CHART_SAVE_FOLDER)


class TestCopyAvatarToAppDataMockingCopyfile(TestCase):
    mock_CLASSLIST_DATA_PATH = Path('.')
    mock_DEFAULT_CHART_SAVE_FOLDER = Path('my_charts')

    def setUp(self):
        self.mock_CLASSLIST_DATA_PATH = Path('.')
        self.mock_DEFAULT_CHART_SAVE_FOLDER = Path('my_charts')

        # arguments to copy_avatar_to_app_data
        self.test_classlist_name = 'arthurs_knights'
        self.test_avatar_filename = 'sir_lancelot_the_looker.image'
        self.copied_avatar_save_filename = 'sir_lancelot.png'

        # Setup test class storage paths
        self.test_class_datafolder_path = self.mock_CLASSLIST_DATA_PATH.joinpath(self.test_classlist_name)
        self.test_class_avatar_subfolder_path = self.test_class_datafolder_path.joinpath('avatars')
        self.test_class_chart_data_subfolder_path = self.test_class_datafolder_path.joinpath('chart_data')

        self.copied_avatar_filepath = self.test_class_avatar_subfolder_path.joinpath(self.copied_avatar_save_filename)

        # assert test preconditions met
        assert not os.path.exists(self.copied_avatar_filepath)

    @patch('definitions.DEFAULT_CHART_SAVE_FOLDER', mock_DEFAULT_CHART_SAVE_FOLDER)
    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    def test_copy_avatar_to_app_data_copy_file_mocked(self):
        with patch('dionysus_app.class_functions.copy_file') as mocked_copy_file:
            copy_avatar_to_app_data(self.test_classlist_name, self.test_avatar_filename,
                                    self.copied_avatar_save_filename)
            mocked_copy_file.assert_called_once_with(self.test_avatar_filename, self.copied_avatar_filepath)


class TestWriteClasslistToFile(TestCase):
    mock_CLASSLIST_DATA_PATH = Path('.')
    mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'

    def setUp(self):
        self.mock_CLASSLIST_DATA_PATH = Path('.')
        self.mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'

        self.test_class_json_dict = test_full_class_data_set['json_dict_rep']
        self.test_class_name = self.test_class_json_dict['name']

        self.test_class_object = Class.from_dict(self.test_class_json_dict)

        # Build save file path
        self.test_class_filename = self.test_class_name + self.mock_CLASSLIST_DATA_FILE_TYPE
        self.test_class_data_path = self.mock_CLASSLIST_DATA_PATH.joinpath(self.test_class_name)
        self.test_class_data_file_path = self.test_class_data_path.joinpath(self.test_class_filename)

        os.makedirs(self.test_class_data_path, exist_ok=True)

    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('dionysus_app.class_functions.CLASSLIST_DATA_FILE_TYPE', mock_CLASSLIST_DATA_FILE_TYPE)
    def test_write_classlist_to_file(self):
        # Assert precondition:
        assert not os.path.exists(self.test_class_data_file_path)

        assert write_classlist_to_file(self.test_class_object) is None

        assert isinstance(self.test_class_data_file_path, Path)

        # Assert file created:
        assert os.path.exists(self.test_class_data_file_path)
        # Verify file contents:
        with open(self.test_class_data_file_path, 'r') as test_class_data_file:
            assert test_class_data_file.read() == self.test_class_object.to_json_str()

    def tearDown(self):
        os.remove(self.test_class_data_file_path)
        shutil.rmtree(self.test_class_data_path)
        assert not os.path.exists(self.test_class_data_file_path)
        assert not os.path.exists(self.test_class_data_path)


class TestWriteClasslistToFileMockingOpen(TestCase):
    mock_CLASSLIST_DATA_PATH = Path('.')
    mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'

    def setUp(self):
        self.mock_CLASSLIST_DATA_PATH = Path('.')
        self.mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'

        self.test_class_json_dict = test_full_class_data_set['json_dict_rep']
        self.test_class_name = self.test_class_json_dict['name']

        self.test_class_object = Class.from_dict(self.test_class_json_dict)

        # Build save file path
        self.test_class_filename = self.test_class_name + self.mock_CLASSLIST_DATA_FILE_TYPE
        self.test_class_data_path = self.mock_CLASSLIST_DATA_PATH.joinpath(self.test_class_name)
        self.test_class_data_file_path = self.test_class_data_path.joinpath(self.test_class_filename)

    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('dionysus_app.class_functions.CLASSLIST_DATA_FILE_TYPE', mock_CLASSLIST_DATA_FILE_TYPE)
    def test_write_classlist_to_file_mocking_open(self):
        mocked_open = mock_open()
        with patch('dionysus_app.class_functions.open', mocked_open), \
             patch('dionysus_app.class_functions.Path.mkdir', autospec=True) as mocked_mkdir:
            assert write_classlist_to_file(self.test_class_object) is None

            assert isinstance(self.test_class_data_file_path, Path)

            mocked_mkdir.assert_called_once_with(self.test_class_data_file_path.parent, exist_ok=True, parents=True)

            mocked_open.assert_called_once_with(self.test_class_data_file_path, 'w')

            opened_test_class_data_file = mocked_open()
            opened_test_class_data_file.write.assert_called_with(self.test_class_object.to_json_str())


class TestCreateChartWithNewClass:
    @pytest.mark.parametrize('test_classname, chose_to_create_chart_from_class',
                             [('Class choosing to create chart immediately', True),
                              ('Class choosing not to create chart immediately', False),
                              ])
    def test_create_chart_with_new_class(self, monkeypatch, test_classname, chose_to_create_chart_from_class):
        def mocked_create_chart_with_new_class_dialogue():
            return chose_to_create_chart_from_class

        def mocked_new_chart(test_class_name):
            if test_class_name != test_classname:
                raise ValueError
            if not chose_to_create_chart_from_class:
                raise ValueError(f'create_chart wrongly called for class {test_class_name}')

        # Mock create_chart_with_new_class_dialogue in original location, due to import at runtime
        # rather than at top of class_functions module.
        monkeypatch.setattr(class_functions, 'create_chart_with_new_class_dialogue',
                            mocked_create_chart_with_new_class_dialogue)
        monkeypatch.setattr(create_chart, 'new_chart', mocked_new_chart)

        assert create_chart_with_new_class(test_classname) is None


class TestSelectClasslist:
    def test_select_classlist(self, monkeypatch):
        test_class_options = {1: 'one', 2: 'two', 3: 'three'}
        selected_class = 'some_class'

        def mocked_create_class_list_dict():
            return test_class_options

        def mocked_display_class_selection_menu(class_options):
            if class_options != test_class_options:
                raise ValueError  # Ensure called with correct arg.
            return None

        def mocked_take_class_selection(class_options):
            if class_options != test_class_options:
                raise ValueError  # Ensure called with correct arg.
            return selected_class

        monkeypatch.setattr(class_functions, 'create_class_list_dict', mocked_create_class_list_dict)
        monkeypatch.setattr(class_functions, 'display_class_selection_menu', mocked_display_class_selection_menu)
        monkeypatch.setattr(class_functions, 'take_class_selection', mocked_take_class_selection)

        assert select_classlist() == selected_class


class TestCreateClassListDict(TestCase):
    mock_definitions_registry = test_registry_data_set['registry_classlist']

    def setUp(self):
        self.mock_definitions_registry = test_registry_data_set['registry_classlist']
        self.enumerated_class_registry = test_registry_data_set['enumerated_dict']

    @patch('dionysus_app.class_functions.definitions.REGISTRY', mock_definitions_registry)
    def test_create_class_list_dict_patching_REGISTRY(self):
        assert create_class_list_dict() == self.enumerated_class_registry


def test_create_class_list_dict(monkeypatch):
    monkeypatch.setattr(class_functions.definitions, 'REGISTRY', None)
    with pytest.raises(ValueError):
        create_class_list_dict()


class TestSelectStudent:
    @pytest.mark.parametrize('selected_student_name, selected_student_students_index',
                             [('one', 0),
                              ('two', 1),
                              ('three', 2),
                              ])
    def test_select_student(self, monkeypatch, selected_student_name, selected_student_students_index):
        test_class_students = [Student(name='one'), Student(name='two'), Student(name='three')]
        test_class = Class(name='some_class', students=test_class_students)
        test_student_options = {1: 'one', 2: 'two', 3: 'three'}

        def mocked_display_student_selection_menu(class_options):
            if class_options != test_student_options:
                raise ValueError  # Ensure called with correct arg.
            return None

        def mocked_take_student_selection(class_options):
            if class_options != test_student_options:
                raise ValueError  # Ensure called with correct arg.
            return selected_student_name

        monkeypatch.setattr(class_functions, 'display_student_selection_menu', mocked_display_student_selection_menu)
        monkeypatch.setattr(class_functions, 'take_student_selection', mocked_take_student_selection)

        assert select_student(test_class) == test_class_students[selected_student_students_index]


class TestLoadClassFromDisk(TestCase):
    mock_CLASSLIST_DATA_PATH = Path('.')
    mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'

    def setUp(self):
        self.mock_CLASSLIST_DATA_PATH = Path('.')
        self.mock_CLASSLIST_DATA_FILE_TYPE = '.class_data_file'

        self.test_class_json_str = test_full_class_data_set['json_str_rep']
        self.test_class_json_dict = test_full_class_data_set['json_dict_rep']
        self.test_class_name = self.test_class_json_dict['name']

        self.test_class_data_filename = self.test_class_name + self.mock_CLASSLIST_DATA_FILE_TYPE
        self.test_classlist_data_path = self.mock_CLASSLIST_DATA_PATH.joinpath(self.test_class_name,
                                                                               self.test_class_data_filename)

        # Create class data_file
        os.mkdir(self.test_class_name)
        with open(self.test_classlist_data_path, 'w+') as my_test_class_data:
            my_test_class_data.write(self.test_class_json_str)

    @patch('dionysus_app.class_functions.CLASSLIST_DATA_PATH', mock_CLASSLIST_DATA_PATH)
    @patch('dionysus_app.class_functions.CLASSLIST_DATA_FILE_TYPE', mock_CLASSLIST_DATA_FILE_TYPE)
    def test_load_class_data_from_disk(self):
        loaded_class = load_class_from_disk(self.test_class_name)
        assert isinstance(loaded_class, Class)
        assert loaded_class.json_dict() == self.test_class_json_dict

    def tearDown(self):
        shutil.rmtree(self.test_class_name)
        assert not os.path.exists(self.test_classlist_data_path)
        assert not os.path.exists(self.test_class_name)


class TestLoadChartData(TestCase):
    def setUp(self):
        self.test_chart_data_path = Path('my_test_path')
        self.mock_load_from_json_file_return_data = {1: 'one', 2: 'two', 3: 'three'}

    def test_load_chart_data(self):
        with patch('dionysus_app.class_functions.load_from_json_file') as mock_load_from_json_file:
            mock_load_from_json_file.return_value = self.mock_load_from_json_file_return_data

            assert load_chart_data(self.test_chart_data_path) == self.mock_load_from_json_file_return_data


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

    @patch('dionysus_app.class_functions.DEFAULT_AVATAR_PATH', mock_DEFAULT_AVATAR_PATH)
    def test_get_avatar_path_when_called_with_no_avatar_arg(self):
        assert get_avatar_path(self.my_class_name) == self.mock_DEFAULT_AVATAR_PATH

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


class TestEditClasslist(TestCase):
    @patch('dionysus_app.class_functions.take_classlist_name_input')
    def test_edit_classlist(self, mocked_take_classlist_name_input):
        mocked_take_classlist_name_input.return_value = 'some class name'
        mocked_open = mock_open()
        with patch('dionysus_app.class_functions.open', mocked_open):
            assert edit_classlist() is None


class TestLoad_class_from_disk(TestCase):
    pass
