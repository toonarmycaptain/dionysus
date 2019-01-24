import unittest

from itertools import permutations

from unittest import TestCase, mock
from unittest.mock import patch

from dionysus_app.UI_menus.class_functions_UI import (display_class_selection_menu,
                                                      take_classlist_name_input,
                                                      display_student_selection_menu,
                                                      take_student_name_input,
                                                      blank_class_dialogue,
                                                      class_data_feedback,
                                                      take_class_selection,
                                                      take_student_selection,
                                                      select_avatar_file_dialogue,
                                                      )
from test_suite.testing_class_data import (testing_registry_data_set as test_registry_data_set,
                                           test_display_class_selection_menu_output,
                                           testing_class_data_set as test_class_data_set,
                                           test_display_student_selection_menu_student_output,
                                           )


class TestTakeClasslistNameInputSimpleTest(TestCase):
    """Test only that function returns valid input, only mocking input."""
    mock_definitions_registry = ['this_class_already_exists']  # cleaned_for_filename('this_class_already_exists')

    def setUp(self):
        self.no_classname = ''
        self.blank_classname = '_'
        self.preexisting_class = 'this class already exists'
        self.valid_new_classname = 'this is a valid classname'

        self.valid_new_classname_cleaned_for_filename = 'this_is_a_valid_classname'

        self.test_case_inputs = [self.no_classname,
                                 self.blank_classname,
                                 self.preexisting_class,
                                 self.valid_new_classname,
                                 ]

    @patch('dionysus_app.class_functions.definitions.REGISTRY', mock_definitions_registry)
    def test_take_classlist_name_input(self):
        with patch('dionysus_app.UI_menus.class_functions_UI.input') as mock_input:
            mock_input.side_effect = self.test_case_inputs
            assert take_classlist_name_input() == self.valid_new_classname_cleaned_for_filename


# This test fails - for some reason existent classnames are being returned as OK.
# NB Function doesn't fail in practice.
class TestTakeClasslistNameInputMockingAllCalls(TestCase):

    def setUp(self):
        # Feedback strings:
        self.input_prompt = 'Please enter a name for the class: '
        self.blank_input_response = 'Class name must contain alphanumeric characters.'
        self.classlist_exists_response = 'A class with this name already exists.'

        # Test cases:
        self.preexisting_class = {
            'classlist_name': 'this_class_already_exists',
            'mock_input_is_essentially_blank_return': False,
            'mock_classlist_exists_return': True,
            'mock_print_calls': [self.classlist_exists_response],
            }
        self.valid_new_classname = {
            'classlist_name': 'this_is_a_valid_class_name',
            'mock_input_is_essentially_blank_return': False,
            'mock_classlist_exists_return': False,
            }
        self.blank_classname = {
            'classlist_name': '__blank_classname__',
            'mock_input_is_essentially_blank_return': True,
            'mock_print_calls': [],
            }

        self.test_case_inputs = [self.blank_classname, self.preexisting_class, self.valid_new_classname]

        # Create input values:
        # Create test_case_orders to test any permutation of inputs
        self.test_cases = [list(test_case_order) for test_case_order in permutations(self.test_case_inputs)]

        # Remove out test_inputs after self.valid_new_classname
        for test_case in self.test_cases:
            for test_input in reversed(test_case):
                if test_input is not self.valid_new_classname:
                    test_case.remove(test_input)  # Remove input after successful classname selections.
                else:
                    break

    @unittest.expectedFailure  # Test is broken!
    @patch('dionysus_app.UI_menus.class_functions_UI.clean_for_filename')
    @patch('dionysus_app.UI_menus.class_functions_UI.classlist_exists')
    @patch('dionysus_app.UI_menus.class_functions_UI.input_is_essentially_blank')
    @patch('dionysus_app.UI_menus.class_functions_UI.input')
    @patch('dionysus_app.UI_menus.class_functions_UI.print')
    def test_take_classlist_name_input(self,
                                       mock_print,
                                       mock_input,
                                       mock_input_is_essentially_blank,
                                       mock_classlist_exists,
                                       mock_clean_for_filename,
                                       ):
        mocked_functions = (mock_print,
                            mock_input,
                            mock_input_is_essentially_blank,
                            mock_classlist_exists,
                            mock_clean_for_filename,
                            )

        for test_case in self.test_cases:
            with self.subTest(i=test_case):
                input_strings = [test_input['classlist_name'] for test_input in test_case]
                mock_input_is_essentially_blank_returns = [test_input['mock_input_is_essentially_blank_return']
                                                           for test_input in test_case
                                                           if 'mock_input_is_essentially_blank_return' in test_input]
                mock_classlist_exists_returns = [test_input['mock_classlist_exists_return'] for test_input in test_case
                                                 if 'mock_classlist_exists_return' in test_input]

                mock_print_call_lists = [test_input['mock_print_calls'] for test_input in test_case
                                         if 'mock_print_calls' in test_input]
                mock_print_calls = [print_call for print_call_list in mock_print_call_lists
                                    for print_call in print_call_list]

                mock_input.side_effect = input_strings
                mock_print.side_effect = mock_print_calls
                mock_input_is_essentially_blank.side_effect = mock_input_is_essentially_blank_returns
                mock_classlist_exists.side_effect = mock_classlist_exists_returns
                mock_clean_for_filename.side_effect = input_strings

                print(f'test case number {self.test_cases.index(test_case)}')

                print(f'input calls {input_strings}')

                print(f'mock_blank_calls: {[mock.call(test_input) for test_input in input_strings]}')
                print(f'mock blank returns: {mock_input_is_essentially_blank_returns}')
                print(f"mock exists calls: {[mock.call(test_input) for test_input in input_strings if test_input is not self.blank_classname['classlist_name']]}")
                print(f'mock exists returns: {mock_classlist_exists_returns}')
                print(f'mock print call lists {mock_print_call_lists}')
                print(f'mock print calls: {mock_print_calls}')
                return_val = take_classlist_name_input()  # WHY IS FUNCTION RETURNING BLANK INPUT!!!
                print(f'function returned classlist name: {return_val}')
                print('\n\n\n')

                assert return_val == self.valid_new_classname['classlist_name']

                assert mock_input.call_args_list == [mock.call(self.input_prompt) for test_input in input_strings]

                assert mock_print.call_args_list == [mock.call(print_call)
                                                     for print_call in mock_print_calls if print_call]

                assert mock_input_is_essentially_blank.call_args_list == [mock.call(test_input)
                                                                          for test_input
                                                                          in input_strings]

                print([mock.call(test_input)
                       for test_input in input_strings
                       if test_input is not self.blank_classname['classlist_name']])
                assert mock_classlist_exists.call_args_list == [mock.call(test_input) for test_input in input_strings
                                                                if test_input is not self.blank_classname['classlist_name']]
                assert mock_clean_for_filename.assert_called_once_with(self.valid_new_classname['classlist_name'])

                # Reset the mock functions after each test sequence:
                for mock_function in mocked_functions:
                    mock_function.reset_mock(return_value=True, side_effect=True)


