from pathlib import Path
from unittest import mock
from unittest.mock import patch

import pytest

from dionysus_app.class_ import Class
from dionysus_app.student import Student
from dionysus_app.UI_menus import class_functions_UI
from dionysus_app.UI_menus.class_functions_UI import (blank_class_dialogue,
                                                      class_data_feedback,
                                                      create_chart_with_new_class_dialogue,
                                                      display_class_selection_menu,
                                                      display_student_selection_menu,
                                                      select_avatar_file_dialogue,
                                                      take_classlist_name_input,
                                                      take_class_selection,
                                                      take_student_name_input,
                                                      take_student_selection,
                                                      )
from test_suite.test_class import test_class_name_only, test_full_class  # fixture
from test_suite.testing_class_data import (testing_registry_data_set as test_registry_data_set,
                                           test_full_class_data_set as test_class_data_set,
                                           test_display_student_selection_menu_student_output,
                                           )
from test_suite.test_persistence.test_database import empty_generic_database  # fixture


class TestTakeClasslistNameInputSimpleTest:
    """Test return on valid input after invalid inputs."""

    def test_take_classlist_name_input(self, monkeypatch, empty_generic_database):
        def mocked_class_name_exists(class_id):
            if class_id == preexisting_classname:
                return True
            return False

        test_database = empty_generic_database
        test_database.class_name_exists = mocked_class_name_exists
        monkeypatch.setattr(class_functions_UI.definitions, 'DATABASE', test_database)

        preexisting_classname = 'this_class_already_exists'  # cleaned_for_filename('this_class_already_exists')
        valid_new_classname = 'this is a valid classname'
        valid_new_classname_cleaned_for_filename = 'this_is_a_valid_classname'  # =cleaned_for_filename('this is a valid classname')

        test_inputs = ['',  # no_classname
                       '_',  # blank_classname
                       preexisting_classname,
                       # Valid input:
                       valid_new_classname,
                       ]

        with patch('builtins.input') as mock_input:
            mock_input.side_effect = test_inputs
            assert take_classlist_name_input() == valid_new_classname_cleaned_for_filename


class TestTakeStudentNameInput:
    def test_take_student_name_input(self):
        """Test return on valid input after invalid inputs."""
        preexisting_student_name = 'this student already exists in the class'
        test_class = Class(name='my_test_class', students=[Student(name=preexisting_student_name)])

        valid_new_student_name = 'this is a valid student name'

        test_inputs = ['',  # no_student_name,
                       '_',  # blank_student_name,
                       preexisting_student_name,  # preexisting_student_name,
                       valid_new_student_name,  # valid_new_student_name,
                       ]

        with patch('builtins.input') as mock_input:
            mock_input.side_effect = test_inputs
            assert take_student_name_input(test_class) == valid_new_student_name


class TestBlankClassDialogue:
    @pytest.mark.parametrize('ask_user_bool_return',
                             [True, False])
    def test_blank_class_dialogue(self, monkeypatch,
                                  ask_user_bool_return):
        """Dialogue returns user input."""

        def mocked_ask_user_bool(question, invalid_input_response):
            assert (question, invalid_input_response) == (
                'Do you want to create an empty class? [Y/N] ',
                'Please enter y for yes to create empty class, or n to return to student input.')
            return ask_user_bool_return

        monkeypatch.setattr(class_functions_UI, 'ask_user_bool', mocked_ask_user_bool)

        assert blank_class_dialogue() == ask_user_bool_return


class TestClassDataFeedback:
    """
    User feedback rendered as expected.

    NB These tests are kinda fragile because of necessity to append the '\n's
    in the correct places. Currently function is including a newline before
    the class name, but the rest are supplied by the multiple calls to
    print(), hence needing to include them manually when simply capturing
    what is passed to print.
    """

    def test_class_data_feedback(self, test_full_class, capsys):
        printed_strings = [f'\nClass name: {test_full_class.name}\n'] + [student.name + '\n' for student in
                                                                         test_full_class]
        class_data_feedback(test_full_class)
        captured = capsys.readouterr().out
        assert captured == ''.join(printed_strings)

    def test_class_data_feedback_with_empty_class(self, test_class_name_only, capsys):
        empty_class_feedback = 'No students entered.'

        printed_strings = [f'\nClass name: {test_class_name_only.name}\n{empty_class_feedback}\n']
        class_data_feedback(test_class_name_only)
        captured = capsys.readouterr().out
        assert captured == ''.join(printed_strings)


class TestCreateChartWithNewClassDialogue:
    @pytest.mark.parametrize(
        'inputs, returned_value',
        [([bad_input, good_input], return_value)
         for bad_input in ['0', '1', '7', 'a', 'z', 'something', '/', '*', '\n', '', ]
         for good_input, return_value in [('n', False),
                                          ('N', False),
                                          ('y', True),
                                          ('Y', True), ]
         ])
    def test_create_chart_with_new_class_dialogue(self, inputs, returned_value):
        """Dialogue returns valid user input."""
        with mock.patch('builtins.input', side_effect=inputs):
            assert create_chart_with_new_class_dialogue() is returned_value


