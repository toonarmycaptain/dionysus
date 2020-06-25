"""UI elements for class_functions"""
from pathlib import Path
from typing import Dict, Optional, Union

import definitions

from dionysus_app.class_ import Class
from dionysus_app.persistence.database import ClassIdentifier
from dionysus_app.UI_menus.UI_functions import (ask_user_bool,
                                                clean_for_filename,
                                                input_is_essentially_blank,
                                                select_file_dialogue,
                                                )


def take_classlist_name_input() -> str:
    """
    Prompts user for classlist name.

    Repeats until user provide valid classlist name.

    :return: str
    """

    while True:
        classlist_name = input('Please enter a name for the class: ')

        if input_is_essentially_blank(classlist_name):  # blank input
            continue

        classlist_name = clean_for_filename(classlist_name)
        if definitions.DATABASE.class_name_exists(classlist_name):
            print('A class with this name already exists.')
            continue
        break
    return classlist_name


def take_student_name_input(the_class: Class) -> str:
    """
    Prompts user to enter a valid student name.

    Prompts user for student name, checks if student name is a valid name, or
    is already in the class, prompting to enter a different name if this is the
    case.

    :param the_class: Class object
    :return: str
    """
    while True:
        student_name = input("Enter student name, or 'end', and hit enter: ")
        if input_is_essentially_blank(student_name):  # Do not allow blank input
            print('Please enter a valid student name.')
            continue

        if student_name in the_class:
            print("This student is already a member of the class.")
            continue
        return student_name


def blank_class_dialogue() -> bool:
    """
    Query user intention to create empty class.

    :return: bool
    """
    return ask_user_bool(
        question='Do you want to create an empty class? [Y/N] ',
        invalid_input_response='Please enter y for yes to create empty class, or n to return to student input.')


def class_data_feedback(current_class: Class) -> None:
    """
    Print classlist name and list of students as user feedback.

    :param current_class: Class object
    :return: None
    """
    print(f'\nClass name: {current_class.name}')
    if not current_class.students:
        print("No students entered.")
    else:
        for student in current_class:
            print(student.name)


def create_chart_with_new_class_dialogue() -> bool:
    """
    Get user desire to create a new chart with newly created class.

    Intended to be called following new class creation.
    Prompts user to indicate if they would like to go directly to creating a
    chart with the class they just created, returning True/False.

    :return: bool
    """
    return ask_user_bool(question="Do you want to create a new chart for the class you just created? [Y/N]: ",
                         invalid_input_response="Invalid response, please try again.")


def display_class_selection_menu(class_options: Dict[int, ClassIdentifier]) -> None:
    """
    Print "Select class from list:" followed by numbered option list.

    :param class_options: Dict[int, ClassIdentifier]
    :return: None
    """
    print("Select class from list:")
    for key, class_ in class_options.items():
        print(f'{key}. {class_.name}')


def take_class_selection(class_options: Dict[int, ClassIdentifier]) -> ClassIdentifier:
    """
    Prompt user to select a class, return selected class name.

    Takes a dict with form i: ClassIdentifier, where i is an integer.

    Prompts user to select class by typing in corresponding integer.

    User may also type in class name if input exactly matches class name,
    but this behaviour is predicated on exact match and thus not
    communicated to user.

    :param class_options: Dict[int: ClassIdentifier]
    :return: ClassIdentifier
    """
    while True:
        chosen_option: Union[int, str]
        chosen_option = input('Select class: ')

        try:
            selected_class = class_options[int(chosen_option)]
            break

        except (KeyError, ValueError):
            # User typed class name instead of numeral:
            class_names = [class_.name for class_ in class_options.values()]
            if chosen_option in class_names:
                # Correct int to select is index in class_names+1,
                # since class_options keys start at 1, not 0.
                selected_class = class_options[class_names.index(chosen_option) + 1]
                break
            # else:
            print("Invalid input.\nPlease enter the integer beside the name of the desired class.")

    return selected_class


def display_student_selection_menu(student_list_dict: dict) -> None:
    """
    Print "Select student from list:" followed by numbered option list.

    :param student_list_dict: dict
    :return: None
    """
    print("Select student from list:")
    for key, class_name in student_list_dict.items():
        print(f'{key}. {class_name}')


def take_student_selection(student_options: dict) -> str:
    """
    Takes a dict with form i: 'student name', where i is an integer.

    Prompts user to select student by typing in corresponding integer.

    User my also type in student name if input exactly matches student name,
    but this behaviour is predicated on exact match and thus not
    communicated to user.

    :param student_options: dict
    :return: str
    """
    while True:
        chosen_option = input('Select student: ')

        try:
            selected_student = student_options[int(chosen_option)]
            break

        except (KeyError, ValueError):
            # Case where user typed in name of student.
            if chosen_option in student_options.values():
                selected_student = chosen_option
                break
            # else:
            print("Invalid input.\nPlease enter the integer beside the name of the desired student.")

    return selected_student


def select_avatar_file_dialogue() -> Optional[Path]:
    """
    Prompts user to select an avatar file.

    Currently only displays PNG files by default.

    :return: Path or None
    """
    dialogue_box_title = 'Select .png format avatar:'
    filetypes = [('.png files', '*.png'), ("all files", "*.*")]
    start_dir = '..'  # start at parent to app directory.

    return select_file_dialogue(dialogue_box_title, filetypes, start_dir)
