"""
Script for taking and saving data for graph.
"""


# score entry:

from dionysus_app.class_functions import load_class_data
from dionysus_app.data_folder import CHART_DATA_FILE_TYPE, DataFolder
from dionysus_app.file_functions import convert_to_json

IMAGE_DATA_PATH = DataFolder.generate_rel_path(DataFolder.IMAGE_DATA.value)


def take_score_data(class_name):
    class_data_dict = load_class_data(class_name)

    student_scores = {}
    for student_name in list(class_data_dict.keys()):

        student_scores[student_name] = take_score_entry(student_name)

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


def write_chart_data_to_file(chart_name: str,
                             score_data_dict: dict,
                             chart_data_dict: dict):
    """
    ### chart_name, pass score_data, chart_data as a dict or tuple?
    ### include class name in chart name as enforced format? eg class_name - chart name



    Write classlist data to disk with format:

    Chart name
    Classlist name
    JSON'd class data dict  # Second line, when reading JSON back in.
        dict keys: student_names, values: scores, None for no score.

    JSON'd graph settings/options dict # Third line of file
        dict keys: settings varying from default, values: set values

    :param chart_name:
    :param score_data_dict:
    :param chart_data_dict:
    :return:
    """
    chart_data_file = chart_name + CHART_DATA_FILE_TYPE
    chart_data_path = IMAGE_DATA_PATH.joinpath(chart_name, chart_data_file)
    # TODO: rename 'image' and 'graph' to 'chart' where they appear,
    # apart from where 'image' is correct (ie referring to actual image/image file.

    json_score_data = convert_to_json(score_data_dict)
    json_chart_data = convert_to_json(chart_data_dict)

    with open(chart_data_path, 'w') as chart_data_file:
        chart_data_file.write(f'{chart_name}\n')
        chart_data_file.write(json_score_data)
        chart_data_file.write(json_chart_data)


if __name__ == '__main__':
    pass
