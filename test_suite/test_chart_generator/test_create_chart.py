from unittest import TestCase
from unittest.mock import patch

from dionysus_app.chart_generator import create_chart
from dionysus_app.chart_generator.create_chart import (get_custom_chart_options,
                                                       new_chart,
                                                       )

class TestTakeStudentScores:
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
            return test_class_name, test_chart_name, test_chart_default_filename, test_score_avatar_dict, test_chart_params

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


class TestGetCustomChartOptions(TestCase):
    def setUp(self):
        self.test_default_params = {'default param': 'my default param value'}

    @patch('dionysus_app.chart_generator.create_chart.take_custom_chart_options')
    def test_get_custom_chart_options(self, mock_custom_chart_options):
        assert get_custom_chart_options(self.test_default_params) == self.test_default_params

        mock_custom_chart_options.assert_called_once()
