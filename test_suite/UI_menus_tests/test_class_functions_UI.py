import unittest

from itertools import permutations

from unittest import TestCase, mock
from unittest.mock import patch

from dionysus_app.UI_menus.class_functions_UI import (display_class_selection_menu,
                                                      take_classlist_name_input,
                                                      display_student_selection_menu,
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

    @unittest.expectedFailure
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

            assert return_val == self.valid_new_classname

            assert mock_input.call_args_list == [mock.call(self.input_prompt) for test_input in input_strings]
            # Equivalent to [call(self.input_prompt) * len(input_strings)]

            assert mock_print.call_args_list == [mock.call(print_call) for print_call in mock_print_calls if print_call]

            assert mock_input_is_essentially_blank.call_args_list == [mock.call(test_input)
                                                                      for test_input
                                                                      in input_strings]

            print([mock.call(test_input)
                   for test_input in input_strings
                   if test_input is not self.blank_classname['classlist_name']])
            assert mock_classlist_exists.call_args_list == [mock.call(test_input)
                                                            for test_input in input_strings
                                                            if test_input is not self.blank_classname['classlist_name']]
            assert mock_clean_for_filename.assert_called_once_with(self.valid_new_classname['classlist_name'])

            # Reset the mock functions after each test sequence:
            for mock_function in mocked_functions:
                mock_function.reset_mock(return_value=True, side_effect=True)


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
