"""
TestCleanForFilename, test_clean_for_filename

TestSaveAsDialogue, test_save_as_dialogue
TestScrubCandidateFilename, test_scrub_candidate_filename
TestSelectFileDialogue, test_select_file_dialogue
TestSelectFolderDialogue, test_select_folder_dialogue
"""
from unittest import TestCase, mock
from unittest.mock import patch

from dionysus_app.UI_menus.UI_functions import (clear_screen,
                                                )


class TestClearScreen(TestCase):
    def setUp(self):
        self.test_arguments = 1, 5, 99
        self.expected_print_calls = ['\n',
                                     5 * '\n',
                                     99 * '\n',
                                     ]
        self.default_argument = 50
        self.default_argument_print_call = 50 * '\n'

    def test_clear_screen(self):
        with patch('dionysus_app.UI_menus.UI_functions.print') as mocked_print:
            for argument in self.test_arguments:
                clear_screen(argument)

            print_calls = [mock.call(printed_str) for printed_str in self.expected_print_calls]

            mocked_print.assert_has_calls(print_calls)  # Test calls.
            assert mocked_print.call_args_list == print_calls  # Test calls made in order.

    def test_clear_screen_default_argument(self):
        with patch('dionysus_app.UI_menus.UI_functions.print') as mocked_print:
            clear_screen()

            print_call = self.default_argument_print_call
            mocked_print.assert_called_once_with(print_call)


class TestInputIsEssentiallyBlank(TestCase):
    def setUp(self):
        pass

    def test_input_is_essentially_blank(self):
        pass

"""
        test_empty_string '' ie no input
        test_single_space ' ',
        test_multiple_spaces 2,3,5 ' ', '  ', '   ', '     '
        test_singe_leading_space ' test'
        test_leading_spaces '   test'
        test_singe_trailing_space 'test '
        test_trailing_spaces 'test   '
        test_leading_and_trailing_space ' test '
        test_no_spaces 'test'
        test_sentence 'not the Spanish inquisition'
        test_sentence_leading_and_trailing_spaces ' not the spanish inquisition'
        test_single_underscore '_'
        test some combinations of _, ' ', - etc
"""