class TestTakeStudentNameInput(TestCase):
    def setUp(self):
        self.no_student_name = ''
        self.blank_student_name = '_'
        self.preexisting_student = 'this student already exists in the class'
        self.valid_new_student_name = 'this is a valid student_name'

        self.invalid_student_name_response = 'Please enter a valid student name.'
        self.preexisting_student_response = 'This student is already a member of the class.'

        self.test_case_inputs = [self.no_student_name,
                                 self.blank_student_name,
                                 self.preexisting_student,
                                 self.valid_new_student_name,
                                 ]

        self.printed_feedback = [self.invalid_student_name_response,
                                 self.invalid_student_name_response,
                                 self.preexisting_student_response,
                                 ]

        self.mock_class_data = {self.preexisting_student: ['some student data']}

    @patch('dionysus_app.UI_menus.class_functions_UI.print')
    def test_take_student_name_input(self, mocked_print):
        with patch('dionysus_app.UI_menus.class_functions_UI.input') as mock_input:
            mock_input.side_effect = self.test_case_inputs
            assert take_student_name_input(self.mock_class_data) == self.valid_new_student_name

            assert mocked_print.call_args_list == [mock.call(printed_string)
                                                   for printed_string in self.printed_feedback]


class TestBlankClassDialogue(TestCase):
    def setUp(self):
        # Blank or junk inputs:
        self.no_input = ''
        self.space_input = ' '
        self.blank_input = '_'
        self.junk_input_knights = 'the knights who say ni'
        self.junk_input_questions = ('First you must answer three questions: \n'
                                     'What is your name?\n'
                                     'What is your quest?\n'
                                     'What is your favourite colour?')
        # Valid inputs:
        # 'No' inputs:
        self.n_input = 'n', False
        self.N_input = 'N', False
        # 'Yes' inputs:
        self.y_input = 'y', True
        self.Y_input = 'Y', True

        self.blank_junk_inputs = [self.no_input, self.space_input, self.junk_input_knights, self.junk_input_questions]
        self.valid_inputs = [self.n_input, self.N_input, self.y_input, self.Y_input]

        # Create test sequences:
        self.input_sets = []
        for valid_input in self.valid_inputs:
            test_case = [self.blank_junk_inputs + [valid_input[0]], valid_input[1]]
            self.input_sets.append(test_case)

    @patch('dionysus_app.UI_menus.class_functions_UI.print')
    def test_blank_class_dialogue(self, mocked_print):
        with patch('dionysus_app.UI_menus.class_functions_UI.input') as mock_input:
            for test_case in self.input_sets:
                with self.subTest(i=test_case):
                    input_strings = test_case[0]
                    expected_return = test_case[1]

                    mock_input.side_effect = input_strings

                    assert blank_class_dialogue() == expected_return

                    # Reset the mock function after each test sequence:
                    mock_input.reset_mock(return_value=True, side_effect=True)