class TestDisplayClassSelectionMenu:
    def test_display_class_selection_menu(self):
        """User feedback rendered as expected."""
        enumerated_registry = test_registry_data_set['enumerated_dict']
        expected_enum_class_strings = [f'{numeral}. {class_.name}'
                                       for numeral, class_ in enumerated_registry.items()]
        expected_print_statements = ["Select class from list:", ] + expected_enum_class_strings

        # capture print function
        # assert captured_print_function == expected_print_statements.
        with patch('builtins.print') as mocked_print:
            display_class_selection_menu(enumerated_registry)

            print_calls = [mock.call(printed_str) for printed_str in expected_print_statements]
            assert mocked_print.call_args_list == print_calls


class TestTakeClassSelection:
    @pytest.mark.parametrize(
        'inputs, returned_value',
        [([bad_input, good_input], return_value)
         for bad_input in ['',  # no_input
                           ' ',  # space_input
                           '_',  # blank_input
                           'the knights who say ni',  # junk_input_knights
                           ('First you must answer three questions: \n'  # junk_input_questions
                            'What is your name?\n'
                            'What is your quest?\n'
                            'What is your favourite colour?'),
                           '-7',  # negative_input
                           '0',  # zero_0_input
                           '2.0',  # reasonable_float
                           '3.14159',  # weird_float
                           '17',  # positive_out_of_range_input
                           ]
         for good_input, return_value in [(str(key), test_registry_data_set['enumerated_dict'][key])  # Numerical inputs
                                          for key in test_registry_data_set['enumerated_dict'].keys()
                                          ] + [(class_.name, class_)  # Exact class name inputs
                                               for class_ in test_registry_data_set['enumerated_dict'].values()]
         ])
    def test_take_class_selection(self, inputs, returned_value):
        """Valid input after invalid input yields expected value."""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = inputs

            assert take_class_selection(test_registry_data_set['enumerated_dict']) == returned_value


class TestDisplayStudentSelectionMenu:
    def test_display_student_selection_menu(self):
        """User feedback rendered as expected."""
        enumerated_classlist = test_class_data_set['enumerated_dict']
        expected_enum_student_strings = test_display_student_selection_menu_student_output
        expected_print_statements = ["Select student from list:", ] + expected_enum_student_strings

        # capture print function
        # assert captured_print_function == expected_print_statements.
        with patch('builtins.print') as mocked_print:
            display_student_selection_menu(enumerated_classlist)

            print_calls = [mock.call(printed_str) for printed_str in expected_print_statements]
            assert mocked_print.call_args_list == print_calls


class TestTakeStudentSelection:
    @pytest.mark.parametrize(
        'inputs, expected_return',
        [([bad_input, good_input], return_value)
         for bad_input in ['',  # no_input
                           ' ',  # space_input
                           '_',  # blank_input
                           'Sir Galahad the brave',  # junk_input_sir_galahad
                           ('First you must answer three questions: \n'  # junk_input_questions
                            'What is your name?\n'
                            'What is your quest?\n'
                            'What is your favourite colour?'),
                           '-7',  # negative_input
                           '0',  # zero_0_input
                           '2.0',  # reasonable_float
                           '3.14159',  # weird_float
                           '76',  # positive_out_of_range_input
                           ]
         for good_input, return_value in [(str(key), test_class_data_set['enumerated_dict'][key])  # Numerical inputs
                                          for key in test_class_data_set['enumerated_dict'].keys()
                                          ] + [(student_name, student_name) for student_name in
                                               # Exact class name inputs
                                               test_class_data_set['enumerated_dict'].values()]
         ])
    def test_take_student_selection(self, inputs, expected_return):
        """Valid input after invalid input yields expected value."""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = inputs

            assert take_student_selection(test_class_data_set['enumerated_dict']) == expected_return


class TestSelectAvatarFileDialogue:
    def test_select_avatar_file_dialogue(self, monkeypatch):
        test_avatar_path = Path('C:\\how_not_to_be_seen.avatar_can_be_seen')

        test_dialogue_box_title = 'Select .png format avatar:'
        test_filetypes = [('.png files', '*.png'), ("all files", "*.*")]
        test_start_dir = '..'  # start at parent to app directory.

        def mocked_select_file_dialogue(title_str, filetypes, start_dir):
            if (title_str, filetypes, start_dir) != (test_dialogue_box_title, test_filetypes, test_start_dir):
                raise ValueError(f"Wrong args passed:\n"
                                 f"Expected: {title_str, filetypes, start_dir}\n"
                                 f"Passed: {test_dialogue_box_title, test_filetypes, test_start_dir}\n")
            return test_avatar_path

        monkeypatch.setattr(class_functions_UI, 'select_file_dialogue', mocked_select_file_dialogue)

        assert select_avatar_file_dialogue() == test_avatar_path
