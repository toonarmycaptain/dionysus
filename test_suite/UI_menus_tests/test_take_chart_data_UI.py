from unittest import TestCase, mock
from unittest.mock import patch

from dionysus_app.UI_menus.chart_generator.take_chart_data_UI import (take_score_data, take_score_entry,
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
        self.mocked_get_avatar_path_return_values = [
            self.avatar_paths[self.mocked_take_score_entry_return_values.index(score)]
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


class TestTakeScoreEntry(TestCase):
    def setUp(self):
        self.test_student_name = 'king arthur'

        self.bad_input_print_stmt = "InputError: please enter a number or '_' to exclude student."
        # self.out_of_range_print_stmt = f'InputError: Please enter a number between {minimum} and {maximum}.'

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.print')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.input')
    def test_take_score_entry_no_input(self, mocked_input, mocked_print):
        """Test no score entered (but return pressed)."""

        mocked_input.side_effect = ['',
                                    '50'  # Good input.
                                    ]

        assert take_score_entry(self.test_student_name) == 50.0

        mocked_print.assert_called_with(self.bad_input_print_stmt)

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.print')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.input')
    def test_take_score_entry_non_numeric_input(self, mocked_input, mocked_print):
        """Test non-numeric input."""

        mocked_input.side_effect = ['Fifty-seven',
                                    '50'  # Good input.
                                    ]

        assert take_score_entry(self.test_student_name) == 50.0

        mocked_print.assert_called_with(self.bad_input_print_stmt)

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.print')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.input')
    def test_take_score_entry_no_score_provided(self, mocked_input, mocked_print):
        """Test for no score given/omit student."""

        mocked_input.return_value = '_'

        assert take_score_entry(self.test_student_name) is None
        mocked_print.assert_not_called()

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.print')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.input')
    def test_take_score_entry_good_input_default_range(self, mocked_input, mocked_print):
        """Test for regular parameters (ie default 0-100 range)."""
        test_inputs = [('0', 0.0),
                       ('0.0', 0.0),
                       ('1.25', 1.25),
                       ('5.7', 5.7),
                       ('5.700', 5.7),
                       ('7', 7.0),
                       ('99', 99.0),
                       ('99.99', 99.99),
                       ('100', 100.0,),
                       ('100.0', 100.0),
                       ]

        for input_str, return_value in test_inputs:
            with self.subTest(msg=f'Good input of {input_str}, default min/max.'):
                mocked_input.return_value = input_str
                assert take_score_entry(self.test_student_name) == return_value
                mocked_print.assert_not_called()

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.print')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.input')
    def test_take_score_entry_good_input_custom_range(self, mocked_input, mocked_print):
        """Test for good input in with custom range parameters."""
        test_inputs = [('5.7', 5.7),
                       ('7', 7.0),
                       ('99', 99.0),
                       ('99.99', 99.99),
                       ('100', 100.0,),
                       ('100.0', 100.0),
                       ('107.60', 107.6),
                       ]
        for input_str, return_value in test_inputs:
            with self.subTest(msg=f'Good input of {input_str}, minimum=3, maximum=110.'):
                mocked_input.return_value = input_str

                assert take_score_entry(self.test_student_name, minimum=3, maximum=110) == return_value
                mocked_print.assert_not_called()

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.print')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.input')
    def test_take_score_entry_good_input_custom_range_negative(self, mocked_input, mocked_print):
        """Test for good input in with custom range parameters."""
        test_inputs = [('-50', -50),
                       ('-16.4', -16.4),
                       ('5.7', 5.7),
                       ('7', 7.0),
                       ('99', 99.0),
                       ('99.99', 99.99),
                       ('100', 100.0,),
                       ('100.0', 100.0),
                       ('107.60', 107.6),
                       ]
        for input_str, return_value in test_inputs:
            with self.subTest(msg=f'Good input of {input_str}, minimum=3, maximum=110.'):
                mocked_input.return_value = input_str

                assert take_score_entry(self.test_student_name, minimum=-99, maximum=110) == return_value
                mocked_print.assert_not_called()

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.print')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.input')
    def test_take_score_entry_input_outside_default_range(self, mocked_input, mocked_print):
        """Test for good input outside default range parameters."""

        test_inputs = ['-17',
                       '-5.67'
                       '103',
                       '107.60',
                       ]

        out_of_range_print_stmt = f'InputError: Please enter a number between 0 and 100.'

        for input_str in test_inputs:
            with self.subTest(msg=f'Input of {input_str} outside default range minimum=0, maximum=100.'):
                mocked_input.side_effect = [input_str,
                                            '50'  # Good input.
                                            ]

                assert take_score_entry(self.test_student_name) == 50.0
                mocked_print.assert_called_once_with(out_of_range_print_stmt)

                mocked_print.reset_mock()

    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.print')
    @patch('dionysus_app.UI_menus.chart_generator.take_chart_data_UI.input')
    def test_take_score_entry_input_outside_custom_range(self, mocked_input, mocked_print):
        """Test for good input outside custom range parameters."""
        test_inputs = ['-66',
                       '-4.567'
                       '0',
                       '0.0',
                       '1.25',
                       '5.7',
                       '7',
                       '99',
                       '99.99',
                       '100',
                       '100.0',
                       '107.60',
                       ]
        min_range, max_range = 49, 51
        out_of_range_print_stmt = f'InputError: Please enter a number between {min_range} and {max_range}.'

        for input_str in test_inputs:
            with self.subTest(msg=f'Input of {input_str} outside range minimum=49, maximum=51.'):
                mocked_input.side_effect = [input_str,
                                            '50'  # Good input.
                                            ]

                assert take_score_entry(self.test_student_name, minimum=min_range, maximum=max_range) == 50.0
                mocked_print.assert_called_once_with(out_of_range_print_stmt)

                mocked_print.reset_mock()
