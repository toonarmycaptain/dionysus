"""
Script for composing data set to pass to graph_image_generator.

Prototype will be a bar graph eg columns for each 10pt range 0-100, each avatar stacked on top of each other.

Immediate enhancement from there will be variable ranges for the graph, columns eg 0-15 for a quiz rather than
apercentage, or column widths of 5pts rather than 10. Other potential concern is graph being too high, so some
sort of overlap without obscuring the avatars, or two columns of avatars in a point column.
"""

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
