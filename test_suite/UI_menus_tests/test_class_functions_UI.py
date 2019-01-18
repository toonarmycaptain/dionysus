from unittest import TestCase, mock
from unittest.mock import patch

from dionysus_app.UI_menus.class_functions_UI import display_class_selection_menu, display_student_selection_menu
from test_suite.testing_class_data import (testing_registry_data_set as test_registry_data_set,
                                           test_display_class_selection_menu_output,
                                           testing_class_data_set as test_class_data_set,
                                           test_display_student_selection_menu_student_output,
                                           )


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
