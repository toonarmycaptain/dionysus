"""
Functions for creating, editing, dealing with classes.
"""

import time

from pathlib import Path

import definitions

from dionysus_app.class_registry_functions import classlist_exists, register_class
from dionysus_app.data_folder import DataFolder, CLASSLIST_DATA_FILE_TYPE
from dionysus_app.file_functions import convert_to_json, load_from_json, copy_file
from dionysus_app.UI_menus.UI_functions import clean_for_filename, input_is_essentially_blank, select_file_dialogue


CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)
DEFAULT_AVATAR_PATH = DataFolder.generate_rel_path(DataFolder.DEFAULT_AVATAR.value)


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


def setup_class(classlist_name):  # TODO: change name because of clash with python 'class' keyword?
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
                chart_data/  # store chart data sets
                avatars/  # store avatars for class


    :param classlist_name: str
    :return: None
    """
    avatar_path = CLASSLIST_DATA_PATH.joinpath(classlist_name, 'avatars')
    chart_path = CLASSLIST_DATA_PATH.joinpath(classlist_name, 'chart_data')
    user_chart_save_folder = Path(definitions.DEFAULT_CHART_SAVE_FOLDER).joinpath(classlist_name)

    avatar_path.mkdir(exist_ok=True, parents=True)
    chart_path.mkdir(exist_ok=True, parents=True)
    user_chart_save_folder.mkdir(exist_ok=True, parents=True)


def create_classlist_data(class_name: str):

    class_data = compose_classlist_dialogue(class_name)

    class_data_feedback(class_name, class_data)
    write_classlist_to_file(class_name, class_data)
    time.sleep(2)  # Pause for user to look over feedback.


def compose_classlist_dialogue(class_name):
    while True:
        class_data = take_class_data_input(class_name)

        if not class_data:  # Test for empty class.
            cancelled = blank_class_dialogue()
            if cancelled:
                break
            # else: ie if not cancelled:
            continue
        break  # class_data not empty

    return class_data


def take_class_data_input(class_name):
    """
    Take student names, avatars, return dictionary of data.

    :return: dict
    """
    class_data = {}
    while True:
        student_name = take_student_name_input(class_data)
        if student_name.upper() == 'END':
            break
        avatar_filename = take_student_avatar(class_name, student_name)
        class_data[student_name] = [avatar_filename]
    return class_data


def take_student_name_input(class_data):
    """
    Prompts user for student name.

    :param class_data: str
    :return: str
    """
    while True:
        student_name = input("Enter student name, or 'end', and hit enter: ")
        if input_is_essentially_blank(student_name):  # Do not allow blank input
            print('Please enter a valid student name.')
            continue

        if student_name in class_data:
            print("This student is already a member of the class.")
            continue
        return student_name


def take_student_avatar(class_name, student_name):
    """
    Prompts user for path to avatar file.

    :param class_name: str
    :param student_name: str
    :return: str or None
    """
    avatar_file = select_avatar_file_dialogue()

    if avatar_file is None:
        return None

    cleaned_student_name = clean_for_filename(student_name)
    target_avatar_filename = f'{cleaned_student_name}.png'

    # TODO: process_student_avatar()
    # TODO: convert to png
    copy_avatar_to_app_data(class_name, avatar_file, target_avatar_filename)

    return target_avatar_filename


def select_avatar_file_dialogue():
    """
    Prompts user to select an avatar file. Only displays PNG files.
    :return: str or None
    """
    dialogue_box_title = 'Select .png format avatar:'
    filetypes = [('.png files', '*.png'), ("all files", "*.*")]
    start_dir = '..'  # start at parent to app directory.

    filename = select_file_dialogue(dialogue_box_title, filetypes, start_dir)

    return filename


def copy_avatar_to_app_data(classlist_name, avatar_filename, save_filename):
    """
    Copies given avatar image to classlist_name/avatars/ with given save_filename.
    No need to pre-check if file exists because it could not be selected if it did not exist.

    :param classlist_name: str
    :param avatar_filename: str or Path
    :param save_filename: str or Path
    :return: None
    """
    save_avatar_path = CLASSLIST_DATA_PATH.joinpath(classlist_name, 'avatars', save_filename)
    copy_file(avatar_filename, save_avatar_path)


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

    JSON'd class data dict  # Second line, when reading JSON back in.

    CAUTION: conversion to JSON will convert int/float keys in score_avatar_dict
    to strings, and keep them as strings when loading.

    :param class_name: str
    :param class_data_dict: dict
    :return: None
    """
    data_file = class_name + CLASSLIST_DATA_FILE_TYPE
    classlist_data_path = CLASSLIST_DATA_PATH.joinpath(class_name, data_file)

    json_class_data = convert_to_json(class_data_dict)

    with open(classlist_data_path, 'w') as classlist_file:
        classlist_file.write(json_class_data)


