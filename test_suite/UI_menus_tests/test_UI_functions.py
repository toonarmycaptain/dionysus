""""Test UI Functions"""

import pytest

from pathlib import Path
from unittest import mock
from unittest.mock import patch

from dionysus_app.UI_menus import UI_functions
from dionysus_app.UI_menus.UI_functions import (ask_user_bool,
                                                clean_for_filename,
                                                clear_screen,
                                                input_is_essentially_blank,
                                                save_as_dialogue,
                                                scrub_candidate_filename,
                                                select_file_dialogue,
                                                select_folder_dialogue,
                                                )


class TestClearScreen:
    @pytest.mark.parametrize(
        'test_input, expected_print_output',
        [(50, 50 * '\n'),
         (1, '\n'),
         (5, 5 * '\n'),
         (99, 99 * '\n'),
         ])
    def test_clear_screen(self, test_input, expected_print_output):
        with patch('dionysus_app.UI_menus.UI_functions.print') as mocked_print:
            clear_screen(test_input)

            mocked_print.assert_called_once_with(expected_print_output)


class TestInputIsEssentiallyBlank:
    @pytest.mark.parametrize(
        'test_input, expected_return_value',
        [('', True),  # empty string, ie no input.
         # Spaces
         (' ', True),  # single space
         ('  ', True),  # 2_spaces
         ('   ', True),  # 3_spaces
         ('     ', True),  # 5_spaces
         # Underscores
         ('_', True),  # single underscore
         ('__', True),  # 2 underscores
         ('___', True),  # 3 underscores
         ('_____', True),  # 5 underscores

         ('''~`!@#$%^&*()-_+{}[]|\\:;"',.<>?/''', True),  # only_special_characters
         (' test', False),  # singe leading space
         (' _ _ _', True),  # spaces underscores combo
         ('   test', False),  # leading spaces
         ('test ', False),  # singe trailing space
         ('test   ', False),  # trailing spaces
         (' test ', False),  # leading and trailing space
         ('test', False),  # no spaces
         ('not the Spanish inquisition', False),  # sentence
         (' not the spanish inquisition ', False),  # sentence leading and trailing spaces
         # test_combination underscore spaces
         (" because nobody_expects_the _spanish_ inquisition the 2nd time", False),
         # combination underscore spaces special characters
         (" because nobody_expects_the !@#$%ing _spanish_ inquisition the 2nd ?~)*% time", False),
         ])
    def test_input_is_essentially_blank(self, test_input, expected_return_value):
        assert input_is_essentially_blank(test_input) == expected_return_value


@pytest.mark.parametrize(
    'test_input, expected_return_value',
    [('', ''),  # empty string, ie no input
     # Spaces
     (' ', ''),  # .rstrip() will remove trailing space, single_space
     ('  ', ''),  # 2 spaces
     ('   ', ''),  # 3 spaces
     ('     ', ''),  # 5 spaces
     # Underscores
     ('_', '_'),  # single underscore
     ('__', '__'),  # double underscore
     ('___', '___'),  # triple underscore
     (' _ _ _', '______'),  # spaces underscores combo
     (' _ _ _ ', '______'),  # spaces underscores combo trailing space
     (' test', '_test'),  # leading space
     ('   test', '___test'),  # leading spaces
     ('test ', 'test'),  # singe trailing space
     ('test   ', 'test'),  # trailing spaces
     (' test ', '_test'),  # leading and trailing space
     ('test', 'test'),  # no spaces
     ('not the Spanish inquisition', 'not_the_Spanish_inquisition'),  # sentence
     (' not the spanish inquisition ',  # sentence leading and trailing spaces
      '_not_the_spanish_inquisition'),
     # Combination underscore spaces.
     (' because nobody_expects_the _spanish_ inquisition the 2nd time',
      '_because_nobody_expects_the__spanish__inquisition_the_2nd_time'),
     # Combination underscore spaces special characters.
     (' because nobody_expects_the !@#$%ing _spanish_ inquisition the 2nd ?~)*% time',
      '_because_nobody_expects_the______ing__spanish__inquisition_the_2nd_______time'),
     # Explicitly test OS/Filesystem format prohibited characters:
     # Prohibited chars FAT32:
     (r'" * / : < > ? \ | + , . ; = [ ] ! @ ; ', '_____________________________________'),
     # Prohibited characters Windows:
     (r'\/:*?"<>|.', '__________'),
     # Prohibited characters *nix/OSX chars:
     (r'*?!/.', '_____'),
     ])
