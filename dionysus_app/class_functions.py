"""
Functions for creating, editing, dealing with classes.
"""

import time

from pathlib import Path

import definitions

from dionysus_app.class_ import Class
from dionysus_app.class_registry_functions import register_class
from dionysus_app.data_folder import DataFolder, CLASSLIST_DATA_FILE_TYPE
from dionysus_app.file_functions import (load_from_json_file,
                                         copy_file,
                                         )
from dionysus_app.UI_menus.class_functions_UI import (blank_class_dialogue,
                                                      class_data_feedback,
                                                      display_class_selection_menu,
                                                      display_student_selection_menu,
                                                      select_avatar_file_dialogue,
                                                      take_class_selection,
                                                      take_classlist_name_input,
                                                      take_student_name_input,
                                                      take_student_selection,
                                                      )
from dionysus_app.UI_menus.UI_functions import clean_for_filename

CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)
DEFAULT_AVATAR_PATH = DataFolder.generate_rel_path(DataFolder.DEFAULT_AVATAR.value)


def create_classlist():
    classlist_name = take_classlist_name_input()  # TODO: Option to cancel creation at class name entry stage

    setup_class(classlist_name)
    create_classlist_data(classlist_name)


def setup_class(classlist_name):
    """
    Setup class data storage file structure.
    Register class in class_registry index

    :param classlist_name:
    :return:
    """
    setup_class_data_storage(classlist_name)
    register_class(classlist_name)


def setup_class_data_storage(classlist_name: str):
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
    new_class = compose_classlist_dialogue(class_name)

    class_data_feedback(new_class)
    write_classlist_to_file(new_class)
    time.sleep(2)  # Pause for user to look over feedback.


def compose_classlist_dialogue(class_name: str):
    """
    Create class object.

    If no students added to class, check if intended, making subsequent call to
    take_class_data_input UI if unintended blank class returned.

    :param class_name: str
    :return: Class object
    """
    while True:
        new_class = take_class_data_input(class_name)

        if not new_class.students:  # Test for empty class.
            create_empty_class = blank_class_dialogue()
            if create_empty_class:
                break
            # else: ie if not cancelled:
            continue  # Line skipped from coverage due to peephole optimiser.
        break  # class_data not empty

    return new_class


def take_class_data_input(class_name: str):
    """
    Take student names, avatars, return Class object.

    :param class_name: str
    :return: Class
    """
    new_class = Class(name=class_name)
    while True:
        student_name = take_student_name_input(new_class)
        if student_name.upper() == 'END':
            break
        avatar_filename = take_student_avatar(class_name, student_name)
        new_class.add_student(name=student_name, avatar_filename=avatar_filename)
    return new_class


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
    # TODO: append hash to filename to prevent name collisions eg cleaned versions of 'a_b.jpg' and 'a b.jpg' will be identical.

    # TODO: process_student_avatar()
    # TODO: convert to png
    copy_avatar_to_app_data(class_name, avatar_file, target_avatar_filename)

    return target_avatar_filename


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


def write_classlist_to_file(current_class: Class):
    """
    Write classlist data to disk as JSON dict, according to Class object's
    Class.json_dict and Class.to_json_str methods.

    CAUTION: conversion to JSON will convert int/float keys to strings, and
    keep them as strings when loading.

    :param current_class: Class object
    :return: Path
    """
    class_name = current_class.name
    data_filename = class_name + CLASSLIST_DATA_FILE_TYPE
    classlist_data_path = CLASSLIST_DATA_PATH.joinpath(class_name, data_filename)

    json_class_data = current_class.to_json_str()

    # Make data path if it doesn't exist.
    classlist_data_path.parent.mkdir(parents=True, exist_ok=True)

    with open(classlist_data_path, 'w') as classlist_file:
        classlist_file.write(json_class_data)

    return classlist_data_path


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
    class_dict = {option: class_name for option, class_name in enumerate(definitions.REGISTRY, start=1)}
    return class_dict


def select_student(class_name: str):
    """
    Display list of students in class and allow user to select one, returning the name of the
    selected student.

    :param class_name: str
    :return: str
    """
    student_options = create_student_list_dict(class_name)
    display_student_selection_menu(student_options)

    selected_student = take_student_selection(student_options)

    return selected_student


def create_student_list_dict(class_name: str):
    """
    Create dict with enumerated students, starting at 1.

    CONSIDER DEPRECIATED GOING FORWARD, as for most all use cases, class will
    already be loaded when this is needed.

    :param class_name: str
    :return: dict
    """
    loaded_class = load_class_from_disk(class_name)
    student_list_dict = {option: student.name
                         for option, student in enumerate(loaded_class.students, start=1)}
    return student_list_dict


def load_class_from_disk(class_name: str):
    """
    Load class data from a class data ('.cld') file, return Class object.

    :param class_name: str
    :return: Class object
    """

    class_data_filename = class_name + CLASSLIST_DATA_FILE_TYPE
    classlist_data_path = CLASSLIST_DATA_PATH.joinpath(class_name, class_data_filename)

    loaded_class = Class.from_file(classlist_data_path)
    return loaded_class


def load_chart_data(chart_data_path: str):
    """
    Load class data from chart data ('.cdf') file.

    :param chart_data_path: Path or str
    :return: dict
    """
    chart_data_dict = load_from_json_file(chart_data_path)
    return chart_data_dict


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