def select_classlist():
    """
    Display list of existent classes from class_registry and allow user to select one, returning the name of the
    selected class.

    :return: str
    """
    class_options = create_class_list_dict()
    display_class_selection_menu(class_options)  # TODO: Select class or redirect to create new class.

    selected_class = take_class_selection(class_options)

    return selected_class


def create_class_list_dict():
    """
    Create dict with enumerated classes, starting at 1.

    :return: dict
    """
    class_dict = {str(option): class_name for option, class_name in enumerate(definitions.REGISTRY, start=1)}
    return class_dict


def display_class_selection_menu(class_options: dict):
    print("Select class from list:")
    for key, class_name in class_options.items():
        print(f'{key}. {class_name}')


def take_class_selection(class_options):

    unselected = True
    selected_class = None
    while unselected:
        chosen_option = input('Select class: ')

        try:
            selected_class = class_options[chosen_option]
            unselected = False  # Exiting the loop when chosen action finishes.
        except KeyError:
            print("Invalid input.\nPlease enter the integer beside the name of the desired class.")

    return selected_class


def create_student_list_dict(class_name: str):
    """
    Create dict with enumerated students, starting at 1.


    :param class_name: str
    :return: dict
    """
    class_data = load_class_data(class_name)
    student_list_dict = {str(option): student_name for option, student_name in enumerate(class_data, start=1)}
    return student_list_dict


def load_class_data(class_name: str):
    """
    Load class data from a class data ('.cld') file.

    Data will be a dict with format:
                                keys: student name
                                values: list currently only containing the avatar filename/None.

    :param class_name: str
    :return: dict
    """

    class_data_filename = class_name + CLASSLIST_DATA_FILE_TYPE
    classlist_data_path = CLASSLIST_DATA_PATH.joinpath(class_name, class_data_filename)

    with open(classlist_data_path, 'r') as class_datafile:
        loaded_class_json = class_datafile.read()
        class_data_dict = load_from_json(loaded_class_json)
    return class_data_dict


def display_student_selection_menu(student_list: dict):
    print("Select student from list:")
    for key, class_name in student_list.items():
        print(f'{key}. {class_name}')


def get_avatar_path(class_name, student_avatar):
    """
    Take value from 'avatar' in list of student data, return path for student avatar or default avatar path if student
    has no avatar.

    :param class_name: str
    :param student_avatar: str or None
    :return: Path object
    """
    if student_avatar is None:
        return DEFAULT_AVATAR_PATH
    return avatar_path_from_string(class_name, student_avatar)


def avatar_path_from_string(class_name, avatar_filename):
    """
    Take class name and student's avatar filename, return a Path object to the avatar image file.

    :param class_name: str
    :param avatar_filename: str
    :return: Path object
    """
    return CLASSLIST_DATA_PATH.joinpath(class_name, 'avatars', avatar_filename)


def edit_classlist():
    """
     similarly to create classlist: for edit classlist -
    :return:
    """
    classlist_name = take_classlist_name_input()
    with open(classlist_name + '.txt', 'r+') as classlist_file:
        pass


if __name__ == '__main__':
    create_classlist()
