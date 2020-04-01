"""Test data_version_conversion.py"""
import json

from argparse import Namespace
from pathlib import Path

import pytest

import data_version_conversion

from data_version_conversion import (CLASSLIST_DATA_PATH,
                                     data_is_new_format,
                                     file_from_gui_dialogue,
                                     get_data_file,
                                     main,
                                     parse_args,
                                     run_script,
                                     transform_data,
                                     transform_all_old_data_files,
                                     transform_old_cld_file,
                                     )
from dionysus_app.class_ import Class
from dionysus_app.data_folder import CLASSLIST_DATA_FILE_TYPE

from test_suite.test_class import test_class_name_only


class TestMain:
    @pytest.mark.parametrize(
        'all_files_arg, filepath_arg',
        [(False, None),  # No args
         (True, None),  # All files arg passed.
         (False, 'some file'),  # File arg passed.
         (True, 'some file'),  # Both args passed.
         ])
    def test_parse_args(self, monkeypatch, all_files_arg, filepath_arg):
        def mocked_run_script(args):
            if args != Namespace(all_class_data_files=all_files_arg, filepath=filepath_arg):
                raise ValueError

        def mocked_parse_args(_):
            return Namespace(all_class_data_files=all_files_arg, filepath=filepath_arg)

        monkeypatch.setattr(data_version_conversion, 'parse_args', mocked_parse_args)
        monkeypatch.setattr(data_version_conversion, 'run_script', mocked_run_script)

        assert main() is None


class TestParseArgs:
    @pytest.mark.parametrize(
        'test_args, expected_returned_value',
        [([], Namespace(all_class_data_files=False, filepath=None)),  # No args
         (['--filepath=some.file'], Namespace(all_class_data_files=False, filepath='some.file')),  # File arg passed.
         (['--f=some.file'], Namespace(all_class_data_files=False, filepath='some.file')),  # Sort file arg passed.
         (['--all_class_data_files'], Namespace(all_class_data_files=True, filepath=None)),  # All files arg passed.
         (['-A'], Namespace(all_class_data_files=True, filepath=None)),  # Sort files arg passed.
         ])
    def test_parse_args(self, monkeypatch, test_args, expected_returned_value):
        assert parse_args(test_args) == expected_returned_value

    @pytest.mark.parametrize(
        'test_args',
        [(['-f']),  # -f passed instead of --f.
         (['--f']),  # --f passed without filename arg.
         (['--filepath']),  # --filepath passed without filename arg.
         (['--all_class_data_files', '--filepath=some.file']),  # Both args passed, with file argument.
         (['--all_class_data_files', '--filepath']),  # Both args passed, without file argument.
         (['--A']),  # --A passed instead of -A.
         (['-A', '--f=some.file']),  # Both short args passed, with file argument.
         (['-A', '--f']),  # Both short args passed, without file argument.
         ])
    def test_parse_args_raising_exception(self, monkeypatch, test_args):
        with pytest.raises(SystemExit):
            parse_args(test_args)


