"""
Functions for creating, editing, dealing with classes.
"""
import time

from pathlib import Path
from typing import Any, Dict, Optional

import definitions

from dionysus_app.class_ import Class, NewClass
from dionysus_app.student import Student
from dionysus_app.data_folder import DataFolder
from dionysus_app.file_functions import (copy_file,
                                         load_from_json_file)
from dionysus_app.persistence.database import ClassIdentifier
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

DEFAULT_AVATAR_PATH = DataFolder.generate_rel_path(DataFolder.DEFAULT_AVATAR.value)


def create_classlist() -> None:
    """
    Create a new class, then give option to create a chart with new class.

    Calls UI elements to collect new class' data, then writes data to persistence.

    :return: None
    """
    classlist_name = take_classlist_name_input()  # TODO: Option to cancel creation at class name entry stage

    new_class: NewClass = compose_classlist_dialogue(classlist_name)

    definitions.DATABASE.create_class(new_class)
    time.sleep(2)  # Pause for user to look over feedback.

    create_chart_with_new_class(new_class)


def compose_classlist_dialogue(class_name: str) -> NewClass:
    """
    Call UI elements to collect new class data.

    Provide feedback to user reflecting new class composition.

    Creates class object.

    If no students added to class, check if intended, making subsequent
    call to take_class_data_input UI if unintended blank class returned.

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
    Take user supplied avatar image file.

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


def avatar_file_exists(avatar_file: Path) -> bool:
    """
    Checks if provided file exists.

    :param avatar_file: Path
    :return: bool
    """
    return Path(avatar_file).exists()


def create_chart_with_new_class(new_class: NewClass) -> None:
    """
    Prompt to create chart with new class, create chart if desired.

    Prompt user to choose whether to create a chart with a newly created
    class.
    Call new_chart with newly created class if user desires.

    :param new_class: NewClass
    :return: None
    """
    if create_chart_with_new_class_dialogue():
        from dionysus_app.chart_generator.create_chart import new_chart
        new_chart(new_class)


def select_classlist() -> Any:
    """
    Prompt user to select a class from list, return selected Class.

    Display list of existent classes from class_registry and allow user to select one, returning the name of the
    selected class.

    :return: Any - the type ClassIdentifier.id is for backend database.
    """
    class_options = create_class_list_dict()
    display_class_selection_menu(class_options)

    selected_class = take_class_selection(class_options)

    return selected_class.id


def create_class_list_dict() -> Dict[int, ClassIdentifier]:
    """
    Create dict with enumerated class identifiers, starting at 1.

    :return: Dict[int, ClassIdentifier]
    :raises ValueError: If registry is None/uninitialised.
    """
    class_identifiers = definitions.DATABASE.get_classes()
    if class_identifiers is None:
        raise ValueError("No Database found.")

    return {option: class_identifier
            for option, class_identifier in enumerate(class_identifiers, start=1)
            }


def select_student(current_class: Class) -> Student:
    """
    Prompt user to select student from class, return selected Student.

    Display list of students in class and allow user to select one,
    returning the selected Student object.

    :param current_class: Class object
    :return: Student_object
    """
    student_options = {numeral: student.name for numeral, student in enumerate(current_class.students, start=1)}
    display_student_selection_menu(student_options)

    selected_student_name = take_student_selection(student_options)

    return next(student for student in current_class.students
                if student.name == selected_student_name)


def load_chart_data(chart_data_path: str) -> dict:
    """
    Load class data from chart data ('.cdf') file.

    :param chart_data_path: Path or str
    :return: dict
    """
    return load_from_json_file(chart_data_path)


def edit_classlist() -> None:
    """
    Unimplemented functionality to edit class.

    :return: None
    """
    classlist_name = take_classlist_name_input()
    with open(classlist_name + '.txt', 'r+') as classlist_file:
        pass
