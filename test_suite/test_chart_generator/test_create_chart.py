from pathlib import Path

import pytest

import definitions

from dionysus_app.chart_generator import create_chart
from dionysus_app.chart_generator.create_chart import (assemble_chart_data,
                                                       copy_image_to_user_save_loc,
                                                       create_class_save_folder,
                                                       get_class_save_folder_path,
                                                       get_custom_chart_options,
                                                       get_user_save_chart_pathname,
                                                       new_chart,
                                                       sanitise_avatar_path_objects,
                                                       set_chart_params,
                                                       show_image,
                                                       write_chart_data_to_file,
                                                       user_save_chart_image,
                                                       )
from dionysus_app.chart_generator.process_chart_data import DEFAULT_CHART_PARAMS
from dionysus_app.class_ import Class, NewClass
from dionysus_app.data_folder import CHART_DATA_FILE_TYPE

from test_suite.test_class import test_full_class
from test_suite.testing_class_data import test_full_class_data_set


class TestNewChart:
    @pytest.mark.parametrize('class_from_create_class',
                             [None,
                              Class.from_dict(test_full_class_data_set['json_dict_rep']),  # Pass in test_class
                              NewClass.from_dict(test_full_class_data_set['json_dict_rep'])  # NewClass obj
                              ])
    def test_new_chart(self, monkeypatch, class_from_create_class, test_full_class):
        # Test class either passed, or instantiated if None is passed.
        test_class = class_from_create_class or test_full_class

        test_chart_name = 'test_chart_name'
        test_chart_default_filename = 'test_chart_default_filename'
        test_chart_params = {'test_chart_params': 'some chart params'}
        test_score_avatar_dict = {'test_student_scores': 'test student avatars'}

        test_chart_data_dict = {'class_name': test_class.name,
                                'chart_name': test_chart_name,
                                'chart_default_filename': test_chart_default_filename,
                                'chart_params': test_chart_params,
                                'score-avatar_dict': test_score_avatar_dict,
                                }

        test_chart_image_location = 'some image location'

        def mocked_select_classlist():
            if class_from_create_class:
                raise ValueError('Function should not be called if class is passed.')
            return test_class.name

        def mocked_load_class_from_disk(class_name):
            if class_from_create_class:
                raise ValueError('Function should not be called if class is passed.')
            return test_class

        def mocked_assemble_chart_data(class_obj):
            return (test_chart_name,
                    test_chart_default_filename,
                    test_score_avatar_dict,
                    test_chart_params)

        def mocked_write_chart_data_to_file(chart_data_dict):
            if chart_data_dict != test_chart_data_dict:
                raise ValueError

        def mocked_generate_chart_image(chart_data_dict):
            if chart_data_dict != test_chart_data_dict:
                raise ValueError
            return test_chart_image_location

        def mocked_show_image(chart_image_location):
            if chart_image_location != test_chart_image_location:
                raise ValueError

        def mocked_user_save_chart_image(chart_data_dict, chart_image_location):
            if chart_data_dict != test_chart_data_dict:
                raise ValueError
            if chart_image_location != test_chart_image_location:
                raise ValueError

        monkeypatch.setattr(create_chart, 'select_classlist', mocked_select_classlist)
        monkeypatch.setattr(create_chart, 'load_class_from_disk', mocked_load_class_from_disk)
        monkeypatch.setattr(create_chart, 'assemble_chart_data', mocked_assemble_chart_data)
        monkeypatch.setattr(create_chart, 'write_chart_data_to_file', mocked_write_chart_data_to_file)
        monkeypatch.setattr(create_chart, 'generate_chart_image', mocked_generate_chart_image)
        monkeypatch.setattr(create_chart, 'show_image', mocked_show_image)
        monkeypatch.setattr(create_chart, 'user_save_chart_image', mocked_user_save_chart_image)

        assert new_chart(class_from_create_class) is None


class TestAssembleChartData:
    @pytest.mark.parametrize('class_from_create_class',
                             [Class.from_dict(test_full_class_data_set['json_dict_rep']),  # Pass in test_class
                              NewClass.from_dict(test_full_class_data_set['json_dict_rep'])  # NewClass obj
                              ])
    def test_assemble_chart_data(self, monkeypatch, class_from_create_class):
        test_chart_name = 'my_chart'
        test_chart_filename = test_chart_name
        mock_score_avatar_dict = {'scores': 'list of avatars'}
        mock_chart_params = {'some': 'chart_params'}

        def mocked_take_score_data(class_obj):
            if class_obj is not class_from_create_class:
                raise ValueError
            return mock_score_avatar_dict

        def mocked_take_chart_name():
            return test_chart_name

        def mocked_clean_for_filename(chart_name):
            if chart_name != test_chart_name:
                raise ValueError
            return test_chart_name

        def mocked_set_chart_params():
            return mock_chart_params

        monkeypatch.setattr(create_chart, 'take_score_data', mocked_take_score_data)
        monkeypatch.setattr(create_chart, 'take_chart_name', mocked_take_chart_name)
        monkeypatch.setattr(create_chart, 'clean_for_filename', mocked_clean_for_filename)
        monkeypatch.setattr(create_chart, 'set_chart_params', mocked_set_chart_params)

        assert assemble_chart_data(class_from_create_class) == (
            test_chart_name, test_chart_filename, mock_score_avatar_dict, mock_chart_params)


