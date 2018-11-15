"""
Script for composing data set to pass to graph_image_generator.

Prototype will be a bar graph eg columns for each 10pt range 0-100, each avatar stacked on top of each other.

Immediate enhancement from there will be variable ranges for the graph, columns eg 0-15 for a quiz rather than
a percentage, or column widths of 5pts rather than 10. Other potential concern is graph being too high, so some
sort of overlap without obscuring the avatars, or two columns of avatars in a point column.
"""
from dionysus_app.class_functions import select_classlist
from dionysus_app.data_folder import CHART_DATA_FILE_TYPE, DataFolder
from dionysus_app.graph_generator.take_graph_data import take_chart_name, take_score_data
from dionysus_app.file_functions import convert_to_json
from dionysus_app.UI_functions import clean_for_filename


CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


def new_graph():
    """

    :return:
    """
    # Select class or redirect to create new class.
    # Take graph_name
    # Take new data set. Store in class_data/{class_name}/graph_data/graph_name.cgd (ClassGraphData)
    # Pass data to graph image creation scripts
    #   - potential options in those scripts (or here) to include:
    #       - graph/image title options
    #       - axis labels, scale/axis tick markings

    # chart_name
    class_name = select_classlist()
    # TODO: warn for empty classlist

    student_scores: dict = take_score_data(class_name)

    chart_name = take_chart_name()

    chart_data_dict = {'class_name': class_name, 'chart_name': chart_name, 'score-avatar_dict': student_scores}

    # chart options here or before score entry, setting chart params, min, max scores etc

    generate_chart_image(chart_data_dict)


def write_chart_data_to_file(chart_data_dict: dict):
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
    chart_filename = clean_for_filename(chart_data_dict['chart_name'])
    chart_data_file = chart_filename + CHART_DATA_FILE_TYPE
    chart_data_filepath = CLASSLIST_DATA_PATH.joinpath(chart_data_dict['class_name'], 'graph_data', chart_data_file)

    json_chart_data = convert_to_json(chart_data_dict)

    with open(chart_data_filepath, 'w') as chart_data_file:
        chart_data_file.write(json_chart_data)


def generate_chart_image(chart_data):
    pass


if __name__ == '__main__':
    new_graph()
    pass
