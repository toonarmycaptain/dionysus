"""
Script for composing data set to pass to graph_image_generator.

Prototype will be a bar chart eg columns for each 10pt range 0-100, each avatar stacked on top of each other.

Immediate enhancement from there will be variable ranges for the chart, columns eg 0-15 for a quiz rather than
a percentage, or column widths of 5pts rather than 10. Other potential concern is chart being too high, so some
sort of overlap without obscuring the avatars, or two columns of avatars in a point column.
"""
from pathlib import Path
from typing import Optional, Tuple

import definitions

from dionysus_app.chart_generator.generate_image import generate_chart_image
from dionysus_app.chart_generator.process_chart_data import DEFAULT_CHART_PARAMS
from dionysus_app.class_ import Class
from dionysus_app.class_functions import select_classlist
from dionysus_app.file_functions import copy_file
from dionysus_app.UI_menus.chart_generator.create_chart_UI import (display_image_save_as,
                                                                   save_chart_dialogue,
                                                                   )
from dionysus_app.UI_menus.chart_generator.take_chart_data_UI import (take_chart_name,
                                                                      take_custom_chart_options,
                                                                      take_score_data,
                                                                      )
from dionysus_app.UI_menus.UI_functions import clean_for_filename


def new_chart(loaded_class: Class = None) -> None:
    """
    Create a new chart with supplied class, user input.

    Prompts user to select class if not provided by caller.
    Take chart name, score data, chart parameters from
    assemble_chart_data, form into chart_data_dict with key-value
    format:
        chart_data_dict = {
            'class_name': class_name,  # str
            'chart_name': chart_name,  # str
            'chart_default_filename': chart_default_filename,  # str
            'chart_params': chart_params,  # dict
            'score-avatar_dict': student_scores,  # dict
            }

    Then write this data to disk as *.cdf (ChartDataFile), generate and
    save the chart.

    :param loaded_class: Class = None
    :return: None
    """
    if not loaded_class:
        class_id = select_classlist()  # TODO: warn for empty classlist
        loaded_class = definitions.DATABASE.load_class(class_id)

    chart_name, chart_default_filename, student_scores, chart_params = assemble_chart_data(loaded_class)

    chart_data_dict = {'class_name': loaded_class.name,  # str
                       'chart_name': chart_name,  # str
                       'chart_default_filename': chart_default_filename,  # str
                       'chart_params': chart_params,  # dict
                       'score-avatar_dict': student_scores,  # dict
                       }

    definitions.DATABASE.create_chart(chart_data_dict)

    chart_image_location = generate_chart_image(chart_data_dict)

    # Show image to user, user save image.
    if show_image(chart_image_location):
        user_save_chart_image(chart_data_dict, chart_image_location)


def assemble_chart_data(loaded_class: Class) -> Tuple[str, str, dict, dict]:
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


def set_chart_params() -> dict:
    """
    Get and return chart parameters.

    eg spacing, min/max score etc.

    :return: dict
    """
    return get_custom_chart_options(DEFAULT_CHART_PARAMS)


def get_custom_chart_options(default_params: dict) -> dict:
    """
    Take default parameters dict and modify based on user input.

    # Possible extension to have custom param_dicts for specific user
    preferences/style options rather than UI for every setting

    # replace/create any custom params in chart_opt dict
    # Potential options in those scripts (or here) to include:
    #      - chart/image title options eg name diff from displayed title
    #      - axis labels, scale/axis tick markings
    #      - min/max score, other options/settings varying from defaults
    # dict keys: parameters, values: arguments/set values - NOT FULLY IMPLEMENTED

    :param default_params: dict
    :return: dict
    """
    take_custom_chart_options()

    return default_params


def user_save_chart_image(chart_data_dict: dict, image_location: Path) -> None:
    """
    Ask user for save location, defaulting to user default save folder
    for class, with default chart filename.
    Copies image file from app save folder to user specified location.

    :param chart_data_dict: dict
    :param image_location: Path object
    :return: None
    """
    class_name = chart_data_dict['class_name']
    default_chart_name = chart_data_dict['chart_default_filename']

    # Save in user selected location with user defined name.
    save_chart_pathname = get_user_save_chart_pathname(class_name, default_chart_name)
    if save_chart_pathname:
        copy_image_to_user_save_loc(image_location, save_chart_pathname)


def copy_image_to_user_save_loc(app_image_location: Path, user_save_location: Path) -> None:
    """
    Copies image from app_data location to user selected location.
    NB if

    :param app_image_location: Path object
    :param user_save_location: Path object
    :return: None
    """
    copy_file(app_image_location, user_save_location)


def get_user_save_chart_pathname(class_name: str, default_chart_name: str) -> Optional[Path]:
    """
    Gets set class save folder path, return None if user cancels save.

    Creates class folder in chart_save_folder if necessary.
    Calls save chart dialogue to prompting user input for chart image
    file save path.

    :param class_name: str
    :param default_chart_name: str
    :return: Path or None
    """
    class_save_folder_path = create_class_save_folder(class_name)

    return save_chart_dialogue(default_chart_name, class_save_folder_path)


def create_class_save_folder(class_name: str) -> Path:
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


def get_class_save_folder_path(class_name: str) -> Path:
    """
    Returns Path to the class folder in user set/default chart save
    folder.

    :param class_name: str
    :return: Path object
    :raises ValueError: If DEFAULT_CHART_SAVE_DIR is None/uninitialised.
    """
    if definitions.DEFAULT_CHART_SAVE_DIR is None:
        raise ValueError("Uninitialised DEFAULT_CHART_SAVE_DIR")

    return Path(definitions.DEFAULT_CHART_SAVE_DIR).joinpath(class_name)


def show_image(image_location: Path) -> bool:
    """
    Calls show_image UI, return user input to save image/not.

    Image display also provides UI whether to save image, return this.

    :param image_location: Path object.
    :return: bool
    """
    return display_image_save_as(image_location)
