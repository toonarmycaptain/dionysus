"""
Script for composing data set to pass to graph_image_generator.

Prototype will be a bar chart eg columns for each 10pt range 0-100, each avatar stacked on top of each other.

Immediate enhancement from there will be variable ranges for the chart, columns eg 0-15 for a quiz rather than
a percentage, or column widths of 5pts rather than 10. Other potential concern is chart being too high, so some
sort of overlap without obscuring the avatars, or two columns of avatars in a point column.
"""
from copy import deepcopy

from dionysus_app.class_functions import select_classlist
from dionysus_app.data_folder import CHART_DATA_FILE_TYPE, DataFolder
from dionysus_app.chart_generator.generate_image import generate_chart_image
from dionysus_app.chart_generator.process_chart_data import DEFAULT_CHART_PARAMS
from dionysus_app.chart_generator.take_chart_data import take_chart_name, take_score_data
from dionysus_app.file_functions import convert_to_json
from dionysus_app.UI_menus.UI_functions import clean_for_filename


CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


def new_chart():
    """
    Take class name selection, chart name, score data, chart parameters from
    assemble_chart_data, form into chart_data_dict with key-value format:
        chart_data_dict = {
                    'class_name': class_name,  # str
                    'chart_name': chart_name,  # str
                    'chart_default_filename': chart_default_filename,  # str
                    'chart_params': chart_params,  # dict
                    'score-avatar_dict': student_scores,  # dict
                    }

    Then write this data to disk as *.cdf (ChartDataFile), generate and save the chart.

    :return: None
    """
    class_name, chart_name, chart_default_filename, student_scores, chart_params = assemble_chart_data()

    chart_data_dict = {'class_name': class_name,  # str
                       'chart_name': chart_name,  # str
                       'chart_default_filename': chart_default_filename,  # str
                       'chart_params': chart_params,  # dict
                       'score-avatar_dict': student_scores,  # dict
                       }

    write_chart_data_to_file(chart_data_dict)

    generate_chart_image(chart_data_dict)


def assemble_chart_data():
    """
    Collect data/user input for new chart.

    Return values for chart_data_dict assembly:
    class_name: str
    chart_name: str
    chart_filename: str
    student_scores: dict
    chart_params: dict

    :return: tuple(str, str, str, dict, dict)
    """

    class_name = select_classlist()  # TODO: warn for empty classlist

    student_scores: dict = take_score_data(class_name)

    chart_name = take_chart_name()

    chart_filename = clean_for_filename(chart_name)

    chart_params = set_chart_params()
    # chart options here or before score entry, setting chart params, min, max scores etc

    return class_name, chart_name, chart_filename,  student_scores, chart_params


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
    chart_params = take_custom_chart_options(DEFAULT_CHART_PARAMS)
    return chart_params


def take_custom_chart_options(default_params: dict):
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


if __name__ == '__main__':
    pass
