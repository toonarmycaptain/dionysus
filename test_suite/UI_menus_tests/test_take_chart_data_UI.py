import pytest

from unittest.mock import patch

from dionysus_app.class_ import Class
from dionysus_app.UI_menus.chart_generator import take_chart_data_UI
from dionysus_app.UI_menus.chart_generator.take_chart_data_UI import (take_chart_name,
                                                                      take_custom_chart_options,
                                                                      take_score_data,
                                                                      take_score_entry,
                                                                      take_student_scores,
                                                                      )
from test_suite.testing_class_data import test_full_class_data_set


class TestTakeScoreData:
    def test_take_score_data(self, monkeypatch):
        test_class = Class.from_dict(test_full_class_data_set['json_dict_rep'])

        mock_score_avatar_dict = {'scores': 'list of avatars'}

        def mocked_take_student_scores(scored_class):
            assert scored_class == test_class
            return mock_score_avatar_dict

        monkeypatch.setattr(take_chart_data_UI, 'take_student_scores', mocked_take_student_scores)

        assert take_score_data(test_class) == mock_score_avatar_dict


class TestTakeStudentScores:
    def test_take_student_scores(self, monkeypatch):
        """
        Score data returned.

        Test with generic database.
        """

        test_class = Class.from_dict(test_full_class_data_set['json_dict_rep'])

        # Gives no score to one student with and without an avatar.
        mocked_take_score_entry_return_values = [0, 1, 3, None, 50, 99, 100, 1, 2, 3, 4, None, 6, 7, 8]

        test_take_student_scores_return_value = {0: [test_class.students[0]],  # Cali
                                                 1: [test_class.students[1],  # Monty
                                                     test_class.students[7]],  # Regina
                                                 3: [test_class.students[2],  # Abby
                                                     test_class.students[9]],  # Alex
                                                 # No score, not returned: None: [test_class.students[3],  # Zach
                                                 #                                test_class.students[11]],  # Edgar
                                                 50: [test_class.students[4]],  # Janell
                                                 99: [test_class.students[5]],  # Matthew
                                                 100: [test_class.students[6]],  # Olivia
                                                 2: [test_class.students[8]],  # Ashley
                                                 4: [test_class.students[10]],  # Melissa
                                                 6: [test_class.students[12]],  # Danielle
                                                 7: [test_class.students[13]],  # Kayla
                                                 8: [test_class.students[14]],  # Jaleigh
                                                 }

        score = (score for score in mocked_take_score_entry_return_values)

        def mocked_take_score_entry(student_name):
            return next(score)

        monkeypatch.setattr(take_chart_data_UI, 'take_score_entry', mocked_take_score_entry)

        assert take_student_scores(test_class) == test_take_student_scores_return_value