class TestCleanForFilename:
    def test_clean_for_filename_mocking_call(self, monkeypatch,
                                             test_input, expected_return_value):
        """
        Mock call to scrub_candidate_filename.
        Essentially an input .replace(' ', '_') operation, unless behaviour changes.
        """

        def mocked_scrub_candidate_filename(test_string):
            assert test_string == test_input
            return test_input

        monkeypatch.setattr(UI_functions, 'scrub_candidate_filename', mocked_scrub_candidate_filename)

        assert clean_for_filename(test_input) == test_input.replace(' ', '_')

    def test_clean_for_filename_unmocked(self, test_input, expected_return_value):
        assert clean_for_filename(test_input) == expected_return_value


@pytest.mark.parametrize(
    'test_input, expected_output',
    [('', ''),  # test_empty_string
     (' ', ''),  # test_single_space
     ('  ', ''),  # test_2_spaces
     ('   ', ''),  # test_3_spaces
     ('     ', ''),  # test_5_spaces
     ('_', '_'),  # test_single_underscore
     ('__', '__'),  # test_double_underscore
     ('___', '___'),  # test_triple_underscore
     (' _ _ _', ' _ _ _'),  # test_spaces_underscores_combo
     (' _ _ _ ', ' _ _ _'),  # test_spaces_underscores_combo_trailing_space
     (' test', ' test'),  # test_leading_space
     ('   test', '   test'),  # test_leading_spaces
     ('test ', 'test'),  # test_singe_trailing_space
     ('test   ', 'test'),  # test_trailing_spaces
     (' test ', ' test'),  # test_leading_and_trailing_space
     ('test', 'test'),  # test_no_spaces
     ('not the Spanish inquisition', 'not the Spanish inquisition'),  # test_sentence
     (' not the spanish inquisition ', ' not the spanish inquisition'),  # test_sentence_leading_and_trailing_spaces
     (' because nobody_expects_the _spanish_ inquisition the 2nd time',
      ' because nobody_expects_the _spanish_ inquisition the 2nd time'),  # test_combination_underscore_spaces
     # test_combination_underscore_spaces_special_characters
     (' because nobody_expects_the !@#$%ing _spanish_ inquisition the 2nd ?~)*% time',
      ' because nobody_expects_the _____ing _spanish_ inquisition the 2nd _____ time'),
     # d'Artagnan's memoirs: preserving accented é, replacing apostrophe, period with underscores.
     ("Les mémoires de M. d'Artagnan", "Les mémoires de M_ d_Artagnan"),
     # Test prohibited chars FAT32
     (r'" * / : < > ? \ | + , . ; = [ ] ! @ ; ', '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _'),
     # Test prohibited characters Windows
     (r'\/:*?"<>|.', '__________'),
     # Test prohibited *nix/OSX chars
     (r'*?!/.', '_____'),
     ])
def test_scrub_candidate_filename(test_input, expected_output):
    assert scrub_candidate_filename(test_input) == expected_output


# ask_user_bool test cases:
# Blank or junk inputs:
no_user_input = ''
space_input = ' '
underscore_input = '_'
junk_input_knights = 'the knights who say ni'
junk_input_questions = ('First you must answer three questions: \n'
                        'What is your name?\n'
                        'What is your quest?\n'
                        'What is your favourite colour?')
# Valid inputs:
# 'No' inputs:
n_input = 'n', False
N_input = 'N', False
no_input = 'no', False
NO_input = 'NO', False
# 'Yes' inputs:
y_input = 'y', True
Y_input = 'Y', True
yes_input = 'yes', True
YES_input = 'YES', True

blank_junk_inputs = [no_user_input, space_input, underscore_input, junk_input_knights, junk_input_questions]
valid_inputs = [n_input, N_input, no_input, NO_input, y_input, Y_input, yes_input, YES_input]


class TestAskUserBool:
    @pytest.mark.parametrize(
        'test_inputs, return_value',
        [[blank_junk_inputs + [valid_input[0]],
          valid_input[1]] for valid_input in valid_inputs])
    def test_ask_user_bool(self, test_inputs, return_value):
        with mock.patch('builtins.input', side_effect=test_inputs):
            assert ask_user_bool('something', 'bad answer') == return_value


