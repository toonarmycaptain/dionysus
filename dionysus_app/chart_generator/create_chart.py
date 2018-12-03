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
from dionysus_app.chart_generator.take_chart_data import take_chart_name, take_score_data
from dionysus_app.file_functions import convert_to_json
from dionysus_app.UI_functions import clean_for_filename


CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


def new_chart():
    """
    TODO: write docstring. In particular form for chart_data_dict.
    :return:
    """
    # Select class or redirect to create new class.
    # Take chart_name
    # Take new data set. Store in class_data/{class_name}/chart_data/chart_name.cdf (ChartDataFile)
    # Pass data to chart image creation scripts
    #   - potential options in those scripts (or here) to include:
    #       - chart/image title options eg name different from displayed title
    #       - axis labels, scale/axis tick markings

    chart_name, class_name, student_scores, chart_params = assemble_chart_data()

    chart_data_dict = {'class_name': class_name,
                       'chart_name': chart_name,
                       'chart_params': chart_params,
                       'score-avatar_dict': student_scores,
                       }

    write_chart_data_to_file(chart_data_dict)

    generate_chart_image(chart_data_dict)


def assemble_chart_data():
    """
    TODO: write docstring, reference for return value form.
    :return:
    """

    class_name = select_classlist()  # TODO: warn for empty classlist

    student_scores: dict = take_score_data(class_name)

    chart_name = take_chart_name()

    chart_params = set_chart_params()
    # chart options here or before score entry, setting chart params, min, max scores etc

    return chart_name, class_name, student_scores, chart_params


def write_chart_data_to_file(chart_data_dict: dict):
    """
    ### include class name in chart name as enforced format? eg class_name - chart name

    Write classlist data to disk with format:

    class_data_dict: {
        'class_name':
        'chart_name':
        # date? Not yet implemented.
        'score-avatar_dict':    student_name, score, None for no score.
               # chart_params_dict: Not yet implemented.
            # eg min/max score, other options/settings varying from defaults
            # dict keys: parameters, values: arguments/set values
        }

    :param chart_data_dict: dict
    :return: None
    """
    file_chart_data_dict = deepcopy(chart_data_dict)
    chart_filename = clean_for_filename(file_chart_data_dict['chart_name'])
    chart_data_file = chart_filename + CHART_DATA_FILE_TYPE
    chart_data_filepath = CLASSLIST_DATA_PATH.joinpath(file_chart_data_dict['class_name'], 'chart_data', chart_data_file)

    json_safe_chart_data_dict = sanitise_avatar_path_objects(file_chart_data_dict)
    json_chart_data = convert_to_json(json_safe_chart_data_dict)

    with open(chart_data_filepath, 'w') as chart_data_file:
        chart_data_file.write(json_chart_data)


def set_chart_params():
    default_chart_params = {}  # dict with default chart params goes here.
    chart_params = take_custom_chart_options(default_chart_params)
    return chart_params


def take_custom_chart_options(default_params: dict):
    # replace/create any custom params in chart_opt dict
    # return dict
    return default_params


def sanitise_avatar_path_objects(data_dict: dict):
    """
    chart_data_dict['score-avatar_dict'] is a dict with integer keys, lists of Path objects as values.

    Possible TODO: change to save student name instead of path to avatar?

    :param chart_data_dict: dict
    :return: dict
    """
    for score in list(data_dict['score-avatar_dict'].keys()):
        data_dict['score-avatar_dict'][score] = [str(avatar_Path) for avatar_Path in
                                                       data_dict['score-avatar_dict'][score]]
    return data_dict


if __name__ == '__main__':
    pass