class TestTakeScoreEntry:
    @pytest.mark.parametrize(
        'mocked_inputs, expected_return',
        [(['', '25'], 25.0),  # No score/blank.
         (['Fifty-seven', '50'], 50.0),  # Non numeric input.
         (['66.6667', ], 66.6667),  # Decimal input.
         (['', '_'], None),  # No score given/omit student.
         # Good inputs.
         (['0'], 0.0),
         (['0.0'], 0.0),
         (['1.25'], 1.25),
         (['5.7'], 5.7),
         (['5.700'], 5.7),
         (['7'], 7.0),
         (['99'], 99.0),
         (['99.99'], 99.99),
         (['100'], 100.0,),
         (['100.0'], 100.0),
         ])
    def test_take_score_entry(self, mocked_inputs, expected_return):
        """
        Test bad input entered prompts for correct input, in std range.
        ie default 0-100 range
        """
        with patch('builtins.input', side_effect=mocked_inputs):
            assert take_score_entry('some student name') == expected_return

    @pytest.mark.parametrize(
        'mocked_inputs, expected_return',
        [(['0'], 0.0),
         (['0.0'], 0.0),
         (['1.25'], 1.25),
         (['5.7'], 5.7),
         (['5.700'], 5.7),
         (['7'], 7.0),
         (['99'], 99.0),
         (['99.99'], 99.99),
         (['100'], 100.0,),
         (['100.0'], 100.0),
         ])
    def test_take_score_entry_good_input_default_range(self, mocked_inputs, expected_return):
        """Test for regular parameters (ie default 0-100 range)."""
        with patch('builtins.input', side_effect=mocked_inputs):
            assert take_score_entry('some student name') == expected_return

    @pytest.mark.parametrize(
        'mocked_inputs, expected_return',
        [(['5.7'], 5.7),
         (['7'], 7.0),
         (['99'], 99.0),
         (['99.99'], 99.99),
         (['100'], 100.0,),
         (['100.0'], 100.0),
         (['107.60'], 107.6),
         ])
    def test_take_score_entry_good_input_custom_range(self, mocked_inputs, expected_return):
        """Test for good input in with custom range parameters."""
        with patch('builtins.input', side_effect=mocked_inputs):
            assert take_score_entry('some student name', minimum=3, maximum=110) == expected_return

    @pytest.mark.parametrize(
        'mocked_inputs, expected_return',
        [(['5.7'], 5.7),
         (['-17', '50'], 50.0),
         (['-5.6', '50'], 50.0),
         (['103', '50'], 50.0),
         (['107.60', '50'], 50.0),
         ])
    def test_take_score_entry_input_outside_default_range(self, mocked_inputs, expected_return):
        """
        Test for good input outside default range parameters.
        Default range minimum=0, maximum=100.
        """
        with patch('builtins.input', side_effect=mocked_inputs):
            assert take_score_entry('some student name') == expected_return

    @pytest.mark.parametrize(
        'mocked_inputs, expected_return',
        [(['-66', '50'], 50.0),
         (['-4.567', '50'], 50.0),
         (['0', '50'], 50.0),
         (['0.0', '50'], 50.0),
         (['1.25', '50'], 50.0),
         (['5.7', '50'], 50.0),
         (['7', '50'], 50.0),
         (['99', '50'], 50.0),
         (['99.99', '50'], 50.0),
         (['100', '50'], 50.0),
         (['100.0', '50'], 50.0),
         (['107.60', '50'], 50.0),
         ])
    def test_take_score_entry_input_outside_custom_range(self, mocked_inputs, expected_return):
        """Test for good input outside custom range parameters."""
        with patch('builtins.input', side_effect=mocked_inputs):
            min_range, max_range = 49, 51
            assert take_score_entry('some student name', minimum=min_range, maximum=max_range) == expected_return


class TestTakeChartName:
    @pytest.mark.parametrize(
        'mocked_inputs, expected_return',
        [(['', ' ', ' _ ', '_', '.', ',', 'final valid chart name'], 'final valid chart name'),  # Initial blank inputs.
         (['correct chart name first time'], 'correct chart name first time')
         ])
    def test_take_chart_name(self, monkeypatch,
                             mocked_inputs, expected_return):
        """Test valid input returned, mocking validation."""

        def mocked_input_is_essentially_blank(test_chart_name):
            """Presume last input will be accepted."""
            return test_chart_name != mocked_inputs[-1]

        monkeypatch.setattr(take_chart_data_UI, 'input_is_essentially_blank', mocked_input_is_essentially_blank)
        with patch('builtins.input', side_effect=mocked_inputs):
            assert take_chart_name() == expected_return

    @pytest.mark.parametrize(
        'mocked_inputs, expected_return',
        [(['', ' ', ' _ ', '_', '.', ',', 'final valid chart name'], 'final valid chart name'),  # Initial blank inputs.
         (['correct chart name first time'], 'correct chart name first time')
         ])
    def test_take_chart_name_unmocked_validation(self, monkeypatch,
                                                 mocked_inputs, expected_return):
        """Test valid input returned, without mocking validation."""
        with patch('builtins.input', side_effect=mocked_inputs):
            assert take_chart_name() == expected_return


class TestTakeCustomChartOptions:
    """Function currently not implemented."""

    def test_take_custom_chart_options(self):
        assert take_custom_chart_options() is None