class TestWriteChartDataToFile:
    def test_write_chart_data_to_file(self, monkeypatch, tmp_path):
        test_chart_data_dict = {'class_name': 'test_class_name',
                                'chart_name': 'test_chart_name',
                                'chart_default_filename': 'test_default_chart_filename',
                                'chart_params': {'some': 'params'},
                                'score-avatar_dict': {'some student': 'scores'}
                                }
        test_filename = test_chart_data_dict['chart_default_filename'] + CHART_DATA_FILE_TYPE
        test_file_folder = tmp_path.joinpath(test_chart_data_dict['class_name'], 'chart_data')
        test_file_folder.mkdir(parents=True, exist_ok=True)
        test_filepath = test_file_folder.joinpath(test_filename)

        test_text_written_to_file = 'A JSON string.'

        assert tmp_path.exists()
        assert test_file_folder.exists()

        def mocked_sanitise_avatar_path_objects(file_chart_data_dict):
            if file_chart_data_dict != test_chart_data_dict:
                raise ValueError('The dict of chart data did not contain expected items.')
            # file_chart_data_dict should be a deepcopy, not a reference to the original chart_data_dict.
            if file_chart_data_dict is test_chart_data_dict:
                raise ValueError("A reference to the original chart data dict was passed. \n"
                                 "An exact (deep)copy should be passed, because sanitise_avatar_path_objects \n"
                                 "will mutate ('sanitise') the dict passed to it.\n")

            return file_chart_data_dict

        def mocked_convert_to_json(json_safe_dict):
            if json_safe_dict != test_chart_data_dict:
                raise ValueError
            return test_text_written_to_file

        monkeypatch.setattr(create_chart, 'CLASSLIST_DATA_PATH', tmp_path)
        monkeypatch.setattr(create_chart, 'sanitise_avatar_path_objects', mocked_sanitise_avatar_path_objects)
        monkeypatch.setattr(create_chart, 'convert_to_json', mocked_convert_to_json)
        write_chart_data_to_file(test_chart_data_dict)

        assert test_filepath.exists()
        with open(test_filepath, 'r') as test_file:
            assert test_file.read() == test_text_written_to_file


class TestSetChartParams:
    def test_set_chart_params(self, monkeypatch):
        test_params = {'some': 'params'}

        def mocked_get_custom_chart_options(default_options):
            if default_options != DEFAULT_CHART_PARAMS:
                raise ValueError
            return test_params

        monkeypatch.setattr(create_chart, 'get_custom_chart_options', mocked_get_custom_chart_options)

        assert set_chart_params() == test_params


class TestGetCustomChartOptions:
    def test_get_custom_chart_options(self, monkeypatch):
        test_default_params = {'default param': 'my default param value'}

        take_custom_chart_options_mock = {'called': False}

        def mocked_take_custom_chart_options():
            take_custom_chart_options_mock['called'] = True

        monkeypatch.setattr(create_chart, 'take_custom_chart_options', mocked_take_custom_chart_options)

        assert get_custom_chart_options(test_default_params) == test_default_params

        assert take_custom_chart_options_mock['called']


class TestSanitiseAvatarPathObjects:
    def test_santise_avatar_path_objects(self):
        mock_default_avatar_path = Path('default/path')
        str_mock_default_avatar_path = str(mock_default_avatar_path)
        test_data_dict = {
            'class_name': "test_class_name",
            'chart_name': "test_chart_name",
            'chart_default_filename': "test_chart_default_filename",
            'chart_params': {"some": "chart", "default": "params"},
            'score-avatar_dict': {0: [Path('path to Cali_avatar.png')],
                                  1: [mock_default_avatar_path, mock_default_avatar_path],
                                  3: [mock_default_avatar_path, mock_default_avatar_path],
                                  50: [mock_default_avatar_path],
                                  99: [mock_default_avatar_path],
                                  100: [mock_default_avatar_path],
                                  2: [Path('path to Ashley_avatar.png')],
                                  4: [mock_default_avatar_path],
                                  6: [Path('path to Danielle.png')],
                                  7: [mock_default_avatar_path],
                                  8: [mock_default_avatar_path]
                                  },
        }
        test_returned_sanitised_data_dict = {
            'class_name': "test_class_name",
            'chart_name': "test_chart_name",
            'chart_default_filename': "test_chart_default_filename",
            'chart_params': {"some": "chart", "default": "params"},
            'score-avatar_dict': {0: ['path to Cali_avatar.png'],
                                  1: [str_mock_default_avatar_path, str_mock_default_avatar_path],
                                  3: [str_mock_default_avatar_path, str_mock_default_avatar_path],
                                  50: [str_mock_default_avatar_path],
                                  99: [str_mock_default_avatar_path],
                                  100: [str_mock_default_avatar_path],
                                  2: ['path to Ashley_avatar.png'],
                                  4: [str_mock_default_avatar_path],
                                  6: ['path to Danielle.png'],
                                  7: [str_mock_default_avatar_path],
                                  8: [str_mock_default_avatar_path]
                                  },
        }

        assert sanitise_avatar_path_objects(test_data_dict) == test_returned_sanitised_data_dict


