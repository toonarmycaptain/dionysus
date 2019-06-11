from unittest import TestCase
from unittest.mock import patch

from dionysus_app.chart_generator import create_chart
from dionysus_app.chart_generator.create_chart import (assemble_chart_data,
                                                       get_custom_chart_options,
                                                       new_chart,
                                                       set_chart_params,
                                                       write_chart_data_to_file,
                                                       )
from dionysus_app.chart_generator.process_chart_data import DEFAULT_CHART_PARAMS
from dionysus_app.class_ import Class
from dionysus_app.data_folder import CHART_DATA_FILE_TYPE

from test_suite.testing_class_data import test_full_class_data_set


class TestNewChart:
    def test_new_chart(self, monkeypatch):
        test_class_name = 'test_class_name'
        test_chart_name = 'test_chart_name'
        test_chart_default_filename = 'test_chart_default_filename'
        test_chart_params = {'test_chart_params': 'some chart params'}
        test_score_avatar_dict = {'test_student_scores': 'test student avatars'}

        test_chart_data_dict = {'class_name': test_class_name,
                                'chart_name': test_chart_name,
                                'chart_default_filename': test_chart_default_filename,
                                'chart_params': test_chart_params,
                                'score-avatar_dict': test_score_avatar_dict,
                                }

        test_chart_image_location = 'some image location'

        def mocked_assemble_chart_data():
            return (test_class_name,
                    test_chart_name,
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

        monkeypatch.setattr(create_chart, 'assemble_chart_data', mocked_assemble_chart_data)
        monkeypatch.setattr(create_chart, 'write_chart_data_to_file', mocked_write_chart_data_to_file)
        monkeypatch.setattr(create_chart, 'generate_chart_image', mocked_generate_chart_image)
        monkeypatch.setattr(create_chart, 'show_image', mocked_show_image)
        monkeypatch.setattr(create_chart, 'user_save_chart_image', mocked_user_save_chart_image)

        assert new_chart() is None


class TestAssembleChartData:
    def test_assemble_chart_data(self, monkeypatch):
        test_class = Class.from_dict(test_full_class_data_set['json_dict_rep'])
        test_class_name = test_class.name
        test_chart_name = 'my_chart'
        test_chart_filename = test_chart_name
        mock_score_avatar_dict = {'scores': 'list of avatars'}
        mock_chart_params = {'some': 'chart_params'}

        def mocked_select_classlist():
            return test_class_name

        def mocked_load_class_from_disk(class_name):
            assert class_name == test_class_name
            return test_class

        def mocked_take_score_data(class_obj):
            assert class_obj is test_class
            return mock_score_avatar_dict

        def mocked_take_chart_name():
            return test_chart_name

        def mocked_clean_for_filename(chart_name):
            assert chart_name == test_chart_name
            return test_chart_name

        def mocked_set_chart_params():
            return mock_chart_params

        monkeypatch.setattr(create_chart, 'select_classlist', mocked_select_classlist)
        monkeypatch.setattr(create_chart, 'load_class_from_disk', mocked_load_class_from_disk)
        monkeypatch.setattr(create_chart, 'take_score_data', mocked_take_score_data)
        monkeypatch.setattr(create_chart, 'take_chart_name', mocked_take_chart_name)
        monkeypatch.setattr(create_chart, 'clean_for_filename', mocked_clean_for_filename)
        monkeypatch.setattr(create_chart, 'set_chart_params', mocked_set_chart_params)

        assert assemble_chart_data() == (
            test_class_name, test_chart_name, test_chart_filename, mock_score_avatar_dict, mock_chart_params)


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
            assert file_chart_data_dict == test_chart_data_dict
            # file_chart_data_dict should be a deepcopy, not a reference to the original chart_data_dict.
            assert file_chart_data_dict is not test_chart_data_dict

            return file_chart_data_dict

        def mocked_convert_to_json(json_safe_dict):
            assert json_safe_dict == test_chart_data_dict
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


class TestGetCustomChartOptions(TestCase):
    def setUp(self):
        self.test_default_params = {'default param': 'my default param value'}

    @patch('dionysus_app.chart_generator.create_chart.take_custom_chart_options')
    def test_get_custom_chart_options(self, mock_custom_chart_options):
        assert get_custom_chart_options(self.test_default_params) == self.test_default_params

        mock_custom_chart_options.assert_called_once()
