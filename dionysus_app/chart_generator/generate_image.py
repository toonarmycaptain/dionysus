"""
Optional feature implementations:

if title/name desired on image:
    fig.subtitle('title_string')
"""

import matplotlib.pyplot as plt

from matplotlib.offsetbox import AnnotationBbox, OffsetImage

from dionysus_app.chart_generator.process_chart_data import generate_avatar_coords

def generate_chart_image(chart_data_dict):
    """

    :param chart_data_dict:
    :return:
    """
    fig = plt.figure(figsize=(16, 9))  # set proportion/size in inches,
    ax = plt.subplot(xlim=(-0, 105), ylim=(-0, 100))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1, wspace=0.01, hspace=0.01)

# TODO: hide vertical axis, top and right border lines.
    set_axis()

    # if custom chart parameters affecting avatar layout, pass chart_data_dict['chart_params'] to generate_avatar_coords

    # nominally, avatar_coord_dict will be chart_data_dict['score-avatar_dict']
    avatar_coord_dict = generate_avatar_coords(chart_data_dict['score-avatar_dict'])

    add_avatars_to_plot(ax, avatar_coord_dict)

    # save fig for test
    plt.savefig(chart_data_dict['chart_name'],  # save filename.png TODO: change file save location
                dpi=120)  # dpi - 120 comes to 1920*1080, 80 - 1280*720

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
    Takes an image path and adds that image to the ax given, at each set of coordinates in the list supplied.

    eg xy_coords = [(10, 90)] will place image at 10, 90
    eg xy_coords = [(10, 90), (25, 25)} will place the image at both 10, 90 and 25, 25. This is intended for use with
    the default avatar, or if future feature allows multiple results.

    :param ax:
    :param avatar_path: Path object
    :param xy_coords: list - list of tuples (x, y)
    :return:
    """
    avatar_image = plt.imread(str(avatar_path))  # matplotlib takes an 8bit string or FILE objectT, not Path object.
    imagebox = OffsetImage(avatar_image, zoom=.4)

    for xy in xy_coords:
        # xy = tuple coordinates to position this image
        ab = AnnotationBbox(imagebox, xy,
                            # xycoords='data',
                            # boxcoords="offset points",
                            )
        ax.add_artist(ab)
        ax.grid(False)  # No grid
        plt.draw()


def add_avatars_to_plot(ax, avatar_coord_dict):
    for avatar_path in avatar_coord_dict.keys():
        xy_coords = avatar_coord_dict[avatar_path]
        add_avatar_to_plot(ax, avatar_path, xy_coords)



if __name__ == '__main__':
    data_dict = {'chart_name': 'testing cart',
                 'score-avatar_dict': {'default_avatar_1.png': [(10, 5), (10, 55), ],
                                       'default_avatar_2.png': [(10, 15), (10, 65), ],
                                       'default_avatar_3.png': [(10, 25), (10, 75), ],
                                       'default_avatar_4.png': [(10, 35), (10, 85), ],
                                       'default_avatar.png': [(10, 45), (10, 95)],
                                       }
                 }
    # offset by 5 and increments of 10 neatly spaces .4 zoom 150px images from x axis and eachother

    generate_chart_image(data_dict)
