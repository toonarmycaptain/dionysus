"""
Script for composing data set to pass to graph_image_generator.

Prototype will be a bar chart eg columns for each 10pt range 0-100, each avatar stacked on top of each other.

Immediate enhancement from there will be variable ranges for the chart, columns eg 0-15 for a quiz rather than
a percentage, or column widths of 5pts rather than 10. Other potential concern is chart being too high, so some
sort of overlap without obscuring the avatars, or two columns of avatars in a point column.
"""
from copy import deepcopy
from pathlib import Path

import definitions

from dionysus_app.chart_generator.generate_image import generate_chart_image
from dionysus_app.chart_generator.process_chart_data import DEFAULT_CHART_PARAMS
from dionysus_app.class_ import Class
from dionysus_app.class_functions import select_classlist, load_class_from_disk
from dionysus_app.data_folder import CHART_DATA_FILE_TYPE, DataFolder
from dionysus_app.file_functions import convert_to_json, copy_file
from dionysus_app.UI_menus.chart_generator.create_chart_UI import (display_image_save_as,
                                                                   save_chart_dialogue,
                                                                   )
from dionysus_app.UI_menus.chart_generator.take_chart_data_UI import (take_chart_name,
                                                                      take_score_data,
                                                                      take_custom_chart_options,
                                                                      )
from dionysus_app.UI_menus.UI_functions import clean_for_filename

CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


def new_chart(loaded_class: Class = None):
    """
    Prompts user to select class if not provided by caller.
    Take chart name, score data, chart parameters from assemble_chart_data,
    form into chart_data_dict with key-value format:
        chart_data_dict = {
                    'class_name': class_name,  # str
                    'chart_name': chart_name,  # str
                    'chart_default_filename': chart_default_filename,  # str
                    'chart_params': chart_params,  # dict
                    'score-avatar_dict': student_scores,  # dict
                    }

    Then write this data to disk as *.cdf (ChartDataFile), generate and save the chart.

    :param loaded_class: Class = None
    :return: None
    """
    if not loaded_class:
        class_name = select_classlist()  # TODO: warn for empty classlist
        loaded_class = load_class_from_disk(class_name)

    chart_name, chart_default_filename, student_scores, chart_params = assemble_chart_data(loaded_class)

    chart_data_dict = {'class_name': loaded_class.name,  # str
                       'chart_name': chart_name,  # str
                       'chart_default_filename': chart_default_filename,  # str
                       'chart_params': chart_params,  # dict
                       'score-avatar_dict': student_scores,  # dict
                       }

    write_chart_data_to_file(chart_data_dict)

    chart_image_location = generate_chart_image(chart_data_dict)

    # Show image to user, user save image.
    show_image(chart_image_location)
    user_save_chart_image(chart_data_dict, chart_image_location)


def assemble_chart_data(loaded_class: Class):
    """
    Collect data/user input for new chart.

    Get classname from user, if not provided, load class data,
    take chart data from user.

    Return values for chart_data_dict assembly:
    loaded_class: Class
    chart_name: str
    chart_filename: str
    student_scores: dict
    chart_params: dict

    :param loaded_class: str = None
    :return: tuple(str, str, dict, dict)
    """
    student_scores: dict = take_score_data(loaded_class)

    chart_name = take_chart_name()

    chart_filename = clean_for_filename(chart_name)

    chart_params = set_chart_params()
    # chart options here or before score entry, setting chart params, min, max scores etc

    return chart_name, chart_filename, student_scores, chart_params


def write_chart_data_to_file(chart_data_dict: dict):
    """
    Saves chart data to disk as JSON in class' chart_data folder.

    Filename is chart name sanitised to a suitable string.

    Pathlib Path objects are not json-serializable, so data dict is converted to
    a JSON-safe form before conversion to JSON

    Write classlist data to disk with format:
    chart_data_dict = {
                'class_name': class_name,  str
                'chart_name': chart_name,  str
                'chart_default_filename': chart_default_filename,  str
                 # date? Not yet implemented.
                'chart_params': chart_params,  dict
                    dict of chart parameters and settings
                'score-avatar_dict': student_scores,  dict
                }

    CAUTION: conversion to JSON will convert int/float keys in score_avatar_dict
    to strings, and keep them as strings when loading.
    This could be handled if necessary by running something like:
    original_score_avatar_dict = {
        float(score): avatar_list for score, avatar_list in dejsonified_score_avatar_dict.items()}

    :param chart_data_dict: dict
    :return: None
    """
    file_chart_data_dict = deepcopy(chart_data_dict)  # Copy so as to not modify in-use dict.

    chart_filename = file_chart_data_dict['chart_default_filename']
    chart_data_file = chart_filename + CHART_DATA_FILE_TYPE
    chart_data_filepath = CLASSLIST_DATA_PATH.joinpath(
        file_chart_data_dict['class_name'], 'chart_data', chart_data_file)

    # Convert data_dict to JSON-safe form.
    json_safe_chart_data_dict = sanitise_avatar_path_objects(file_chart_data_dict)
    json_chart_data = convert_to_json(json_safe_chart_data_dict)

    with open(chart_data_filepath, 'w') as chart_data_file:
        chart_data_file.write(json_chart_data)


