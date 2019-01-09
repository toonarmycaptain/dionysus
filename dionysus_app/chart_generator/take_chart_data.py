"""
Script for taking and saving data for graph.
"""

# score entry:

from dionysus_app.class_functions import load_class_data, get_avatar_path
from dionysus_app.data_folder import DataFolder
from dionysus_app.UI_menus.UI_functions import input_is_essentially_blank


CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


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


def take_score_entry(student_name: str, minimum: int=0, maximum: int=100):
    """

    :param student_name: str
    :param minimum: int, default=0
    :param maximum: int, default=100
    :return: float
    """
    while True:
        score = input(f'{student_name}: ')

        if score == '_':
            return None  # do not include student in graph eg if absent

        try:
            score_float = float(score)
        except ValueError:
            print("InputError: please enter a number or '_' to exclude student.")
            continue
        # else:
        if score_float < minimum or score_float > maximum:
            print(f'InputError: Please enter a number between {minimum} and {maximum}.')
            continue
        return score_float


def take_chart_name():
    """
    Ask user for chart name. Ask again if name is essentially
    blank/whitespace/punctuation.

    :return: str
    """
    chart_name = input('Please enter a chart name/title: ')
    while True:
        if input_is_essentially_blank(chart_name):
            continue
        break
    return chart_name


def take_custom_chart_options():
    pass

    # offer to reduce x-axis to just outside spread of data.
    # offer to use hash of student name instead of default avatar.
    # offer to put chart name (or a title distinct from chart/file name)
    # in chart.


if __name__ == '__main__':
    pass