# Patching Tk doesn't affect test but not doing so slows down test 10x.
# Pass to test func as mock_tk
@patch('dionysus_app.UI_menus.UI_functions.tk.Tk')
class TestSaveAsDialogue:
    @pytest.mark.parametrize(
        'save_as_dialog_args, expected_filedialog_args, test_filename, returned_filepath',
        [({}, {}, "my save file", Path("my save file")),  # No args.
         pytest.param({}, {'filetypes': 'should be the default', 'initialdir': 'starting directory: ".." '},
                      "my_save_file", Path("my_save_file"),
                      marks=pytest.mark.xfail(reason="Test diagnostic.")),
         ({'title_str': None,  # None args passed to save_as_dialog
           'default_file_extension': None,
           'filetypes': None,
           'suggested_filename': None,
           'start_dir': None},
          {'initialdir': None},  # None dir passed on, default_filetypes subst by func.
          "my_save_file", Path("my_save_file")),
         # Title string.
         ({'title_str': "Save your super_file_as:"},
          {'title': "Save your super_file_as:"},
          "my_save_file", Path("my_save_file")),
         # Default extension.
         ({'default_file_extension': '.some_ext'},
          {'defaultextension': '.some_ext'},
          "my_save_file", Path("my_save_file.some_ext")),
         # Passing all files works same as no arg, since all files is default.
         ({'filetypes': [("all files", "*.*")]},
          {},
          "my_save_file", Path("my_save_file")),
         # Pass a filetypes with no default, and it becomes default extension.
         ({'filetypes': [('some ext', '*.some_ext')]},
          {'filetypes': [('some ext', '*.some_ext')],
           'defaultextension': '.some_ext'},
          "my_save_file", Path("my_save_file.some_ext")),
         # Test default extension and filetype
         ({'filetypes': [('some ext', '*.some_ext')],
           'default_file_extension': '.some_ext'},
          {'filetypes': [('some ext', '*.some_ext')],
           'defaultextension': '.some_ext'},
          "my_save_file", Path("my_save_file.some_ext")),
         # Test default extension different from first filetypes
         ({'filetypes': [('a ext', '*.a_ext'), ('b ext', '*.b_ext')],
           'default_file_extension': '.b_ext'},
          {'filetypes': [('a ext', '*.a_ext'), ('b ext', '*.b_ext')],
           'defaultextension': '.b_ext'},
          "my_save_file", Path("my_save_file.b_ext")),
         # Test default extension is default/first of multiple filetypes.
         ({'filetypes': [('a ext', '*.a_ext'), ('b ext', '*.b_ext')]},
          {'filetypes': [('a ext', '*.a_ext'), ('b ext', '*.b_ext')],
           'defaultextension': '.a_ext'},
          "my_save_file", Path("my_save_file.a_ext")),
         # Test no default extension when multiple filetypes passed with all files first.
         ({'filetypes': [("all files", "*.*"), ('a ext', '*.a_ext'), ('b ext', '*.b_ext')]},
          {'filetypes': [("all files", "*.*"), ('a ext', '*.a_ext'), ('b ext', '*.b_ext')],
           'defaultextension': None},
          "my_save_file", Path("my_save_file")),
         # Test default extension when multiple filetypes passed with all files not first.
         ({'filetypes': [('a ext', '*.a_ext'), ("all files", "*.*"), ('b ext', '*.b_ext')]},
          {'filetypes': [('a ext', '*.a_ext'), ("all files", "*.*"), ('b ext', '*.b_ext')],
           'defaultextension': '.a_ext'},
          "my_save_file", Path("my_save_file.a_ext")),
         # Test passing default filename, with user using default.
         ({'suggested_filename': 'save as this'},
          {'initialfile': 'save as this'},
          "save as this", Path("save as this")),
         # Test passing default filename, but returning another.
         ({'suggested_filename': 'save as this'},
          {'initialfile': 'save as this'},
          "user filename", Path("user filename")),
         # Test passing str starting directory.
         ({'start_dir': 'some start dir'},
          {'initialdir': 'some start dir'},
          "my_save_file", Path("my_save_file")),
         # Test passing Path starting directory.
         ({'start_dir': Path('some start dir')},
          {'initialdir': Path('some start dir')},
          "my_save_file", Path("my_save_file")),
         # Test no user input returns None.
         ({}, {}, '', None),
         ({}, {}, (), None),
         ])
    def test_save_as_dialogue(self, mock_tk, monkeypatch,
                              save_as_dialog_args,
                              expected_filedialog_args,
                              test_filename,
                              returned_filepath,):
        default_filetypes = [("all files", "*.*")]
        default_start_dir = '..'

        def mocked_filedialog_asksaveasfilename(title,
                                                defaultextension,
                                                filetypes,
                                                initialfile,
                                                initialdir,
                                                ):
            """
            Test arguments passed to filedialog are as expected, subbing with defaults save_as_dialogue
            will supply if no value is passed (equivalent to expecting the default).
            """
            assert title == expected_filedialog_args.get('title', None)
            assert defaultextension == expected_filedialog_args.get('defaultextension', None)
            assert filetypes == expected_filedialog_args.get('filetypes', default_filetypes)
            assert initialfile == expected_filedialog_args.get('initialfile', None)
            assert initialdir == expected_filedialog_args.get('initialdir', default_start_dir)
            # Return null test_filename value or filename + extension if present.
            if not test_filename:
                return test_filename
            return test_filename + (expected_filedialog_args.get('defaultextension', '') or '')

        monkeypatch.setattr(UI_functions.filedialog, 'asksaveasfilename', mocked_filedialog_asksaveasfilename)

        assert returned_filepath == save_as_dialogue(**save_as_dialog_args)