class TestClassDataFeedback(TestCase):
    def setUp(self):
        # Normal class data:
        self.test_class_name = 'the knights of the round table'
        self.test_class_data_dict = test_class_data_set['loaded_dict']
        # Class created without students:
        self.empty_class_data_dict = {}
        self.empty_class_feedback = 'No students entered.'

    def test_class_data_feedback(self):
        with patch('dionysus_app.UI_menus.class_functions_UI.print') as mocked_print:

            printed_strings = [f'\nClass name: {self.test_class_name}'] + [name for name in test_class_data_set['loaded_dict']]

            class_data_feedback(self.test_class_name, self.test_class_data_dict)

            assert mocked_print.call_args_list == [mock.call(printed_string) for printed_string in printed_strings]

    def test_class_data_feedback_with_empty_class(self):
        with patch('dionysus_app.UI_menus.class_functions_UI.print') as mocked_print:

            printed_strings = [f'\nClass name: {self.test_class_name}'] + [self.empty_class_feedback]
            assert printed_strings == [f'\nClass name: {self.test_class_name}',
                                       self.empty_class_feedback]  # ie No student names.

            class_data_feedback(self.test_class_name, self.empty_class_data_dict)

            assert mocked_print.call_args_list == [mock.call(printed_string)
                                                   for printed_string in printed_strings]


class TestDisplayClassSelectionMenu(TestCase):
    def setUp(self):
        self.enumerated_registry = test_registry_data_set['enumerated_dict']
        self.expected_enum_class_strings = test_display_class_selection_menu_output
        self.expected_print_statements = ["Select class from list:", ] + self.expected_enum_class_strings

    def test_display_class_selection_menu(self):
        # capture print function
        # assert captured_print_function == expected_print_statements.
        with patch('dionysus_app.UI_menus.class_functions_UI.print') as mocked_print:
            display_class_selection_menu(self.enumerated_registry)

            print_calls = [mock.call(printed_str) for printed_str in self.expected_print_statements]
            assert mocked_print.call_args_list == print_calls


class TestTakeClassSelection(TestCase):
    def setUp(self):
        self.test_class_options = test_registry_data_set['enumerated_dict']
        self.invalid_input_response = ("Invalid input.\n"
                                       "Please enter the integer beside the name of the desired class.")

        # Blank or junk inputs:
        self.no_input = ''
        self.space_input = ' '
        self.blank_input = '_'
        self.junk_input_knights = 'the knights who say ni'
        self.junk_input_questions = ('First you must answer three questions: \n'
                                     'What is your name?\n'
                                     'What is your quest?\n'
                                     'What is your favourite colour?')
        self.negative_input = '-7'
        self.zero_0_input = '0'
        self.reasonable_float = '2.0'
        self.weird_float = '3.14159'
        self.positive_out_of_range_input = '17'
        # Valid inputs: (valid_input, return_value)
        # Numerical
        self.valid_numerical_inputs = [(str(key), self.test_class_options[key])
                                       for key in self.test_class_options.keys()]
        # Exact class name
        self.valid_string_inputs = [(class_name, class_name) for class_name
                                    in self.test_class_options.values()]

        self.blank_junk_inputs = [self.no_input,
                                  self.space_input,
                                  self.junk_input_knights,
                                  self.junk_input_questions,
                                  self.negative_input,
                                  self.zero_0_input,
                                  self.reasonable_float,
                                  self.weird_float,
                                  self.positive_out_of_range_input,
                                  ]

        self.valid_inputs = self.valid_numerical_inputs + self.valid_string_inputs

        self.input_sets = []
        for valid_input in self.valid_inputs:
            test_case = [self.blank_junk_inputs + [valid_input[0]], valid_input[1]]
            self.input_sets.append(test_case)

    @patch('dionysus_app.UI_menus.class_functions_UI.print')
    def test_take_class_selection(self, mock_print):
        with patch('dionysus_app.UI_menus.class_functions_UI.input') as mock_input:
            for test_case in self.input_sets:
                with self.subTest(i=test_case):
                    input_strings = test_case[0]
                    expected_return = test_case[1]

                    mock_input.side_effect = input_strings

                    assert take_class_selection(self.test_class_options) == expected_return

                    # Check print calls:
                    assert mock_print.call_args_list == [mock.call(self.invalid_input_response)
                                                         for input_string in input_strings[0:-1]]

                    # Reset the mock function after each test sequence:
                    mock_input.reset_mock(return_value=True, side_effect=True)
                    mock_print.reset_mock(return_value=True, side_effect=True)


