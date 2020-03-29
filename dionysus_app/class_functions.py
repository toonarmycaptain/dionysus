"""
Functions for creating, editing, dealing with classes.
"""

import time

from pathlib import Path
from typing import Optional, Union

import definitions

from dionysus_app.class_ import Class, NewClass
from dionysus_app.student import Student
from dionysus_app.class_registry_functions import register_class
from dionysus_app.data_folder import DataFolder, CLASSLIST_DATA_FILE_TYPE
from dionysus_app.file_functions import (copy_file,
                                         load_from_json_file,
                                         move_file)
from dionysus_app.UI_menus.class_functions_UI import (blank_class_dialogue,
                                                      class_data_feedback,
                                                      create_chart_with_new_class_dialogue,
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


def create_classlist() -> None:
    """
    Create a new class, then give option to create a chart with new class.

    Calls UI elements to collect new class' data, then writes data to persistence.

    :return: None
    """
    classlist_name = take_classlist_name_input()  # TODO: Option to cancel creation at class name entry stage

    new_class: NewClass = compose_classlist_dialogue(classlist_name)

    create_classlist_data(new_class)  # Future: Call to Database.create_class(new_class)
    time.sleep(2)  # Pause for user to look over feedback.

    create_chart_with_new_class(new_class)


def setup_class(classlist_name: str) -> None:
    """
    Setup class data storage file structure.
    Register class in class_registry index

    :param classlist_name:
    :return: None
    """
    setup_class_data_storage(classlist_name)  # Database.create_class
    register_class(classlist_name)


def setup_class_data_storage(classlist_name: str) -> None:
    """
    Setup data storage for new classes.

    Structure for data storage:
    app_data/
        class_data/
            class_name/  # folder for each class
                chart_data/  # store chart data sets
                avatars/  # store avatars for class

    Raises ValueError on uninitialised DEFAULT_CHART_SAVE_FOLDER value: value
    should be previously set in:
    run_app
        app_init
            app_config
                app_start_set_default_chart_save_location


    :param classlist_name: str
    :return: None
    :raises ValueError: If DEFAULT_CHART_SAVE_FOLDER is None/uninitialised.
    """
    avatar_path = CLASSLIST_DATA_PATH.joinpath(classlist_name, 'avatars')
    chart_path = CLASSLIST_DATA_PATH.joinpath(classlist_name, 'chart_data')
    if definitions.DEFAULT_CHART_SAVE_FOLDER is None:
        raise ValueError("Uninitialised DEFAULT_CHART_SAVE_FOLDER")
    user_chart_save_folder = definitions.DEFAULT_CHART_SAVE_FOLDER.joinpath(classlist_name)

    avatar_path.mkdir(exist_ok=True, parents=True)
    chart_path.mkdir(exist_ok=True, parents=True)
    user_chart_save_folder.mkdir(exist_ok=True, parents=True)


def create_classlist_data(new_class: NewClass) -> None:
    """
    Creates class data in persistence.
    Calls setup_class to create any needed files, then writes data to file.

    :param new_class: Class object
    :return: None
    """
    setup_class(new_class.name)  # -> functionality moves to (ie function called by) JSONDatabase.create_class
    write_classlist_to_file(new_class)
    move_avatars_to_class_data(new_class)


def move_avatars_to_class_data(new_class: NewClass) -> None:
    """
    Move avatars from NewClass.temp_dir  to new class' avatars directory.

    :param new_class: NewClass
    :return: None
    """
    for avatar_file in [student.avatar_filename for student in new_class.students
                        if student.avatar_filename]:
        move_avatar_to_class_data(new_class, avatar_file)


def move_avatar_to_class_data(new_class: NewClass, avatar_filename: str) -> None:
    """
    Moves avatar from NewClass.temp_dir to new class' avatars directory.
    Will not repeat moves of same filename if image already exists in avatars
    directory, to avoid repeated overwrite with same file.

    :param new_class: NewClass
    :param avatar_filename: str
    :return: None
    """
    origin_path = new_class.temp_avatars_dir.joinpath(avatar_filename)
    destination_path = CLASSLIST_DATA_PATH.joinpath(new_class.name, 'avatars', avatar_filename)
    if not destination_path.exists():  # Avatar not already in database/class data.
        move_file(origin_path, destination_path)


def compose_classlist_dialogue(class_name: str) -> NewClass:
    """
    Call UI elements to collect new class data.
    Provide feedback to user reflecting new class composition.

    Creates class object.

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

    class_data_feedback(new_class)

    return new_class


def take_class_data_input(class_name: str) -> NewClass:
    """
    Take student names, avatars, return Class object.

    :param class_name: str
    :return: Class
    """
    new_class = NewClass(name=class_name)
    while True:
        student_name = take_student_name_input(new_class)
        if student_name.upper() == 'END':
            break
        avatar_filename = take_student_avatar(new_class, student_name)
        new_class.add_student(name=student_name, avatar_filename=avatar_filename)
    return new_class


def take_student_avatar(new_class: NewClass, student_name: str) -> Optional[str]:
    """
    Get avatar for student:
    Prompts user for path to avatar file.
    Copies avatar file to temp dir for class.

    :param new_class: NewClass class object
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
    copy_file(avatar_file, new_class.temp_avatars_dir.joinpath(target_avatar_filename))
    return target_avatar_filename


def avatar_file_exists(avatar_file: Union[str, Path]) -> bool:
    """
    Checks if provided file exists.

    :param avatar_file: str
    :return: bool
    """
    return Path(avatar_file).exists()


def write_classlist_to_file(current_class: Class) -> None:
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


def create_chart_with_new_class(new_class: NewClass) -> None:
    """
    Prompt to create a chart with a newly created class, call new_chart with
    newly created class if user desires.

    :param new_class: NewClass
    :return: None
    """
    if create_chart_with_new_class_dialogue():
        from dionysus_app.chart_generator.create_chart import new_chart
        new_chart(new_class)


def select_classlist() -> str:
    """
    Display list of existent classes from class_registry and allow user to select one, returning the name of the
    selected class.

    :return: str
    """
    class_options = create_class_list_dict()
    display_class_selection_menu(class_options)  # TODO: Select class or redirect to create new class.

    selected_class = take_class_selection(class_options)

    return selected_class


def create_class_list_dict() -> dict:
    """
    Create dict with enumerated classes, starting at 1.

    :return: dict
    :raises ValueError: If registry is None/uninitialised.
    """

    if definitions.REGISTRY is None:
        raise ValueError("RegistryError: Registry uninitialised.")
    class_dict = {option: class_name for option, class_name in enumerate(definitions.REGISTRY, start=1)}
    return class_dict


def select_student(current_class: Class) -> Student:
    """
    Display list of students in class and allow user to select one, returning
    the selected Student object.

    :param current_class: Class object
    :return: Student_object
    """
    student_options = {numeral: student.name for numeral, student in enumerate(current_class.students, start=1)}
    display_student_selection_menu(student_options)

    selected_student_name = take_student_selection(student_options)

    return next(student for student in current_class.students
                if student.name == selected_student_name)


def load_class_from_disk(class_name: str) -> Class:
    """
    Load class data from a class data ('.cld') file, return Class object.

    :param class_name: str
    :return: Class object
    """

    class_data_filename = class_name + CLASSLIST_DATA_FILE_TYPE
    classlist_data_path = CLASSLIST_DATA_PATH.joinpath(class_name, class_data_filename)

    loaded_class = Class.from_file(classlist_data_path)
    return loaded_class


def load_chart_data(chart_data_path: str) -> dict:
    """
    Load class data from chart data ('.cdf') file.

    :param chart_data_path: Path or str
    :return: dict
    """
    chart_data_dict = load_from_json_file(chart_data_path)
    return chart_data_dict


def get_avatar_path(class_name: str, student_avatar: str = None) -> Path:
    """
    Take value from 'avatar' in list of student data, return path for student avatar or default avatar path if student
    has no avatar.
    Defaults to default avatar if none provided.

    :param class_name: str
    :param student_avatar: str or None
    :return: Path object
    """
    if student_avatar is None:
        return DEFAULT_AVATAR_PATH
    return avatar_path_from_string(class_name, student_avatar)


def avatar_path_from_string(class_name: str, avatar_filename: str) -> Path:
    """
    Take class name and student's avatar filename, return a Path object to the avatar image file.

    :param class_name: str
    :param avatar_filename: str
    :return: Path object
    """
    return CLASSLIST_DATA_PATH.joinpath(class_name, 'avatars', avatar_filename)


def edit_classlist() -> None:
    """
     similarly to create classlist: for edit classlist -
    :return:
    """
    classlist_name = take_classlist_name_input()
    with open(classlist_name + '.txt', 'r+') as classlist_file:
        pass
