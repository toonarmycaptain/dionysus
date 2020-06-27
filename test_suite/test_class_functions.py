"""Test functions in class_functions.py"""
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from dionysus_app import class_functions
from dionysus_app.chart_generator import create_chart
from dionysus_app.class_ import Class, NewClass
from dionysus_app.class_functions import (avatar_file_exists,
                                          compose_classlist_dialogue,
                                          create_chart_with_new_class,
                                          create_classlist,
                                          create_class_list_dict,
                                          edit_classlist,
                                          load_chart_data,
                                          select_classlist,
                                          select_student,
                                          take_class_data_input,
                                          take_student_avatar,
                                          )
from dionysus_app.persistence.database import ClassIdentifier
from dionysus_app.student import Student
from dionysus_app.UI_menus.UI_functions import clean_for_filename
from test_suite.test_persistence.test_database import empty_generic_database  # Fixture.
from test_suite.test_class import (test_class_name_only,
                                   test_full_class)
from test_suite.testing_class_data import (testing_registry_data_set as test_registry_data_set,
                                           test_full_class_data_set,
                                           )


class TestCreateClasslist:
    def test_create_classlist(self, monkeypatch, empty_generic_database,
                              test_full_class):
        test_database = empty_generic_database

        def mocked_take_classlist_name_input():
            return test_full_class.name

        def mocked_compose_classlist_dialogue(test_class_name):
            if test_class_name != test_full_class.name:
                raise ValueError
            return test_full_class


        def mocked_create_class(test_class):
            if test_class != test_full_class:
                raise ValueError

        test_database.create_class = mocked_create_class

        def mocked_time_sleep(seconds):
            pass

        def mocked_create_chart_with_new_class(test_class_name):
            if test_class_name != test_full_class:
                raise ValueError

        monkeypatch.setattr(class_functions, 'take_classlist_name_input', mocked_take_classlist_name_input)
        monkeypatch.setattr(class_functions, 'compose_classlist_dialogue', mocked_compose_classlist_dialogue)
        monkeypatch.setattr(class_functions.definitions, 'DATABASE', test_database)
        monkeypatch.setattr(class_functions.time, 'sleep', mocked_time_sleep)
        monkeypatch.setattr(class_functions, 'create_chart_with_new_class', mocked_create_chart_with_new_class)

        assert create_classlist() is None


class TestComposeClasslistDialogue:
    @pytest.mark.parametrize(
        'class_data, create_blank_class',
        [([Class.from_dict(test_full_class_data_set['json_dict_rep'])], []),
         ([Class(name='Empty class with no students')], [True]),  # Empty class created
         pytest.param([Class(name='class with no students')], [],
                      marks=pytest.mark.xfail(reason="No values left to return from blank_class_dialogue.")),
         ([Class(name=Class.from_dict(test_full_class_data_set['json_dict_rep']).name),  # Empty class, then full class.
           Class.from_dict(test_full_class_data_set['json_dict_rep'])], [False]),
         ([Class(name="Empty class"), Class(name="Empty class")], [False, True]),  # Empty class refused then accepted.
         ])
    def test_compose_classlist_dialogue_full_class(self, monkeypatch,
                                                   class_data, create_blank_class,
                                                   test_full_class,
                                                   ):
        class_data_to_return = (test_class for test_class in class_data)

        def mocked_take_class_data_input(class_name):
            if class_name not in [test_class.name for test_class in class_data]:
                raise ValueError
            return next(class_data_to_return)

        blank_class_returns = (chosen_option for chosen_option in create_blank_class)

        def mocked_blank_class_dialogue():
            # Will raise StopIteration if no values left to return (or none to begin with).
            return next(blank_class_returns)

        def mocked_class_data_feedback(test_class):
            if test_class not in class_data:
                raise ValueError

        monkeypatch.setattr(class_functions, 'take_class_data_input', mocked_take_class_data_input)
        monkeypatch.setattr(class_functions, 'blank_class_dialogue', mocked_blank_class_dialogue)
        monkeypatch.setattr(class_functions, 'class_data_feedback', mocked_class_data_feedback)
        assert compose_classlist_dialogue(class_data[0].name).json_dict() == class_data[-1].json_dict()


class TestTakeClassDataInput:
    def test_take_class_data_input(self, monkeypatch):
        test_class_name = 'my test class'
        test_take_student_name_input_returns = ['test_student', 'END']
        take_student_avatar_return = 'my_student_avatar.jpg'
        test_class = Class(name=test_class_name,
                           students=[Student(name=test_take_student_name_input_returns[0],
                                             avatar_filename=take_student_avatar_return),
                                     ])
        test_take_student_name_input_return = (name for name in test_take_student_name_input_returns)

        def mocked_take_student_name_input(new_class):
            if new_class.name != test_class_name:
                raise ValueError
            return next(test_take_student_name_input_return)

        def mocked_take_student_avatar(new_class, student_name):
            if (new_class.name, student_name) != (test_class_name, test_take_student_name_input_returns[0]):
                raise ValueError
            return take_student_avatar_return

        monkeypatch.setattr(class_functions, 'take_student_avatar', mocked_take_student_avatar)
        monkeypatch.setattr(class_functions, 'take_student_name_input', mocked_take_student_name_input)

        assert take_class_data_input(test_class_name).json_dict() == test_class.json_dict()


