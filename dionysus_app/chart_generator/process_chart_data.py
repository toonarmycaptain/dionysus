"""
Process input data for image generation code.
"""
DEFAULT_CHART_PARAMS = {'column_max_avatars': 10,  # max number of avatars vertically.
                        # Nominally pixels from x-axis to top of image//height of avatar.
                        'avatar_horizontal_offset': 5,  # Spacing between avatars ~ width of avatar
                        'avatar_vertical_offset': 10,  # Spacing between avatars ~ height of avatar
                        'init_vertical_offset': 5,  # Initial offset from x-axis ~ half width of avatar
                        'min_score': 0,
                        'max_score': 100,
                        }


def generate_avatar_coords(score_avatar_dict: dict, chart_params: dict = None):  # set chart params to a default?
    """
    Takes score_avatar_dict - dict of scores to lists of avatar image locations for each score, returns a dictionary
    with avatar Paths as keys, and a list of x,y coordinate tuples as values.

    eg keys: avatar Path, values: list of x, y tuples eg [(80, 80), (90, 90)]

    :param score_avatar_dict: dict
    :param chart_params: dict
    :return: dict
    """

    if not chart_params:
        chart_params = DEFAULT_CHART_PARAMS  # pull values from DEFAULT_CHART_PARAMS dict

    # Re-sort in ascending score order.
    score_avatar_dict = {score: score_avatar_dict[score] for score in sorted(score_avatar_dict)}

    banded_avatars = assign_avatars_to_bands(score_avatar_dict)  # TODO: use DEFAULT_CHART_PARAMS values for offsets.

    avatar_coord_dict = assign_avatar_coords(banded_avatars, chart_params)

    return avatar_coord_dict


def assign_avatars_to_bands(score_avatar_dict: dict):
    """
    Sort and ten  in order from lowest to highest.
    Iterate over scores and assign score to band (scores in bands will
    thus be in order from lowest to highest).

    :param score_avatar_dict: dict
    :return: dict
    """
    band_dict = {band: [] for band in range(0, 101, 10)}

    for score in score_avatar_dict.keys():
        for band in band_dict:
            if band - 5 < score <= band + 5:  # 95-100 set greedier than 0-5
                band_dict[band] += score_avatar_dict[score]

    return band_dict


def assign_avatar_coords(band_avatar_dict, chart_params=DEFAULT_CHART_PARAMS):
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
    avatar_xy_dict = {}
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


if __name__ == '__main__':
    pass