class TestUserSaveChartImage:
    def test_user_save_chart_image(self, monkeypatch):
        test_chart_data_dict = {'class_name': 'my_test_class',
                                'chart_default_filename': 'my_test_default_chart_filename'
                                }
        test_image_location = Path('my/test/image/location')

        test_user_pathname = 'my/path'

        def mocked_get_user_save_chart_pathname(class_name, default_chart_name):
            if (class_name, default_chart_name) != (
                    test_chart_data_dict['class_name'], test_chart_data_dict['chart_default_filename']):
                raise ValueError
            return test_user_pathname

        def mocked_copy_image_to_user_save_loc(image_location, save_chart_pathname):
            if image_location != test_image_location and save_chart_pathname != test_user_pathname:
                raise ValueError

        monkeypatch.setattr(create_chart, 'get_user_save_chart_pathname', mocked_get_user_save_chart_pathname)
        monkeypatch.setattr(create_chart, 'copy_image_to_user_save_loc', mocked_copy_image_to_user_save_loc)

        assert user_save_chart_image(test_chart_data_dict, test_image_location) is None


class TestCopyImageToUserSaveLoc:
    def test_copy_image_to_user_save_loc(self, monkeypatch):
        test_app_image_location = Path('test/app/image/location')
        test_user_save_location = Path('test/user/save/location')

        def mocked_copy_file(app_image_location, user_save_location):
            if (app_image_location, user_save_location) != (
                    test_app_image_location, test_user_save_location):
                raise ValueError

        monkeypatch.setattr(create_chart, 'copy_file', mocked_copy_file)

        assert copy_image_to_user_save_loc(test_app_image_location, test_user_save_location) is None


class TestGetUserSaveChartPathname:
    def test_get_user_save_chart_pathname(self, monkeypatch):
        test_class_name = 'my_test_class'
        test_default_chart_name = 'my_test_chart_name'

        test_class_save_folder_path = Path('path/to/test/class/save/folder')
        test_save_chart_path_str = r'test/save/chart/path/str'

        def mocked_create_class_save_folder(class_name):
            if class_name is not test_class_name:
                raise ValueError
            return test_class_save_folder_path

        def mocked_save_chart_dialogue(default_chart_name, class_save_folder_path):
            if (default_chart_name, class_save_folder_path) != (
                    test_default_chart_name, test_class_save_folder_path):
                raise ValueError
            return test_save_chart_path_str

        monkeypatch.setattr(create_chart, 'create_class_save_folder', mocked_create_class_save_folder)
        monkeypatch.setattr(create_chart, 'save_chart_dialogue', mocked_save_chart_dialogue)

        assert get_user_save_chart_pathname(test_class_name, test_default_chart_name) == test_save_chart_path_str


class TestCreateClassSaveFolder:
    def test_create_class_save_folder(self, tmp_path, monkeypatch):
        test_class_name = 'my_test_class_name'
        test_class_save_folder_path = tmp_path.joinpath(test_class_name)

        def mocked_get_class_save_folder_path(class_name):
            if class_name != test_class_name:
                raise ValueError
            return test_class_save_folder_path

        monkeypatch.setattr(create_chart, 'get_class_save_folder_path', mocked_get_class_save_folder_path)

        assert create_class_save_folder(test_class_name) == test_class_save_folder_path

        assert test_class_save_folder_path.exists()


class TestGetClassSaveFolderPath:
    def test_get_class_save_folder_path(self, monkeypatch):
        monkeypatch.setattr(definitions, 'DEFAULT_CHART_SAVE_FOLDER', Path('my.DEFAULT/CHART/SAVE/FOLDER'))

        test_class_name = 'my_test_class_name'
        test_class_save_folder_path = definitions.DEFAULT_CHART_SAVE_FOLDER.joinpath(test_class_name)

        assert get_class_save_folder_path(test_class_name) == test_class_save_folder_path


def test_get_class_save_folder_path(monkeypatch):
    monkeypatch.setattr(create_chart.definitions, 'DEFAULT_CHART_SAVE_FOLDER', None)
    with pytest.raises(ValueError):
        get_class_save_folder_path('some_class')


class TestShowImage:
    def test_show_image(self, monkeypatch):
        test_image_location = Path('my/test/image/path')

        display_image_save_as_mock = {'called': False}

        def mocked_display_image_save_as(image_location):
            if image_location != test_image_location:
                raise ValueError
            display_image_save_as_mock['called'] = True

        monkeypatch.setattr(create_chart, 'display_image_save_as', mocked_display_image_save_as)

        assert show_image(test_image_location) is None

        assert display_image_save_as_mock['called']