class TestTakeStudentAvatar:
    def test_take_student_avatar_no_avatar(self, monkeypatch):
        test_class = NewClass('some_class')

        def mocked_select_avatar_file_dialogue():
            return None  # No file selected

        monkeypatch.setattr(class_functions, 'select_avatar_file_dialogue', mocked_select_avatar_file_dialogue)

        # Ensure calls to other funcs will cause error.
        monkeypatch.delattr(class_functions, 'clean_for_filename')
        monkeypatch.delattr(class_functions, 'copy_file')

        assert take_student_avatar(test_class, 'some student') is None

    def test_take_student_avatar_pre_clean_name(self, monkeypatch):
        test_class = NewClass('some_class')
        test_student_name = 'clean name'
        test_avatar_filepath = Path('avatar file name')
        cleaned_student_name = 'file name was already clean'
        returned_filename = f'{cleaned_student_name}.png'

        def mocked_select_avatar_file_dialogue():
            return test_avatar_filepath

        def mocked_clean_for_filename(student_name):
            if student_name != test_student_name:
                raise ValueError  # Ensure called with correct arg.
            return cleaned_student_name

        def mocked_copy_file(avatar_filepath, destination_filepath):
            if (avatar_filepath, destination_filepath) != (
                    test_avatar_filepath, test_class.temp_avatars_dir.joinpath(returned_filename)):
                raise ValueError  # Ensure called with correct args.
            return None

        monkeypatch.setattr(class_functions, 'select_avatar_file_dialogue', mocked_select_avatar_file_dialogue)
        monkeypatch.setattr(class_functions, 'clean_for_filename', mocked_clean_for_filename)
        monkeypatch.setattr(class_functions, 'copy_file', mocked_copy_file)

        assert take_student_avatar(test_class, test_student_name) == returned_filename

    def test_take_student_avatar_dirty_name(self, monkeypatch):
        test_class = NewClass('some_class')
        test_student_name = r'very unsafe */^@ :$ name'
        test_avatar_filepath = Path('avatar file name')

        returned_filename = f'{clean_for_filename(test_student_name)}.png'

        def mocked_select_avatar_file_dialogue():
            return test_avatar_filepath

        def mocked_copy_file(avatar_filepath, destination_filepath):
            if (avatar_filepath, destination_filepath) != (
                    test_avatar_filepath, test_class.temp_avatars_dir.joinpath(returned_filename)):
                raise ValueError  # Ensure called with correct args.
            return None

        monkeypatch.setattr(class_functions, 'select_avatar_file_dialogue', mocked_select_avatar_file_dialogue)
        monkeypatch.setattr(class_functions, 'copy_file', mocked_copy_file)

        assert take_student_avatar(test_class, test_student_name) == returned_filename


class TestAvatarFileExists:
    @pytest.mark.parametrize(
        'path_exists, return_value',
        [(True, True),
         (False, False),
         pytest.param(False, True, marks=pytest.mark.xfail),
         pytest.param(True, False, marks=pytest.mark.xfail),
         ])
    def test_avatar_file_exists(self, monkeypatch, path_exists, return_value):
        monkeypatch.setattr(class_functions.Path, 'exists', lambda x: path_exists)

        assert avatar_file_exists('some_path') is return_value


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
        test_class_options = {1: ClassIdentifier('one', 'one'),
                              2: ClassIdentifier('two', 'two'),
                              3: ClassIdentifier('three', 'three')}
        selected_class = ClassIdentifier('some_class', 'some_class')

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

        assert select_classlist() == selected_class.id


class TestCreateClassListDict:
    @pytest.mark.parametrize(
        'classes_list, enumerated_dict',
        [(test_registry_data_set['enumerated_dict'].values(), test_registry_data_set['enumerated_dict']),
         pytest.param(None, 'error raised!', marks=pytest.mark.xfail('ValueError("No Database found.")')),
         ])
    def test_create_class_list_dict_patching_REGISTRY(self, monkeypatch, empty_generic_database,
                                                      classes_list, enumerated_dict,
                                                      ):
        def mocked_get_classes():
            return classes_list

        test_database = empty_generic_database
        test_database.get_classes = mocked_get_classes
        monkeypatch.setattr(class_functions.definitions, 'DATABASE', test_database)

        assert create_class_list_dict() == test_registry_data_set['enumerated_dict']


class TestSelectStudent:
    @pytest.mark.parametrize('selected_student_name, selected_student_students_index',
                             [('one', 0),
                              ('two', 1),
                              ('three', 2),
        pytest.param('one', 2, marks=pytest.mark.xfail(reason="Wrong student.")),

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


class TestLoadChartData:
    def test_load_chart_data(self, monkeypatch):
        mock_load_from_json_file_return_data = {1: 'one', 2: 'two', 3: 'three'}

        monkeypatch.setattr(class_functions, 'load_from_json_file', lambda path: mock_load_from_json_file_return_data)
        assert load_chart_data(Path('some chart datafile')) == mock_load_from_json_file_return_data


class TestEditClasslist:
    def test_edit_classlist(self, monkeypatch):
        monkeypatch.setattr(class_functions, 'take_classlist_name_input', lambda: 'some class name')
        mocked_open = mock_open()
        with patch('dionysus_app.class_functions.open', mocked_open):
            assert edit_classlist() is None
