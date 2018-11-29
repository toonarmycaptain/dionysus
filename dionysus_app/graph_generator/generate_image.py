"""
Optional feature implementations:

if title/name desired on image:
    fig.subtitle('title_string')
"""

import matplotlib.pyplot as plt

from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib._png import read_png


def generate_chart_image(chart_data_dict):
    """

    :param chart_data_dict:
    :return:
    """
    fig = plt.figure(figsize=(16, 9), dpi=120)  # set size in inches, dpi - comes to 1920*1080
    # fig = plt.figure(figsize=(16, 9), dpi=80)  # set size in inches, dpi - comes to 1280*720

    ax = plt.subplot(111, xlim=(-0, 100), ylim=(-0, 100))
# SET AXIS X 0-100, Y 0-? based on max band data points
# HIDE VERTICAL AXIS
    set_axis()

    avatar_coord_dict = generate_avatar_coords(chart_data_dict['score-avatar_dict'])
    add_avatars_to_plot(ax, avatar_coord_dict)

    # save fig for test
    plt.savefig(chart_data_dict['chart_name'],
                # bbox_inches='tight',
                pad_inches=0)  # save filename.png, cropping tightly without cutting off anything, with zero padding added.


    # Maximise displayed image.
    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")



    # Show image.
    plt.show()


def set_axis(x_min=0, x_max=100, x_step=10):
    plt.xticks([tick for tick in range(x_min, x_max+1, x_step)])
    plt.yticks([])


def add_avatar_to_plot(ax, avatar_path, xy_coords: list):
    """

    :param ax:
    :param avatar_path: Path object
    :param xy_coords: tuple (x, y)
    :return:
    """
    avatar_image = read_png(avatar_path)
    imagebox = OffsetImage(avatar_image, zoom=.25)

    for xy in xy_coords:
        # xy = tuple coordinates to position this image
        ab = AnnotationBbox(imagebox, xy,
                            # xycoords='data',
                            # boxcoords="offset points",
                            )
        ax.add_artist(ab)
        ax.grid(False)  # No grid
        plt.draw()


# import itertools
# y_image_coords = itertools.count(start=init_avatar_offset_from_axis, step=offset_per_avatar)
# next(y_image_coords)  # yields 4, 11, 18, 25...each time it is called.

def generate_avatar_coords(score_avatars_dict):

    # take chart_data_dict['score-avatar_dict'] and translate into dict
    # with keys: avatar path, values: list of x, y tuples eg [(80, 80), (90, 90)]

    pass


def add_avatars_to_plot(ax, avatar_coord_dict):
    # for avatar in avatar_coord_dict:
    #
    pass


if __name__ == '__main__':
    data_dict = {'default_avatar_1.png': [(10, 4)],
                 'default_avatar_2.png': [(10, 11)],
                 'default_avatar_3.png': [(10, 18)],
                 'default_avatar.png': [(25, 25)],
                 }
    # offset by 4 and increments of 7 nearly spaces .25 zoom 150px images from x axis and eachother

    generate_chart_image(data_dict)
