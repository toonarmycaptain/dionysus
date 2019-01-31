"""
TestCleanForFilename, test_clean_for_filename

TestSaveAsDialogue, test_save_as_dialogue
TestScrubCandidateFilename, test_scrub_candidate_filename
TestSelectFileDialogue, test_select_file_dialogue
TestSelectFolderDialogue, test_select_folder_dialogue
"""
from pathlib import Path
from unittest import TestCase, mock
from unittest.mock import patch

from dionysus_app.UI_menus.UI_functions import (clean_for_filename,
                                                clear_screen,
                                                input_is_essentially_blank,
                                                save_as_dialogue,
                                                scrub_candidate_filename,
                                                select_file_dialogue,
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
        # Test cases: (input_value, expected_return_value)
        self.test_cases = {
            'test_empty_string': ('', True),  # ie no input
            # Spaces
            'test_single_space': (' ', True),
            'test_2_spaces': ('  ', True),
            'test_3_spaces': ('   ', True),
            'test_5_spaces': ('     ', True),
            # Underscores
            'test_single_underscore': ('_', True),
            'test_2_underscores': ('__', True),
            'test_3_underscores': ('___', True),
            'test_5_underscores': ('_____', True),

            'test_only_special_characters': ('''~`!@#$%^&*()-_+{}[]|\\:;"',.<>?/''', True),
            'test_singe_leading_space': (' test', False),
            'test_spaces_underscores_combo': (' _ _ _', True),
            'test_leading_spaces': ('   test', False),
            'test_singe_trailing_space': ('test ', False),
            'test_trailing_spaces': ('test   ', False),
            'test_leading_and_trailing_space': (' test ', False),
            'test_no_spaces': ('test', False),
            'test_sentence': ('not the Spanish inquisition', False),
            'test_sentence_leading_and_trailing_spaces': (' not the spanish inquisition ', False),
            'test_combination_underscore_spaces': (
                " because nobody_expects_the _spanish_ inquisition the 2nd time", False),
            'test_combination_underscore_spaces_special_characters': (
                " because nobody_expects_the !@#$%ing _spanish_ inquisition the 2nd ?~)*% time", False),
            }

    def test_input_is_essentially_blank(self):
        for test_case in self.test_cases:
            with self.subTest(i=self.test_cases[test_case]):
                test_input = self.test_cases[test_case][0]
                expected_output = self.test_cases[test_case][1]

                assert input_is_essentially_blank(test_input) == expected_output


class TestCleanForFilename(TestCase):
    def setUp(self):
        # Test cases: (input_value, expected_return_value)
        self.test_cases = {
            'test_empty_string': ('', ''),  # ie no input
            # Spaces
            'test_single_space': (' ', ''),  # .rstrip() will remove trailing space.
            'test_2_spaces': ('  ', ''),
            'test_3_spaces': ('   ', ''),
            'test_5_spaces': ('     ', ''),
            # Underscores
            'test_single_underscore': ('_', '_'),
            'test_double_underscore': ('__', '__'),
            'test_triple_underscore': ('___', '___'),
            'test_spaces_underscores_combo': (' _ _ _', '______'),
            'test_spaces_underscores_combo_trailing_space': (' _ _ _ ', '______'),
            'test_leading_space': (' test', '_test'),
            'test_leading_spaces': ('   test', '___test'),
            'test_singe_trailing_space': ('test ', 'test'),
            'test_trailing_spaces': ('test   ', 'test'),
            'test_leading_and_trailing_space': (' test ', '_test'),
            'test_no_spaces': ('test', 'test'),
            'test_sentence': ('not the Spanish inquisition', 'not_the_Spanish_inquisition'),
            'test_sentence_leading_and_trailing_spaces': (' not the spanish inquisition ',
                                                          '_not_the_spanish_inquisition'),
            'test_combination_underscore_spaces': (
                ' because nobody_expects_the _spanish_ inquisition the 2nd time',
                '_because_nobody_expects_the__spanish__inquisition_the_2nd_time'),
            'test_combination_underscore_spaces_special_characters': (
                ' because nobody_expects_the !@#$%ing _spanish_ inquisition the 2nd ?~)*% time',
                '_because_nobody_expects_the_ing__spanish__inquisition_the_2nd__time')
            }

    @patch('dionysus_app.UI_menus.UI_functions.scrub_candidate_filename')
    def test_clean_for_filename_mocking_call(self, mocked_scrub_candidate_filename):
        """
        Mock call to scrub_candidate_filename.
        Essentially an input .replace(' ', '_') operation.
        """
        for test_case in self.test_cases:
            with self.subTest(i=self.test_cases[test_case]):
                test_input = self.test_cases[test_case][0]
                expected_output = test_input.replace(' ', '_')

                # Have scrub_candidate_filename return input_string.
                mocked_scrub_candidate_filename.return_value = test_input
                assert clean_for_filename(test_input) == expected_output

                mocked_scrub_candidate_filename.assert_called_once_with(test_input)
                mocked_scrub_candidate_filename.reset_mock(return_value=True, side_effect=True)

    def test_clean_for_filename_unmocked(self):
        for test_case in self.test_cases:
            with self.subTest(i=self.test_cases[test_case]):
                test_input = self.test_cases[test_case][0]
                expected_output = self.test_cases[test_case][1]

                assert clean_for_filename(test_input) == expected_output


class TestScrubCandidateFilename(TestCase):
    def setUp(self):
        # Test cases: (input_value, expected_return_value)
        self.test_cases = {
            'test_empty_string': ('', ''),  # ie no input
            # Spaces
            'test_single_space': (' ', ''),  # .rstrip() will remove trailing space.
            'test_2_spaces': ('  ', ''),
            'test_3_spaces': ('   ', ''),
            'test_5_spaces': ('     ', ''),
            # Underscores
            'test_single_underscore': ('_', '_'),
            'test_double_underscore': ('__', '__'),
            'test_triple_underscore': ('___', '___'),
            'test_spaces_underscores_combo': (' _ _ _', ' _ _ _'),
            'test_spaces_underscores_combo_trailing_space': (' _ _ _ ', ' _ _ _'),
            'test_leading_space': (' test', ' test'),
            'test_leading_spaces': ('   test', '   test'),
            'test_singe_trailing_space': ('test ', 'test'),
            'test_trailing_spaces': ('test   ', 'test'),
            'test_leading_and_trailing_space': (' test ', ' test'),
            'test_no_spaces': ('test', 'test'),
            'test_sentence': ('not the Spanish inquisition', 'not the Spanish inquisition'),
            'test_sentence_leading_and_trailing_spaces': (' not the spanish inquisition ',
                                                          ' not the spanish inquisition'),
            'test_combination_underscore_spaces': (
                ' because nobody_expects_the _spanish_ inquisition the 2nd time',
                ' because nobody_expects_the _spanish_ inquisition the 2nd time'),
            'test_combination_underscore_spaces_special_characters': (
                ' because nobody_expects_the !@#$%ing _spanish_ inquisition the 2nd ?~)*% time',
                ' because nobody_expects_the ing _spanish_ inquisition the 2nd  time')
            }

    def test_scrub_candidate_filename(self):
        for test_case in self.test_cases:
            with self.subTest(i=self.test_cases[test_case]):
                test_input = self.test_cases[test_case][0]
                expected_output = self.test_cases[test_case][1]

                assert scrub_candidate_filename(test_input) == expected_output


@patch('dionysus_app.UI_menus.UI_functions.tk.Tk')
class TestSaveAsDialogue(TestCase):
    def setUp(self):
        self.default_filetypes = [("all files", "*.*")]
        self.test_returned_filepath_str = "my save file"

    def test_save_as_dialogue_no_arguments(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            save_as_filedialog.return_value = self.test_returned_filepath_str
            assert save_as_filedialog.return_value == save_as_dialogue()

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=None,
                                                       filetypes=self.default_filetypes,
                                                       initialdir=None,
                                                       initialfile=None
                                                       )

    def test_save_as_dialogue_all_None_arguments(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(title_str=None,
                                    default_file_extension=None,
                                    filetypes=None,
                                    suggested_filename=None,
                                    start_dir=None
                                    ) == save_as_filedialog.return_value

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=None,
                                                       filetypes=self.default_filetypes,
                                                       initialdir=None,
                                                       initialfile=None,
                                                       )

    def test_save_as_dialogue_with_title_str(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            title_string = "Save your super_file_as:"

            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(title_str=title_string) == save_as_filedialog.return_value

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=title_string,
                                                       defaultextension=None,
                                                       filetypes=self.default_filetypes,
                                                       initialdir=None,
                                                       initialfile=None,
                                                       )

    def test_save_as_dialogue_with_default_extension_some_ext(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            test_default_extension = '.some_ext'

            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(default_file_extension=test_default_extension) == save_as_filedialog.return_value

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension='.some_ext',
                                                       filetypes=self.default_filetypes,
                                                       initialdir=None,
                                                       initialfile=None
                                                       )

    def test_save_as_dialogue_with_filetypes_all_files(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            test_filetypes = [("all files", "*.*")]

            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(filetypes=test_filetypes) == save_as_filedialog.return_value

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=None,
                                                       filetypes=self.default_filetypes,
                                                       initialdir=None,
                                                       initialfile=None
                                                       )

    def test_save_as_dialogue_with_filetypes_some_ext(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            test_filetypes = [('some ext', '*.some_ext')]
            test_default_extension = '.some_ext'

            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(default_file_extension=test_default_extension,
                                    filetypes=test_filetypes
                                    ) == self.test_returned_filepath_str

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=test_default_extension,
                                                       filetypes=test_filetypes,
                                                       initialdir=None,
                                                       initialfile=None,
                                                       )

    def test_save_as_dialogue_with_filetypes_all_files_plus_some_ext(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            test_filetypes = [('all files', '*.*'), ('some ext', '*.some_ext')]

            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(filetypes=test_filetypes) == self.test_returned_filepath_str

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=None,
                                                       filetypes=test_filetypes,
                                                       initialdir=None,
                                                       initialfile=None,
                                                       )

    def test_save_as_dialogue_with_filetypes_some_ext_plus_all_files(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            test_filetypes = [('some ext', '*.some_ext'), ('all files', '*.*')]
            test_default_extension = '.some_ext'

            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(default_file_extension=test_default_extension,
                                    filetypes=test_filetypes,
                                    ) == save_as_filedialog.return_value

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=test_default_extension,
                                                       filetypes=test_filetypes,
                                                       initialdir=None,
                                                       initialfile=None,
                                                       )

    def test_save_as_dialogue_with_suggested_filename(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            test_suggested_filename = 'you should call your save file THIS'

            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(suggested_filename=test_suggested_filename) == self.test_returned_filepath_str

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=None,
                                                       filetypes=self.default_filetypes,
                                                       initialdir=None,
                                                       initialfile=test_suggested_filename,
                                                       )

    def test_save_as_dialogue_with_start_dir_str(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            test_start_dir = 'where to start?'

            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(start_dir=test_start_dir) == self.test_returned_filepath_str

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=None,
                                                       filetypes=self.default_filetypes,
                                                       initialdir=test_start_dir,
                                                       initialfile=None,
                                                       )

    def test_save_as_dialogue_with_start_dir_Path(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            test_start_dir = 'where to start?'
            test_start_dir_path = Path(test_start_dir)

            save_as_filedialog.return_value = self.test_returned_filepath_str

            assert save_as_dialogue(start_dir=test_start_dir_path) == self.test_returned_filepath_str

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=None,
                                                       filetypes=self.default_filetypes,
                                                       initialdir=test_start_dir_path,
                                                       initialfile=None,
                                                       )

    def test_save_as_dialogue_no_input_returns_None(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.asksaveasfilename') as save_as_filedialog:
            save_as_filedialog.return_value = ''

            assert save_as_dialogue() is None

            mock_tkinter.assert_called()
            save_as_filedialog.assert_called_once_with(title=None,
                                                       defaultextension=None,
                                                       filetypes=self.default_filetypes,
                                                       initialdir=None,
                                                       initialfile=None,
                                                       )


@patch('dionysus_app.UI_menus.UI_functions.tk.Tk')
class TestSelectFileDialogue(TestCase):
    def setUp(self):
        self.test_default_filetypes = [('all files', '*.*')]

        self.test_title_str = 'First you must answer three questions'
        self.test_filetypes = [('some ext', '*.some_ext'), ('all files', '*.*')]
        self.test_start_dir = 'What\\is\\your\\quest'

        self.test_returned_filepath_str = 'strange women lying in ponds distributing swords'

    def test_select_file_dialogue_called_without_arguments(self, mock_tkinter):
        # Tests filedialog called with default_filetypes.
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.askopenfilename') as select_filedialog:
            select_filedialog.return_value = self.test_returned_filepath_str

            assert select_file_dialogue() == self.test_returned_filepath_str

            mock_tkinter.assert_called()
            select_filedialog.assert_called_once_with(title=None,
                                                      filetype=self.test_default_filetypes,
                                                      initialdir=None)

    def test_select_file_dialogue_all_None_arguments(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.askopenfilename') as select_filedialog:
            select_filedialog.return_value = self.test_returned_filepath_str

            assert select_file_dialogue(title_str=None,
                                        filetypes=None,
                                        start_dir=None,
                                        ) == self.test_returned_filepath_str

            mock_tkinter.assert_called()
            select_filedialog.assert_called_once_with(title=None,
                                                      filetype=self.test_default_filetypes,
                                                      initialdir=None)

    def test_select_file_dialogue_called_with_all_arguments(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.askopenfilename') as select_filedialog:
            select_filedialog.return_value = self.test_returned_filepath_str

            assert select_file_dialogue(title_str=self.test_title_str,
                                        filetypes=self.test_filetypes,
                                        start_dir=self.test_start_dir,
                                        ) == self.test_returned_filepath_str

            mock_tkinter.assert_called()
            select_filedialog.assert_called_once_with(title=self.test_title_str,
                                                      filetype=self.test_filetypes,
                                                      initialdir=self.test_start_dir)

    def test_select_file_dialogue_no_input_returns_None(self, mock_tkinter):
        with patch('dionysus_app.UI_menus.UI_functions.filedialog.askopenfilename') as select_filedialog:
            select_filedialog.return_value = ''

            assert select_file_dialogue() is None

            mock_tkinter.assert_called()
            select_filedialog.assert_called_once_with(title=None,
                                                      filetype=self.test_default_filetypes,
                                                      initialdir=None)