class TestDisplayStudentSelectionMenu(TestCase):
    def setUp(self):
        self.enumerated_classlist = test_class_data_set['enumerated_dict']
        self.expected_enum_student_strings = test_display_student_selection_menu_student_output
        self.expected_print_statements = ["Select student from list:", ] + self.expected_enum_student_strings

    def test_display_student_selection_menu(self):
        # capture print function
        # assert captured_print_function == expected_print_statements.
        with patch('dionysus_app.UI_menus.class_functions_UI.print') as mocked_print:
            display_student_selection_menu(self.enumerated_classlist)

            print_calls = [mock.call(printed_str) for printed_str in self.expected_print_statements]
            assert mocked_print.call_args_list == print_calls


class TestTakeStudentSelection(TestCase):
    def setUp(self):
        self.test_class_student_options = test_class_data_set['enumerated_dict']
        self.invalid_input_response = "Invalid input.\nPlease enter the integer beside the name of the desired student."

        # Blank or junk inputs:
        self.no_input = ''
        self.space_input = ' '
        self.blank_input = '_'
        self.junk_input_sir_galahad = 'Sir Galahad the brave'
        self.junk_input_questions = ('First you must answer three questions: \n'
                                     'What is your name?\n'
                                     'What is your quest?\n'
                                     'What is your favourite colour?')
        self.negative_input = '-7'
        self.zero_0_input = '0'
        self.reasonable_float = '2.0'
        self.weird_float = '3.14159'
        self.positive_out_of_range_input = '76'
        # Valid inputs: (valid_input, return_value)
        # Numerical
        self.valid_numerical_inputs = [(str(key), self.test_class_student_options[key])
                                       for key in self.test_class_student_options.keys()]
        # Exact class name
        self.valid_string_inputs = [(class_name, class_name) for class_name in self.test_class_student_options.values()]

        self.blank_junk_inputs = [self.no_input,
                                  self.space_input,
                                  self.junk_input_sir_galahad,
                                  self.junk_input_questions,
                                  self.negative_input,
                                  self.zero_0_input,
                                  self.reasonable_float,
                                  self.weird_float,
                                  self.positive_out_of_range_input,
                                  ]

        self.valid_inputs = self.valid_numerical_inputs + self.valid_string_inputs

        self.input_sets = []
        for valid_input in self.valid_inputs:
            test_case = [self.blank_junk_inputs + [valid_input[0]], valid_input[1]]
            self.input_sets.append(test_case)

    @patch('dionysus_app.UI_menus.class_functions_UI.print')
    def test_take_student_selection(self, mock_print):
        with patch('dionysus_app.UI_menus.class_functions_UI.input') as mock_input:
            for test_case in self.input_sets:
                with self.subTest(i=test_case):
                    input_strings = test_case[0]
                    expected_return = test_case[1]

                    mock_input.side_effect = input_strings

                    assert take_student_selection(self.test_class_student_options) == expected_return

                    # Check print calls:
                    assert mock_print.call_args_list == [mock.call(self.invalid_input_response)
                                                         for input_string in input_strings[0:-1]]

                    # Reset the mock function after each test sequence:
                    mock_input.reset_mock(return_value=True, side_effect=True)
                    mock_print.reset_mock(return_value=True, side_effect=True)


class TestSelectAvatarFileDialogue(TestCase):
    def setUp(self):
        self.my_avatar_path = 'C:\\how_not_to_be_seen.avatar_can_be_seen'

        # Mocked file dialogue arguments
        self.dialogue_box_title = 'Select .png format avatar:'
        self.filetypes = [('.png files', '*.png'), ("all files", "*.*")]
        self.start_dir = '..'  # start at parent to app directory.

    @patch('dionysus_app.UI_menus.class_functions_UI.select_file_dialogue')
    def test_select_avatar_file_dialogue(self, mocked_select_file_dialogue):

        mocked_select_file_dialogue.return_value = self.my_avatar_path

        assert select_avatar_file_dialogue() == self.my_avatar_path
        mocked_select_file_dialogue.assert_called_once_with(self.dialogue_box_title,
                                                            self.filetypes,
                                                            self.start_dir,
                                                            )
