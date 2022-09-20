"""
Script for taking and saving data for chart.
"""
from typing import Optional

from dionysus_app.class_ import Class
from dionysus_app.student import Student
from dionysus_app.UI_menus.UI_functions import input_is_essentially_blank, get_user_input


def take_score_data(current_class: Class) -> dict:
    """
    Prints score taking instructions, calls take_student_scores.
    Prints a newline after completion for readability.

    Returns dict with scores as keys, lists of Path objects as
    values. eg student_scores = {33: [student_id1, student_id2, student_id3,
                                 17: [student_id4, student_id5, student_id6]
                                 }

    :param current_class: Class object
    :return: dict
    """
    print(f"\nEnter student scores for {current_class.name}: \n"
          f"Type score for each student, or '_' to exclude student, and press enter.")

    student_scores = take_student_scores(current_class)

    # Newline between last score and 'Please enter a chart name/title: '
    print('\n')

    return student_scores


def take_student_scores(current_class: Class) -> dict[float, list[Student]]:
    """
    UI function presenting student names from supplied class one at a
    time and taking a score for each.
    Path objects for each student's avatar are added to a list of avatar
    Paths corresponding to scores.

    Scores can be int or float, eg 78.5 is valid entry, and are
    converted to float (from str) by default.

    Return is a dict with scores as keys, lists of Path objects as
    values. eg student_scores = {33: [student1, student2, student3,
                                 17: [student1, student2, student3]
                                 }

    :param current_class: Class object
    :return: dict[float, list[Student]]
    """
    student_scores: dict = dict()
    for student in current_class.students:

        student_score = take_score_entry(student.name)
        # add student to list of students for score
        if student_score is not None:
            student_scores[student_score] = student_scores.get(student_score, []) + [student]

    return student_scores


def take_score_entry(student_name: str,
                     minimum: int = 0,
                     maximum: int = 100) -> Optional[float]:
    """

    :param student_name: str
    :param minimum: int, default=0
    :param maximum: int, default=100
    :return: float or None
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

        if score_float < minimum or score_float > maximum:
            print(f'InputError: Please enter a number between {minimum} and {maximum}.')
            continue
        return score_float


def take_chart_name() -> str:
    """
    Ask user for chart name. Ask again if name is essentially
    blank/whitespace/punctuation.

    :return: str
    """
    chart_name = get_user_input(prompt='Please enter a chart name/title: ',
                                validation=lambda name: not input_is_essentially_blank(name),
                                validation_error_msg='Please enter a valid chart name.')
    return chart_name


def take_custom_chart_options() -> None:
    pass

    # offer to reduce x-axis to just outside spread of data.
    # offer to use hash of student name instead of default avatar.
    # offer to put chart name (or a title distinct from chart/file name)
    # in chart.