class TestRunScript:
    @pytest.mark.parametrize(
        'test_args, expected_function',
        [(Namespace(all_class_data_files=False, filepath=None),  # No args
          'mocked file_from_gui_dialogue called'),
         (Namespace(all_class_data_files=False, filepath='some.file'),  # File arg passed.
          'mocked transform_old_cld_file called'),
         (Namespace(all_class_data_files=True, filepath=None),  # All files arg passed.
          'mocked transform_all_old_data_files called'),
         ])
    def test_run_script(self, monkeypatch, test_args, expected_function):
        def mocked_transform_all_old_data_files():
            if expected_function != 'mocked transform_all_old_data_files called':
                raise ValueError

        def mocked_transform_old_cld_file(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            if expected_function != 'mocked transform_old_cld_file called':
                raise ValueError

        def mocked_file_from_gui_dialogue():
            if expected_function != 'mocked file_from_gui_dialogue called':
                raise ValueError

        monkeypatch.setattr(data_version_conversion,
                            'transform_all_old_data_files', mocked_transform_all_old_data_files)
        monkeypatch.setattr(data_version_conversion,
                            'transform_old_cld_file', mocked_transform_old_cld_file)
        monkeypatch.setattr(data_version_conversion,
                            'file_from_gui_dialogue', mocked_file_from_gui_dialogue)

        assert run_script(test_args) is None


class TestTransformAllOldDataFiles:
    def test_transform_all_old_data_files(self, monkeypatch):
        test_file_paths = [Path('first/path'), Path('second/path')]

        def mocked_path_glob(self, cld_pattern):
            if cld_pattern != '**/*.cld':
                raise ValueError
            return (test_path for test_path in test_file_paths)

        def mocked_transform_old_cld_file(arg):
            if not isinstance(arg, Path):
                raise TypeError
            if arg not in test_file_paths:
                raise ValueError

        monkeypatch.setattr(data_version_conversion.Path, 'glob', mocked_path_glob)
        monkeypatch.setattr(data_version_conversion, 'transform_old_cld_file', mocked_transform_old_cld_file)

        assert transform_all_old_data_files() is None


class TestTransformOldCldFile:
    def test_transform_old_cld_file_nonexistent_path(self, monkeypatch, capsys):
        test_filepath = Path('hi//I//do//not//exist.oops')
        error_statement = f'File {test_filepath} does not exist.'

        def mocked_path_exists(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            return False

        monkeypatch.setattr(data_version_conversion.Path, 'exists', mocked_path_exists)

        assert transform_old_cld_file(test_filepath) is None

        captured = capsys.readouterr().out
        assert error_statement in captured
        # 'in' workaround to avoid playing with differing newlines in statement and output.

    def test_transform_old_cld_file_json_decode_error(self, monkeypatch, capsys):
        test_filepath = Path('hi//I//do//exist.yay')
        error_statement = (f'Something went wrong with decoding {test_filepath}:\n'
                           f'The file might be corrupted or is not a supported format.\n')

        def mocked_path_exists(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            return True

        def mocked_load_from_json_file(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            raise json.decoder.JSONDecodeError(msg='Wow', doc='#bad doc#', pos=1)

        monkeypatch.setattr(data_version_conversion.Path, 'exists', mocked_path_exists)
        monkeypatch.setattr(data_version_conversion, 'load_from_json_file', mocked_load_from_json_file)

        assert transform_old_cld_file(test_filepath) is None

        captured = capsys.readouterr().out
        assert captured == error_statement

    def test_transform_old_cld_file_already_in_new_format(self, monkeypatch, test_class_name_only, capsys):
        test_filepath = Path('hi//I//do//exist.yay')
        error_statement = f'It looks like {test_filepath.name} is already in the new format.'

        def mocked_path_exists(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            return True

        def mocked_load_from_json_file(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            return test_class_name_only.json_dict()

        def mocked_data_is_new_format(json_dict):
            if not isinstance(json_dict, dict):
                raise TypeError
            return True

        monkeypatch.setattr(data_version_conversion.Path, 'exists', mocked_path_exists)
        monkeypatch.setattr(data_version_conversion, 'load_from_json_file', mocked_load_from_json_file)
        monkeypatch.setattr(data_version_conversion, 'data_is_new_format', mocked_data_is_new_format)

        assert transform_old_cld_file(test_filepath) is None

        captured = capsys.readouterr().out
        assert error_statement in captured
        # 'in' workaround to avoid playing with differing newlines in statement and output.

    def test_transform_old_cld_file_genuine_old_file(self, monkeypatch, test_class_name_only, capsys):

        mocked_CLASSLIST_DATA_PATH = Path(f'hi//I//do//')
        test_filepath = Path(mocked_CLASSLIST_DATA_PATH).joinpath(test_class_name_only.path_safe_name,
                                                                  f'{test_class_name_only.path_safe_name}.yay')
        new_data_filepath = test_filepath.parent.joinpath(
            test_class_name_only.path_safe_name + CLASSLIST_DATA_FILE_TYPE)

        feedback_statement = f'Transformed {test_class_name_only.name} data file to new data format in {new_data_filepath}'

        def mocked_path_exists(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            return True

        def mocked_load_from_json_file(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            return test_class_name_only.json_dict()

        def mocked_data_is_new_format(json_dict):
            if not isinstance(json_dict, dict):
                raise TypeError
            return False

        def mocked_transform_data(class_name, class_data_dict):
            if not isinstance(class_name, str):
                raise TypeError
            if not isinstance(class_data_dict, dict):
                raise TypeError
            return test_class_name_only

        def mocked_write_classlist_to_file(test_class):
            if not isinstance(test_class, Class):
                raise TypeError
            return new_data_filepath

        monkeypatch.setattr(data_version_conversion.Path, 'exists', mocked_path_exists)
        monkeypatch.setattr(data_version_conversion, 'load_from_json_file', mocked_load_from_json_file)
        monkeypatch.setattr(data_version_conversion, 'data_is_new_format', mocked_data_is_new_format)
        monkeypatch.setattr(data_version_conversion, 'transform_data', mocked_transform_data)
        monkeypatch.setattr(data_version_conversion, 'write_classlist_to_file', mocked_write_classlist_to_file)
        monkeypatch.setattr(data_version_conversion, 'CLASSLIST_DATA_PATH', mocked_CLASSLIST_DATA_PATH)

        assert transform_old_cld_file(test_filepath) is None

        captured = capsys.readouterr().out
        assert feedback_statement in captured
        # 'in' workaround to avoid playing with differing newlines in statement and output.


class TestDataIsOldFormat:
    def test_data_is_new_format_with_new_data_style(self, test_class_name_only):
        class_data = test_class_name_only.json_dict()

        assert data_is_new_format(class_data) is True

    def test_data_is_new_format_with_old_data_style(self):
        class_data = {'some_student': ['some_avatar.jpg'], 'some other student': [None]}

        assert data_is_new_format(class_data) is False


class TestTransformData:
    def setup_method(self):
        self.old_format_class_name = "huge 53 student class"
        self.old_format_json_str = '{\n    "student 0": [\n        "myavatar.jpg"\n    ],\n    "student 1": [\n        null\n    ],\n    "student 2": [\n        null\n    ],\n    "student 3": [\n        null\n    ],\n    "student 4": [\n        null\n    ],\n    "student 5": [\n        null\n    ],\n    "student 6": [\n        null\n    ],\n    "student 7": [\n        null\n    ],\n    "student 8": [\n        null\n    ],\n    "student 9": [\n        null\n    ],\n    "student 10": [\n        null\n    ],\n    "student 11": [\n        null\n    ],\n    "student 12": [\n        null\n    ],\n    "student 13": [\n        null\n    ],\n    "student 14": [\n        null\n    ],\n    "student 15": [\n        null\n    ],\n    "student 16": [\n        null\n    ],\n    "student 17": [\n        null\n    ],\n    "student 18": [\n        null\n    ],\n    "student 19": [\n        null\n    ],\n    "student 20": [\n        null\n    ],\n    "student 21": [\n        null\n    ],\n    "student 22": [\n        null\n    ],\n    "student 23": [\n        null\n    ],\n    "student 24": [\n        null\n    ],\n    "student 25": [\n        null\n    ],\n    "student 26": [\n        null\n    ],\n    "student 27": [\n        null\n    ],\n    "student 28": [\n        null\n    ],\n    "student 29": [\n        null\n    ],\n    "student 30": [\n        null\n    ],\n    "student 31": [\n        null\n    ],\n    "student 32": [\n        null\n    ],\n    "student 33": [\n        null\n    ],\n    "student 34": [\n        null\n    ],\n    "student 35": [\n        null\n    ],\n    "student 36": [\n        null\n    ],\n    "student 37": [\n        null\n    ],\n    "student 38": [\n        null\n    ],\n    "student 39": [\n        null\n    ],\n    "student 40": [\n        null\n    ],\n    "student 41": [\n        null\n    ],\n    "student 42": [\n        null\n    ],\n    "student 43": [\n        null\n    ],\n    "student 44": [\n        null\n    ],\n    "student 45": [\n        null\n    ],\n    "student 46": [\n        null\n    ],\n    "student 47": [\n        null\n    ],\n    "student 48": [\n        null\n    ],\n    "student 49": [\n        "seven_squared.gif"\n    ],\n    "student 50": [\n        null\n    ],\n    "student 51": [\n        "some_pic.png"\n    ],\n    "student 52": [\n        null\n    ]\n}'
        self.old_format_json_dict = {'student 0': ['myavatar.jpg'],
                                     'student 1': [None],
                                     'student 2': [None],
                                     'student 3': [None],
                                     'student 4': [None],
                                     'student 5': [None],
                                     'student 6': [None],
                                     'student 7': [None],
                                     'student 8': [None],
                                     'student 9': [None],
                                     'student 10': [None],
                                     'student 11': [None],
                                     'student 12': [None],
                                     'student 13': [None],
                                     'student 14': [None],
                                     'student 15': [None],
                                     'student 16': [None],
                                     'student 17': [None],
                                     'student 18': [None],
                                     'student 19': [None],
                                     'student 20': [None],
                                     'student 21': [None],
                                     'student 22': [None],
                                     'student 23': [None],
                                     'student 24': [None],
                                     'student 25': [None],
                                     'student 26': [None],
                                     'student 27': [None],
                                     'student 28': [None],
                                     'student 29': [None],
                                     'student 30': [None],
                                     'student 31': [None],
                                     'student 32': [None],
                                     'student 33': [None],
                                     'student 34': [None],
                                     'student 35': [None],
                                     'student 36': [None],
                                     'student 37': [None],
                                     'student 38': [None],
                                     'student 39': [None],
                                     'student 40': [None],
                                     'student 41': [None],
                                     'student 42': [None],
                                     'student 43': [None],
                                     'student 44': [None],
                                     'student 45': [None],
                                     'student 46': [None],
                                     'student 47': [None],
                                     'student 48': [None],
                                     'student 49': ['seven_squared.gif'],
                                     'student 50': [None],
                                     'student 51': ['some_pic.png'],
                                     'student 52': [None]}

        self.new_format_json_str = '{\n    "name": "huge 53 student class",\n    "students": [\n        {\n            "name": "student 0",\n            "avatar_filename": "myavatar.jpg"\n        },\n        {\n            "name": "student 1"\n        },\n        {\n            "name": "student 2"\n        },\n        {\n            "name": "student 3"\n        },\n        {\n            "name": "student 4"\n        },\n        {\n            "name": "student 5"\n        },\n        {\n            "name": "student 6"\n        },\n        {\n            "name": "student 7"\n        },\n        {\n            "name": "student 8"\n        },\n        {\n            "name": "student 9"\n        },\n        {\n            "name": "student 10"\n        },\n        {\n            "name": "student 11"\n        },\n        {\n            "name": "student 12"\n        },\n        {\n            "name": "student 13"\n        },\n        {\n            "name": "student 14"\n        },\n        {\n            "name": "student 15"\n        },\n        {\n            "name": "student 16"\n        },\n        {\n            "name": "student 17"\n        },\n        {\n            "name": "student 18"\n        },\n        {\n            "name": "student 19"\n        },\n        {\n            "name": "student 20"\n        },\n        {\n            "name": "student 21"\n        },\n        {\n            "name": "student 22"\n        },\n        {\n            "name": "student 23"\n        },\n        {\n            "name": "student 24"\n        },\n        {\n            "name": "student 25"\n        },\n        {\n            "name": "student 26"\n        },\n        {\n            "name": "student 27"\n        },\n        {\n            "name": "student 28"\n        },\n        {\n            "name": "student 29"\n        },\n        {\n            "name": "student 30"\n        },\n        {\n            "name": "student 31"\n        },\n        {\n            "name": "student 32"\n        },\n        {\n            "name": "student 33"\n        },\n        {\n            "name": "student 34"\n        },\n        {\n            "name": "student 35"\n        },\n        {\n            "name": "student 36"\n        },\n        {\n            "name": "student 37"\n        },\n        {\n            "name": "student 38"\n        },\n        {\n            "name": "student 39"\n        },\n        {\n            "name": "student 40"\n        },\n        {\n            "name": "student 41"\n        },\n        {\n            "name": "student 42"\n        },\n        {\n            "name": "student 43"\n        },\n        {\n            "name": "student 44"\n        },\n        {\n            "name": "student 45"\n        },\n        {\n            "name": "student 46"\n        },\n        {\n            "name": "student 47"\n        },\n        {\n            "name": "student 48"\n        },\n        {\n            "name": "student 49",\n            "avatar_filename": "seven_squared.gif"\n        },\n        {\n            "name": "student 50"\n        },\n        {\n            "name": "student 51",\n            "avatar_filename": "some_pic.png"\n        },\n        {\n            "name": "student 52"\n        }\n    ]\n}'
        self.new_format_json_dict = {'name': 'huge 53 student class',
                                     'students': [{'name': 'student 0', 'avatar_filename': 'myavatar.jpg'},
                                                  {'name': 'student 1'},
                                                  {'name': 'student 2'},
                                                  {'name': 'student 3'},
                                                  {'name': 'student 4'},
                                                  {'name': 'student 5'},
                                                  {'name': 'student 6'},
                                                  {'name': 'student 7'},
                                                  {'name': 'student 8'},
                                                  {'name': 'student 9'},
                                                  {'name': 'student 10'},
                                                  {'name': 'student 11'},
                                                  {'name': 'student 12'},
                                                  {'name': 'student 13'},
                                                  {'name': 'student 14'},
                                                  {'name': 'student 15'},
                                                  {'name': 'student 16'},
                                                  {'name': 'student 17'},
                                                  {'name': 'student 18'},
                                                  {'name': 'student 19'},
                                                  {'name': 'student 20'},
                                                  {'name': 'student 21'},
                                                  {'name': 'student 22'},
                                                  {'name': 'student 23'},
                                                  {'name': 'student 24'},
                                                  {'name': 'student 25'},
                                                  {'name': 'student 26'},
                                                  {'name': 'student 27'},
                                                  {'name': 'student 28'},
                                                  {'name': 'student 29'},
                                                  {'name': 'student 30'},
                                                  {'name': 'student 31'},
                                                  {'name': 'student 32'},
                                                  {'name': 'student 33'},
                                                  {'name': 'student 34'},
                                                  {'name': 'student 35'},
                                                  {'name': 'student 36'},
                                                  {'name': 'student 37'},
                                                  {'name': 'student 38'},
                                                  {'name': 'student 39'},
                                                  {'name': 'student 40'},
                                                  {'name': 'student 41'},
                                                  {'name': 'student 42'},
                                                  {'name': 'student 43'},
                                                  {'name': 'student 44'},
                                                  {'name': 'student 45'},
                                                  {'name': 'student 46'},
                                                  {'name': 'student 47'},
                                                  {'name': 'student 48'},
                                                  {'name': 'student 49', 'avatar_filename': 'seven_squared.gif'},
                                                  {'name': 'student 50'},
                                                  {'name': 'student 51', 'avatar_filename': 'some_pic.png'},
                                                  {'name': 'student 52'}]}

    def test_transform_data_dict(self):
        transformed_data = transform_data(self.old_format_class_name, self.old_format_json_dict)
        assert isinstance(transformed_data, Class)
        assert transformed_data.json_dict() == self.new_format_json_dict

    def test_transform_data_str(self):
        transformed_data = transform_data(self.old_format_class_name, self.old_format_json_dict)
        assert isinstance(transformed_data, Class)
        assert transformed_data.to_json_str() == self.new_format_json_str


class TestFileFromGuiDialogue:
    def test_file_from_gui_dialogue_no_file(self, monkeypatch, capsys):
        feedback_statement = 'No file selected.'

        def mocked_get_data_file():
            return None

        def mocked_transform_old_cld_file(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            raise ValueError  # Function should not be called.

        monkeypatch.setattr(data_version_conversion, 'get_data_file', mocked_get_data_file)
        monkeypatch.setattr(data_version_conversion, 'transform_old_cld_file', mocked_transform_old_cld_file)

        assert file_from_gui_dialogue() is None

        captured = capsys.readouterr().out
        assert feedback_statement in captured
        # 'in' workaround to avoid playing with differing newlines in statement and output.

    def test_file_from_gui_dialogue_given_file(self, monkeypatch):
        test_filepath = Path('some.path')

        def mocked_get_data_file():
            return test_filepath

        def mocked_transform_old_cld_file(filepath):
            if not isinstance(filepath, Path):
                raise TypeError
            if filepath != test_filepath:
                raise ValueError
            return None

        monkeypatch.setattr(data_version_conversion, 'get_data_file', mocked_get_data_file)
        monkeypatch.setattr(data_version_conversion, 'transform_old_cld_file', mocked_transform_old_cld_file)

        assert file_from_gui_dialogue() is None


class TestGetDataFile:
    def test_get_data_file_no_file(self, monkeypatch):
        def mocked_select_file_dialogue(title_str, filetypes, start_dir):
            assert isinstance(title_str, str) and isinstance(filetypes, list) and start_dir is CLASSLIST_DATA_PATH
            return None

        monkeypatch.setattr(data_version_conversion, 'select_file_dialogue', mocked_select_file_dialogue)

        assert get_data_file() is None

    def test_get_data_file_given_file(self, monkeypatch):
        test_filepath = Path('path/to/some.file')

        def mocked_select_file_dialogue(title_str, filetypes, start_dir):
            assert isinstance(title_str, str) and isinstance(filetypes, list) and start_dir is CLASSLIST_DATA_PATH
            return test_filepath

        monkeypatch.setattr(data_version_conversion, 'select_file_dialogue', mocked_select_file_dialogue)

        assert get_data_file() == test_filepath
