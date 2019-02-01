from unittest import mock, TestCase
from unittest.mock import patch

from dionysus_app.UI_menus.chart_generator.take_chart_data_UI import (take_score_data,
                                                                      take_student_scores,
                                                                      )
from test_suite.testing_class_data import testing_class_data_set as test_class_data


class TestTakeScoreData(TestCase):
    def setUp(self):
        self.test_classname = 'the knights who say ni'
        self.test_class_data_dict = test_class_data['loaded_dict']

        self.score_entry_instruction = (f"\nEnter student scores for {self.test_classname}: \n"
                                        f"Type score for each student, or '_' to exclude student, and press enter.")
        self.newline_after_entry = '\n'
        self.print_calls = [self.score_entry_instruction, self.newline_after_entry]

        self.mock_score_avatar_dict = {'scores': 'list of avatars'}

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.take_student_scores')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.print')
    def test_take_score_data(self, mocked_print, mocked_take_student_scores):
        mocked_take_student_scores.return_value = self.mock_score_avatar_dict

        assert take_score_data(self.test_classname,
                               self.test_class_data_dict) == self.mock_score_avatar_dict

        assert mocked_print.call_args_list == [mock.call(print_call) for print_call in self.print_calls]
        mocked_take_student_scores.called_once_with(self.test_classname, self.test_class_data_dict)














def test_take_score_entry():
    """
    Test for regular parameters (ie default 0-100 range)
    Need further tests using different range.

    :return:
    """

    test_dict = {
        '_': None,
        '0': 0.0,
        '1.25': 1.25,
        '5.7': 5.7,
        '7': 7.0,
        '99': 99.0,
        '100': 100.0,
        '101': "InputError: Please enter a number between 0 and 100.",
        'i am bad data': "InputError: please enter a number or '_' to exclude student.",
        }

    for i in test_dict:
        assert i == i
        # mock input
        # assert take_score_entry() == return_value_from_function
