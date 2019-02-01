
from unittest import TestCase

from dionysus_app.UI_menus.chart_generator.take_chart_data_UI import (take_score_data,
                                                                      )


class TestTakeScoreData(TestCase):
    def test_take_score_data(self):
        self.fail()



def take_score_data(class_name: str):
    """
    UI function presenting student names from supplied class one at a
    time and taking a score for each.
    Path objects for each student's avatar are added to a list of avatar
    Paths corresponding to scores.

    Scores can be int or float, eg 78.5 is valid entry, and are
    converted to float (from str) by default.

    Return is a dict with scores as keys, lists of Path objects as
    values. eg student_scores = {33: [Path_obj1, Path_obj2, Path_obj3,
                                 17: [Path_obj1, Path_obj2, Path_obj3]
                                 }


    :param class_name: str
    :return: dict
    """

    class_data_dict = load_class_data(class_name)

    student_scores = {}

    print(f"\nEnter student scores for {class_name}: \n"
          f"Type score for each student, or '_' to exclude student, and press enter.")

    for student_name in list(class_data_dict.keys()):

        student_avatar_filename = class_data_dict[student_name][0]
        avatar_path = get_avatar_path(class_name, student_avatar_filename)

        student_score = take_score_entry(student_name)
        # add avatar to list of avatars for score
        if student_score:
            student_scores[student_score] = student_scores.get(student_score, []) + [avatar_path]

    # Newline between last score and 'Please enter a chart name/title: '
    print('\n')

    return student_scores
















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
