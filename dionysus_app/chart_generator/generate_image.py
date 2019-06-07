"""
Optional feature implementations:

if title/name desired on image:
    fig.subtitle('title_string')
"""
from pathlib import Path

import matplotlib.pyplot as plt

from matplotlib.offsetbox import AnnotationBbox, OffsetImage

from dionysus_app.chart_generator.process_chart_data import generate_avatar_coords
from dionysus_app.class_functions import avatar_file_exists, DEFAULT_AVATAR_PATH
from dionysus_app.data_folder import DataFolder

CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


def generate_chart_image(chart_data_dict: dict) -> Path:
    """
    Create the chart image with given input, return image Path.

    :param chart_data_dict: dict
    :return: Path object
    """
    fig = plt.figure(figsize=(16, 9))  # set proportion/size in inches,
    ax = plt.subplot(xlim=(-0, 105), ylim=(-0, 100))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1, wspace=0.01, hspace=0.01)

# TODO: hide vertical axis, top and right border lines.
    set_axis()
    ax.grid(False)  # No grid

    # if custom chart parameters affecting avatar layout, pass chart_data_dict['chart_params'] to generate_avatar_coords

    # nominally, avatar_coord_dict will be chart_data_dict['score-avatar_dict']
    avatar_coord_dict = generate_avatar_coords(chart_data_dict['score-avatar_dict'])

    add_avatars_to_plot(ax, avatar_coord_dict)

    image_location = save_chart_image(chart_data_dict)

    return image_location


def set_axis(x_min: int=0, x_max: int=100, x_step: int=10):
    plt.xticks([tick for tick in range(x_min, x_max+1, x_step)])
    plt.yticks([])


def add_avatar_to_plot(ax, avatar_path, xy_coords: list) -> None:
    """
    Takes an image path and adds that image to the ax given, at each set of coordinates in the list supplied.

    eg xy_coords = [(10, 90)] will place image at 10, 90
    eg xy_coords = [(10, 90), (25, 25)} will place the image at both 10, 90 and 25, 25. This is intended for use with
    the default avatar, or if future feature allows multiple results.

    :param ax:
    :param avatar_path: Path object
    :param xy_coords: list - list of tuples (x, y)
    :return: None
    """
    valid_avatar_path = validate_avatar(avatar_path)

    avatar_image = plt.imread(str(valid_avatar_path))  # matplotlib takes an 8bit str or FILE object, not Path object.
    imagebox = OffsetImage(avatar_image, zoom=.4)

    for xy in xy_coords:
        # xy = tuple coordinates to position this image
        ab = AnnotationBbox(imagebox, xy,
                            # xycoords='data',
                            # boxcoords="offset points",
                            )
        ax.add_artist(ab)
        plt.draw()


def validate_avatar(avatar_path):
    """
    Validates the existence of the supplied path.

    :param avatar_path: Path
    :return: Path
    """
    if not avatar_file_exists(avatar_path):
        return DEFAULT_AVATAR_PATH

    return avatar_path


def add_avatars_to_plot(ax, avatar_coord_dict: dict):
    """
    Takes dict mapping avatar paths to lists of coordinates at which to plot them, calls add_avatar_to_plot on each
    avatar path - coordinate list pair.

    :param ax:
    :param avatar_coord_dict: dict
    :return: None
    """
    for avatar_path in avatar_coord_dict.keys():
        xy_coords = avatar_coord_dict[avatar_path]
        add_avatar_to_plot(ax, avatar_path, xy_coords)


def save_chart_image(chart_data_dict: dict):
    """
    Save figure to app_data/classname/chart_data with same filename as
    chart_name and chart_data_file name.

    :param chart_data_dict: dict
    :return: Path object
    """

    class_name = chart_data_dict['class_name']
    default_chart_name = chart_data_dict['chart_default_filename']
    app_data_save_pathname = Path(CLASSLIST_DATA_PATH).joinpath(class_name, 'chart_data', default_chart_name + '.png')

    # Save in app_data/class_data/class_name/chart_data with chart_default_filename
    plt.savefig(app_data_save_pathname,
                dpi=120)  # dpi - 120 comes to 1920*1080, 80 - 1280*720
    return app_data_save_pathname


if __name__ == '__main__':
    data_dict = {'chart_name': 'testing cart',
                 'score-avatar_dict': {10: ['default_avatar_1.png',
                                            'default_avatar_2.png',
                                            'default_avatar_3.png',
                                            'default_avatar_4.png',
                                            'default_avatar.png',
                                            ]
                                       }
                 }
    # offset by 5 and increments of 10 neatly spaces .4 zoom 150px images from x axis and eachother

    generate_chart_image(data_dict)
