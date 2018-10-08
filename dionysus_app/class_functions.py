"""
Functions for creating, editing, dealing with classes.
"""

import time
from pathlib import Path

from dionysus_app.UI_functions import clean_for_filename, input_is_essentially_blank
from dionysus_app.data_folder import DataFolder

CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)
CLASS_REGISTRY_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_REGISTRY.value)
CLASSLIST_DATA_FILE_TYPE = '.cld'


def create_classlist():

    classlist_name = take_classlist_name_input()  # TODO: Option to cancel creation at class name entry stage

    setup_class(classlist_name)
    create_classlist_data(classlist_name)


def create_classlist_data(classlist_name):  # TODO: fix path composition
    data_file = classlist_name + CLASSLIST_DATA_FILE_TYPE
    classlist_data_path = CLASSLIST_DATA_PATH.joinpath(classlist_name, data_file)

    with open(classlist_data_path, 'w+') as classlist_file:
        cancelled = False
        while True:
            class_data = take_class_data_input()

            if class_data == '':  # Test for empty class.
                cancelled = blank_class_dialogue()
                if cancelled:
                    break
                # else: ie if not cancelled:
                continue
            break  # class_data not empty

        print(f'\nClass: {classlist_name}')
        if cancelled:
            print("No students entered.")
        else:
            print(class_data)

        classlist_file.write(class_data)  # consider using JSON?
        time.sleep(2)


def blank_class_dialogue():
    while True:
        choice = input("Do you want to create an empty class? y/n")
        if choice.upper() == 'Y':
            return True
        if choice.upper() == 'N':
            return False
        # TODO: Option to cancel creation here/after entering a class name (eg made typo in class name)
        print('Please enter y for yes to create empty class, or n to return to student input.')


def take_class_data_input():
    """
    Continues to get pairs of values (student name, avatar filename) unless user type 'end'

    :return: str
    """
    class_data = ''
    while True:

        student_name = take_student_name_input(class_data)
        if student_name.upper() == 'END':
            break

        avatar_filename = take_student_avatar(student_name)
        # else:
        class_data += f'{student_name}, {avatar_filename}\n'  # consider using JSON? dictionaries?
    return class_data


def take_student_name_input(class_data):
    """
    Prompts user for student name.

    :param class_data: str
    :return: str
    """
    while True:
        student_name = input("Enter student name, or 'end': ")
        if input_is_essentially_blank(student_name):  # Do not allow blank input TODO: include dash, underscore
            print('Please enter a valid student name.')
            continue

        if student_name in class_data:  # TODO: search for it in class - if it exists, ask for more input
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


def register_class(classlist_name):
    """
    Register class in class_registry file.
    Create if registry non-existent.

    :param classlist_name: str
    :return: None
    """
    with open(CLASS_REGISTRY_PATH, 'a+') as class_registry:  # open class registry, create if does not exist.
        class_registry.write(f'{classlist_name}\n')


def avatar_file_exists(avatar_file):
    """
    Chcecks if provided file exists.

    :param avatar_file: str
    :return: bool
    """
    return Path(avatar_file).expanduser().resolve().exists()


# TODO: reorder/rearrange functions


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


def classlist_exists(classlist_name):
    """
    Checks if there is .cld file for classlist.

    :param classlist_name: str
    :return: bool
    """
    classlist_file_path = Path(classlist_name, CLASSLIST_DATA_FILE_TYPE)
    return CLASSLIST_DATA_PATH.joinpath(classlist_file_path).exists()


if __name__ == '__main__':
    create_classlist()
    # similarly for edit classlist - with open(classlist_name + '.txt', 'r+') as classlist_file: to edit
