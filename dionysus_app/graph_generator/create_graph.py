"""
Script for composing data set to pass to graph_image_generator.

Prototype will be a bar graph eg columns for each 10pt range 0-100, each avatar stacked on top of each other.

Immediate enhancement from there will be variable ranges for the graph, columns eg 0-15 for a quiz rather than
a percentage, or column widths of 5pts rather than 10. Other potential concern is graph being too high, so some
sort of overlap without obscuring the avatars, or two columns of avatars in a point column.
"""
from dionysus_app.class_functions import select_classlist
from dionysus_app.graph_generator.take_graph_data import take_score_data


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
    print(f'Enter student scores for {class_name}: ')
    student_scores: dict = take_score_data(class_name)


if __name__ == '__main__':
    pass
