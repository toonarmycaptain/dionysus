"""
Script for taking and saving data for graph.
"""

# score entry:

from dionysus_app.class_functions import load_class_data, get_avatar_path
from dionysus_app.data_folder import CHART_DATA_FILE_TYPE, DataFolder
from dionysus_app.file_functions import convert_to_json


CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


def take_score_data(class_name):
    class_data_dict = load_class_data(class_name)

    student_scores = {}
    for student_name in list(class_data_dict.keys()):

        student_avatar_filename = class_data_dict[student_name][0]
        avatar_path = get_avatar_path(class_name, student_avatar_filename)

        student_score = take_score_entry(student_name)
        # add avatar to list of avatars for score
        student_scores[student_score] = student_scores.get(student_score, []).append(avatar_path)

    return student_scores


def take_score_entry(student_name: str, minimum: int=0, maximum: int=100):
    """

    :param student_name: str
    :param minimum: int, default=0  # is there a more correct way to document default keyword arguments?
    :param maximum: int, default=100
    :return:
    """
    while True:
        score = input(f'{student_name}: ')

        if score == '_':
            return None  # do not include student in graph eg if absent

        try:
            score_float = float(score)
        except ValueError:
            print("InputError: please enter a number or '_' to exclude student.")
            continue
        # else:
        if score_float < minimum or score_float > maximum:
            print(f'InputError: Please enter a number between {minimum} and {maximum}.')
            continue
        return score_float


def write_chart_data_to_file(class_name: str, chart_data_dict: dict):
    """
    ### chart_name, pass score_data, chart_data as a dict or tuple?
    ### include class name in chart name as enforced format? eg class_name - chart name



    Write classlist data to disk with format:

    Dict: {
        class_name:
        chart_name:
        date?
        score_data_dict:    student_name, score, None for no score.
        chart_params_dict: min/max score, other options

    JSON'd graph settings/options dict # Third line of file
        dict keys: settings varying from default, values: set values

    :param class_name: str
    :param chart_data_dict: dict
    :return:
    """
    chart_data_file = chart_data_dict[chart_name] + CHART_DATA_FILE_TYPE
    chart_data_path = CLASSLIST_DATA_PATH.joinpath(class_name, 'graph_data', chart_data_file)

    json_chart_data = convert_to_json(chart_data_dict)

    with open(chart_data_path, 'w') as chart_data_file:
        chart_data_file.write(json_chart_data)


if __name__ == '__main__':
    pass
