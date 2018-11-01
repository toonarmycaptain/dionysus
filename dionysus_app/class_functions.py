"""
Functions for creating, editing, dealing with classes.
"""

import json
import time
from pathlib import Path

from dionysus_app.data_folder import DataFolder
from dionysus_app.UI_functions import clean_for_filename, input_is_essentially_blank
from dionysus_app.class_registry import CLASSLIST_DATA_FILE_TYPE, classlist_exists, register_class

CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


def create_classlist():

    classlist_name = take_classlist_name_input()  # TODO: Option to cancel creation at class name entry stage

    setup_class(classlist_name)
    create_classlist_data(classlist_name)


def take_classlist_name_input():
    """
    Prompts user for classlist name.
    It repeats until user provide correct classlist name.

    :return: str
    """

    while True:
        classlist_name = input('Please enter a name for the class: ')

        if input_is_essentially_blank(classlist_name):  # blank input
            continue

        classlist_name = clean_for_filename(classlist_name)
        if classlist_exists(classlist_name):
            print('A class with this name already exists.')
            continue
        break
    return classlist_name


def setup_class(classlist_name):  # TODO: change name because of class with python 'class' keyword?
    """
    Setup class data storage file structure.
    Register class in class_registry index

    :param classlist_name:
    :return:
    """
    setup_class_data_storage(classlist_name)
    register_class(classlist_name)


def setup_class_data_storage(classlist_name):
    """
    Setup data storage for new classes.

    Structure for data storage:
    app_data/
        class_data/
            class_name/  # folder for each class
                graph_data/  # store graph data sets
                avatars/  # store avatars for class


    :param classlist_name: str
    :return: None
    """
    avatar_path = CLASSLIST_DATA_PATH.joinpath(classlist_name, 'avatars')
    graph_path = CLASSLIST_DATA_PATH.joinpath(classlist_name, 'graph_data')

    avatar_path.mkdir(exist_ok=True, parents=True)
    graph_path.mkdir(exist_ok=True, parents=True)


def create_classlist_data(class_name: str):

    class_data = compose_classlist_dialogue()

    class_data_feedback(class_name, class_data)
    write_classlist_to_file(class_name, class_data)
    time.sleep(2)  # Pause for user to look over feedback.


def compose_classlist_dialogue():
    while True:
        class_data = take_class_data_input()

        if not class_data:  # Test for empty class.
            cancelled = blank_class_dialogue()
            if cancelled:
                break
            # else: ie if not cancelled:
            continue
        break  # class_data not empty

    return class_data


def take_class_data_input():
    """
    Take student names, avatars, return dictionary of data.

    :return: dict
    """
    class_data = {}
    while True:
        student_name = take_student_name_input(class_data)
        if student_name.upper() == 'END':
            break
        avatar_filename = take_student_avatar(student_name)
        class_data[student_name] = [avatar_filename]
    return class_data


def take_student_name_input(class_data):
    """
    Prompts user for student name.

    :param class_data: str
    :return: str
    """
    while True:
        student_name = input("Enter student name, or 'end': ")
        if input_is_essentially_blank(student_name):  # Do not allow blank input
            print('Please enter a valid student name.')
            continue

        if student_name in class_data:
            print("This student is already a member of the class.")
            continue
        return student_name


def take_student_avatar(student_name):
    """
    Prompts user for path to avatar file.

    :param student_name: str
    :return: str or None
    """
    print(f'Load avatar image for {student_name}.')
    while True:
        avatar_file = input(r'Please paste complete filepath and name eg C:\my_folder\my_avatar.jpg or None to skip: ')
        if avatar_file.upper() == 'NONE':
            return None
        if avatar_file_exists(avatar_file):
            break
        # else:
        print('Supplied filepath cannot be found.')

    if avatar_file is None:
        return None
    cleaned_student_name = clean_for_filename(student_name)
    avatar_filename = f'{cleaned_student_name}.jpg'
    # process_student_avatar()
    # convert to jpg or whatever, copy image file to class_data avatar folder with filename that is student name
    return avatar_filename


def avatar_file_exists(avatar_file):
    """
    Checks if provided file exists.

    :param avatar_file: str
    :return: bool
    """
    return Path(avatar_file).expanduser().resolve().exists()


def blank_class_dialogue():
    while True:
        choice = input("Do you want to create an empty class? y/n")
        if choice.upper() == 'Y':
            return True
        if choice.upper() == 'N':
            return False
        # TODO: Option to cancel creation here/after entering a class name (eg made typo in class name)
        print('Please enter y for yes to create empty class, or n to return to student input.')


def class_data_feedback(classlist_name: str, class_data_dict: dict):
    """
    Print classlist name and list of students as user feedback.

    :param classlist_name: str
    :param class_data_dict: dict
    :return: None
    """
    print(f'\nClass name: {classlist_name}')
    if not class_data_dict:
        print("No students entered.")
    else:
        for key in class_data_dict:
            print(key)


def write_classlist_to_file(class_name: str, class_data_dict: dict):
    """
    Write classlist data to disk with format:

    Classlist name
    JSON'd class data dict  # Second line, when reading JSON back in.

    :param class_name: str
    :param class_data_dict: dict
    :return: None
    """
    data_file = class_name + CLASSLIST_DATA_FILE_TYPE
    classlist_data_path = CLASSLIST_DATA_PATH.joinpath(class_name, data_file)

    json_class_data = convert_to_json(class_data_dict)

    with open(classlist_data_path, 'w') as classlist_file:
        classlist_file.write(f'{class_name}\n')
        classlist_file.write(json_class_data)


def convert_to_json(data_to_convert):
    """
    Serialise data in JSON format, return as JSON string.

    :param data_to_convert:
    :return: str
    """
    converted_data = json.dumps(data_to_convert, indent=4)
    return converted_data


if __name__ == '__main__':
    create_classlist()
    # similarly for edit classlist - with open(classlist_name + '.txt', 'r+') as classlist_file: to edit
