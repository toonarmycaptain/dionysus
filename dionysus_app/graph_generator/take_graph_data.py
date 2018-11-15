"""
Script for taking and saving data for graph.
"""

# score entry:

from dionysus_app.class_functions import load_class_data, get_avatar_path
from dionysus_app.data_folder import DataFolder
from dionysus_app.UI_functions import input_is_essentially_blank


CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


def take_score_data(class_name):
    class_data_dict = load_class_data(class_name)

    student_scores = {}
    for student_name in list(class_data_dict.keys()):

        student_avatar_filename = class_data_dict[student_name][0]
        avatar_path = get_avatar_path(class_name, student_avatar_filename)

        student_score = take_score_entry(student_name)
        # add avatar to list of avatars for score
        student_scores[student_score] = student_scores.get(student_score, []).append(avatar_path)

    return student_scores


def take_score_entry(student_name: str, minimum: int=0, maximum: int=100):
    """

    :param student_name: str
    :param minimum: int, default=0  # is there a more correct way to document default keyword arguments?
    :param maximum: int, default=100
    :return:
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
    Ask user for chart name. Ask again if name is essentially blank/whitespace/punctuation.

    :return: str
    """
    chart_name = input('Please enter a chart/title: ')
    while True:
        if input_is_essentially_blank(chart_name):
            continue
        break
    return chart_name


if __name__ == '__main__':
    pass
