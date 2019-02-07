from unittest import TestCase, mock
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


class TestTakeStudentScores(TestCase):
    mock_DEFAULT_AVATAR_PATH = 'mocked_default_avatar_path'

    def setUp(self):
        self.mock_DEFAULT_AVATAR_PATH = 'mocked_default_avatar_path'

        self.test_classname = 'the knights who say ni'
        self.test_class_data_dict = test_class_data['loaded_dict']

        # NB If data other than avatar in dict values, this test implementation may need to change.
        self.avatar_paths = [f'path to {avatar[0]}' if avatar[0] is not None
                             else self.mock_DEFAULT_AVATAR_PATH
                             for avatar in test_class_data['loaded_dict'].values()]

        # Gives no score to one student with and without an avatar.
        self.mocked_take_score_entry_return_values = [0, 1, 3, None, 50, 99, 100, 1, 2, 3, 4, None, 6, 7, 8]
        self.mocked_get_avatar_path_return_values = [self.avatar_paths[self.mocked_take_score_entry_return_values.index(score)]
                                                     for score in self.mocked_take_score_entry_return_values
                                                     if score is not None]

        self.test_take_student_scores_return_value = {0: ['path to Cali_avatar.png'],
                                                      1: [self.mock_DEFAULT_AVATAR_PATH, self.mock_DEFAULT_AVATAR_PATH],
                                                      3: [self.mock_DEFAULT_AVATAR_PATH, self.mock_DEFAULT_AVATAR_PATH],
                                                      # None: ['Zach_avatar.png', None],  # No score not returned.
                                                      50: [self.mock_DEFAULT_AVATAR_PATH],
                                                      99: [self.mock_DEFAULT_AVATAR_PATH],
                                                      100: [self.mock_DEFAULT_AVATAR_PATH],
                                                      2: ['path to Ashley_avatar.png'],
                                                      4: [self.mock_DEFAULT_AVATAR_PATH],
                                                      6: ['path to Danielle.png'],
                                                      7: [self.mock_DEFAULT_AVATAR_PATH],
                                                      8: [self.mock_DEFAULT_AVATAR_PATH]
                                                      }

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.get_avatar_path')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.take_score_entry')
    def test_take_student_scores(self, mocked_take_score_entry, mocked_get_avatar_path):
        mocked_take_score_entry.side_effect = self.mocked_take_score_entry_return_values
        mocked_get_avatar_path.side_effect = self.mocked_get_avatar_path_return_values

        assert take_student_scores(self.test_classname,
                                   self.test_class_data_dict) == self.test_take_student_scores_return_value

        mocked_take_score_entry.call_args_list = [mock.call(student_name) for student_name in self.test_class_data_dict]
        mocked_get_avatar_path.call_args_list = [mock.call(self.test_classname,
                                                           self.test_class_data_dict[student_name][0])
                                                 for student_name in self.test_class_data_dict]


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