# Patching Tk doesn't affect test but not doing so slows down test 10x.
# Pass to test func as mock_tk
@patch('dionysus_app.UI_menus.UI_functions.tk.Tk')
class TestSelectFileDialogue:
    @pytest.mark.parametrize(
        'select_file_dialogue_args, expected_askopenfilename_args, test_filename, returned_filepath',
        [({}, {}, "my save file", Path("my save file")),  # No args.
         pytest.param({}, {'filetypes': 'should be the default', 'initialdir': 'starting directory: ".." '},
                      "my_save_file", Path("some_other_file"),
                      marks=pytest.mark.xfail(reason="Test diagnostic.")),
         ({'title_str': None,  # None args passed to select_file_dialog
           'filetypes': None,
           'start_dir': None},
          {'initialdir': None},  # None dir passed on, default_filetypes subst by func.
          "my_save_file", Path("my_save_file")),
         # All args passed to select_file_dialog
         ({'title_str': 'Some title string',
           'filetypes': [('some ext', '*.some_ext'), ('all files', '*.*')],
           'start_dir': Path(r'start/here')},
          {'title': 'Some title string',
           'filetypes': [('some ext', '*.some_ext'), ('all files', '*.*')],
           'initialdir': Path(r'start/here')},
          "my save file", Path("my save file")),
         # No user input/cancel (ie filename = () or '') returns None
         ({}, {}, '', None),
         ({}, {}, (), None),
         ])
    def test_select_file_dialogue(self, mock_tk, monkeypatch,
                                  select_file_dialogue_args,
                                  expected_askopenfilename_args,
                                  test_filename,
                                  returned_filepath):
        default_filetypes = [("all files", "*.*")]
        default_start_dir = '..'

        def mocked_filedialog_askopenfilename(title,
                                              filetypes,
                                              initialdir,
                                              ):
            """
            Test arguments passed to filedialog are as expected, subbing with defaults save_as_dialogue
            will supply if no value is passed (equivalent to expecting the default).
            """
            assert title == expected_askopenfilename_args.get('title', None)
            assert filetypes == expected_askopenfilename_args.get('filetypes', default_filetypes)
            assert initialdir == expected_askopenfilename_args.get('initialdir', default_start_dir)
            # Return null test_filename value or filename + extension if present.
            if not test_filename:
                return test_filename
            return test_filename + (expected_askopenfilename_args.get('defaultextension', '') or '')

        monkeypatch.setattr(UI_functions.filedialog, 'askopenfilename', mocked_filedialog_askopenfilename)

        assert returned_filepath == select_file_dialogue(**select_file_dialogue_args)


@patch('dionysus_app.UI_menus.UI_functions.tk.Tk')
class TestSelectFolderDialogue:
    @pytest.mark.parametrize(
        'select_folder_dialogue_args, expected_askdirectory_args, test_path, returned_path',
        [({}, {}, "my save dir", Path("my save dir")),  # No args.
         pytest.param({}, {'initialdir': 'starting directory: ".." '},
                      "my_save_dir", Path("some_other_dir"),
                      marks=pytest.mark.xfail(reason="Test diagnostic.")),
         # None args passed to select_file_dialog
         ({'title_str': None,
           'start_dir': None},
          {'initialdir': None},  # None dir passed on.
          "my_save_dir", Path("my_save_dir")),
         # # All args passed to select_file_dialog
         ({'title_str': 'Some title string',
           'start_dir': Path(r'start/here')},
          {'title': 'Some title string',
           'initialdir': Path(r'start/here')},
          "my save dir", Path("my save dir")),
         # No user input/cancel (ie dirpath = '' or ()) returns None
         ({}, {}, '', None),
         ({}, {}, (), None),
         ])
    def test_select_folder_dialogue(self, mock_tk, monkeypatch,
                                    select_folder_dialogue_args,
                                    expected_askdirectory_args,
                                    test_path,
                                    returned_path):
        default_start_dir = '..'

        def mocked_filedialog_askdirectory(title,
                                           initialdir,
                                           ):
            """
            Test arguments passed to filedialog are as expected, subbing with defaults save_as_dialogue
            will supply if no value is passed (equivalent to expecting the default).
            """
            assert title == expected_askdirectory_args.get('title', None)
            assert initialdir == expected_askdirectory_args.get('initialdir', default_start_dir)

            return test_path

        monkeypatch.setattr(UI_functions.filedialog, 'askdirectory', mocked_filedialog_askdirectory)

        assert returned_path == select_folder_dialogue(**select_folder_dialogue_args)