def set_chart_params():
    chart_params = get_custom_chart_options(DEFAULT_CHART_PARAMS)
    return chart_params


def get_custom_chart_options(default_params: dict):
    """
    Take default parameters dict and apply modifications based on user input.

    # Possible extension to have custom param_dicts for specific user preferences/style options
        rather than UI for every setting

    # replace/create any custom params in chart_opt dict
    # Potential options in those scripts (or here) to include:
    #      - chart/image title options eg name different from displayed title
    #      - axis labels, scale/axis tick markings
    #      - min/max score, other options/settings varying from defaults
    # dict keys: parameters, values: arguments/set values - NOT FULLY IMPLEMENTED

    :param default_params: dict
    :return: dict
    """
    take_custom_chart_options()

    return default_params


def sanitise_avatar_path_objects(data_dict: dict):
    """
    chart_data_dict['score-avatar_dict'] is a dict with integer keys, lists of Path objects as values.

    Possible TODO: change to save student name as well as path to avatar used?

    :param data_dict: dict
    :return: dict
    """
    for score in list(data_dict['score-avatar_dict'].keys()):
        data_dict['score-avatar_dict'][score] = [str(avatar_Path) for avatar_Path
                                                 in data_dict['score-avatar_dict'][score]]
    return data_dict


def user_save_chart_image(chart_data_dict: dict, image_location: Path):
    """
    Ask user for save location, defaulting to user default save folder
    for class, with default chart filename. Copies image file from app's
    save folder to users.

    :param chart_data_dict: dict
    :param image_location: Path object
    :return: None
    """
    class_name = chart_data_dict['class_name']
    default_chart_name = chart_data_dict['chart_default_filename']

    # Save in user selected location with user defined name.
    save_chart_pathname = get_user_save_chart_pathname(class_name, default_chart_name)
    copy_image_to_user_save_loc(image_location, save_chart_pathname)


def copy_image_to_user_save_loc(app_image_location: Path, user_save_location: Path):
    """
    Copies image from app_data location to user selected location.

    :param app_image_location: Path object
    :param user_save_location: Path object
    :return: None
    """
    copy_file(app_image_location, user_save_location)


def get_user_save_chart_pathname(class_name: str, default_chart_name: str):
    """
    Gets set class save folder path, creating class folder in
    chart_save_folder if necessary.

    Calls save chart dialogue to prompting user input for chart image
    file save path.

    :param class_name: str
    :param default_chart_name: str
    :return: str
    """
    class_save_folder_path = create_class_save_folder(class_name)

    save_chart_path_str = save_chart_dialogue(default_chart_name, class_save_folder_path)
    return save_chart_path_str


def create_class_save_folder(class_name: str):
    """
    Create class folder in user set/default chart save location if
    necessary.
    Return Path to created/existing folder.

    :param class_name: str
    :return: Path object
    """
    class_save_folder_path = get_class_save_folder_path(class_name)
    class_save_folder_path.mkdir(parents=True, exist_ok=True)  # create class_save_folder if nonexistent
    return class_save_folder_path


def get_class_save_folder_path(class_name: str):
    """
    Returns Path to the class folder in user set/default chart save
    folder.

    :param class_name: str
    :return: Path object
    :raises ValueError: If DEFAULT_CHART_SAVE_FOLDER is None/uninitialised.
    """
    if definitions.DEFAULT_CHART_SAVE_FOLDER is None:
        raise ValueError("Uninitialised DEFAULT_CHART_SAVE_FOLDER")

    class_save_folder_path = Path(definitions.DEFAULT_CHART_SAVE_FOLDER).joinpath(class_name)
    return class_save_folder_path


def show_image(image_location: Path):
    """
    Calls show_image UI.

    :param image_location: Path object.
    :return: None
    """
    display_image_save_as(image_location)
