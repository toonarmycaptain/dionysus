"""
Process input data for image generation code.
"""
from typing import Any

import definitions

from dionysus_app.persistence.databases.json import JSONDatabase
from dionysus_app.student import Student

DEFAULT_CHART_PARAMS = {'column_max_avatars': 10,  # max number of avatars vertically.
                        # Nominally pixels from x-axis to top of image//height of avatar.
                        'avatar_horizontal_offset': 5,  # Spacing between avatars ~ width of avatar
                        'avatar_vertical_offset': 10,  # Spacing between avatars ~ height of avatar
                        'init_vertical_offset': 5,  # Initial offset from x-axis ~ half width of avatar
                        'min_score': 0,
                        'max_score': 100,
                        }


def generate_avatar_coords(score_students_dict: dict[float, list[Student]],
                           class_id: Any,
                           chart_params: dict|None = None):  # set chart params to a default?
    """
    Take score_avatar_dict and transform into dict {avatar: [xy_coords]}

    Takes score_students_dict - dict of scores to lists of Students
    for each score, returns a dictionary with avatar Paths as
    keys, and a list of x,y coordinate tuples as values.

    eg keys: avatar Path, values: list of x, y tuples eg [(80, 80), (90, 90)]

    :param score_students_dict: dict[float, list[Student]]
    :param class_id: Any
    :param chart_params: dict
    :return: dict
    """

    if not chart_params:
        chart_params = DEFAULT_CHART_PARAMS  # pull values from DEFAULT_CHART_PARAMS dict

    # Fetch avatar paths:
    score_avatar_paths_dict = {}
    if isinstance(definitions.DATABASE, JSONDatabase):
        for score in score_students_dict:
            score_avatar_paths_dict[score] = [
                definitions.DATABASE.get_avatar_path(class_id, student.avatar_id)
                for student in score_students_dict[score]]

    else:  # All other db backends:
        for score in score_students_dict:
            score_avatar_paths_dict[score] = [
                definitions.DATABASE.get_avatar_path(student.avatar_id) for student in
                score_students_dict[score]]

    # Re-sort in ascending score order.
    score_avatar_paths_dict = {score: score_avatar_paths_dict[score] for score in sorted(score_avatar_paths_dict)}

    banded_avatars = assign_avatars_to_bands(score_avatar_paths_dict)  # TODO: use DEFAULT_CHART_PARAMS values for offsets.

    # Return avatar_coord_dict
    return assign_avatar_coords(banded_avatars, chart_params)


def assign_avatars_to_bands(score_avatar_dict: dict):
    """
    Iterate over scores and assign score to band (scores in bands will
    thus be in order from lowest to highest).

    :param score_avatar_dict: dict
    :return: dict
    """
    band_dict: dict = {band: [] for band in range(0, 101, 10)}

    for score, avatars in score_avatar_dict.items():
        for band, avatars_in_band in band_dict.items():
            if band - 5 < score <= band + 5:  # 95-100 set greedier than 0-5
                avatars_in_band += avatars

    return band_dict


def assign_avatar_coords(band_avatar_dict, chart_params: dict|None = None):
    """
    Take dict of bands 0-100 by 10 with int values as keys, lists of
    avatar Paths as values.
    Process and translate into dict with avatar Paths as keys, and a
    list of x,y coordinate tuples as values.

    eg keys: avatar Path,
    values: list of x, y tuples eg [(80, 80), (90, 90)]

    Values are in ascending score order when processed into bands, so
    placing lowest score first at the bottom, and the lowest scores into
    the right-most column if more than one column is required for the
    band, maintains the order of score representation visually.

    :param band_avatar_dict: dict
    :param chart_params: dict
    :return: dict
    """
    if not chart_params:
        chart_params = DEFAULT_CHART_PARAMS  # pull values from DEFAULT_CHART_PARAMS dict

    avatar_xy_dict: dict = {}
    col_max_avatars, init_vert_offset, horiz_offset, vert_offset = (
        chart_params['column_max_avatars'],
        chart_params['init_vertical_offset'],
        chart_params['avatar_horizontal_offset'],
        chart_params['avatar_vertical_offset'],
        )

    for band in band_avatar_dict.keys():
        num_col = (len(band_avatar_dict[band]) // col_max_avatars) + 1

        init_x_coord = band - ((num_col - 1) * horiz_offset * 0.5)

        for avatar in range(len(band_avatar_dict[band])):
            x_coord = init_x_coord + horiz_offset * (avatar // col_max_avatars)
            y_coord = init_vert_offset + (avatar % col_max_avatars) * vert_offset
            xy = (x_coord, y_coord)
            avatar_loc = band_avatar_dict[band][avatar]
            # add xy coord to list of coords for avatar
            avatar_xy_dict[avatar_loc] = avatar_xy_dict.get(avatar_loc, []) + [xy]

    return avatar_xy_dict
