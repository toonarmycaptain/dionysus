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
                        # TODO: put avatar offsets here
                        }


def generate_avatar_coords(score_avatar_dict: dict, chart_params: dict = None):  # set chart params to a default?
    """
    score_avatar_dict - dict of scores to lists of avatar image locations for each score.

    :type chart_params: dict
    :param score_avatar_dict: dict
    :param chart_params: dict
    :return:
    """
    # take chart_data_dict['score-avatar_dict'] and translate into dict
    # with keys: avatar path, values: list of x, y tuples eg [(80, 80), (90, 90)]

    # chart_data_dict['chart_params'] - dict of any chart option settings etc.
    #
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
    Iterate over scores and assign score to band (scores in bands will thus be in order from lowest to highest).

    :param score_avatar_dict: dict
    :return: dict
    """
    band_dict = {0: [],
                 10: [],
                 20: [],
                 30: [],
                 40: [],
                 50: [],
                 60: [],
                 70: [],
                 80: [],
                 90: [],
                 100: [],
                 }

    for score in score_avatar_dict.keys():
        for band in band_dict:
            if band - 5 < score <= band + 5:  # 95-100 set greedier than 0-5
                band_dict[band] += score_avatar_dict[score]

    return band_dict


def assign_avatar_coords(band_avatar_dict, chart_params=DEFAULT_CHART_PARAMS):
    # iterate over avatars in lists from lowest to highest
    # if more than one column, place in left-most column first so highest scores are rightmost

    # if 2 columns, offest by 2.5 either side of band eg 87.5, 92.5 for 90

    # import itertools
    # y_image_coords = itertools.count(start=init_avatar_offset_from_axis, step=offset_per_avatar)
    # next(y_image_coords)  # yields 4, 11, 18, 25...each time it is called.

    avatar_xy_dict = {}
    col_max_avatars, init_vert_offset, horiz_offset, vert_offset = (chart_params['column_max_avatars'],
                                                                    chart_params['init_vertical_offset'],
                                                                    chart_params['avatar_horizontal_offset'],
                                                                    chart_params['avatar_vertical_offset'],
                                                                    )

    for band in band_avatar_dict.keys():  # iterate over bands in band_avatar_dict
        num_col = (len(band_avatar_dict[band]) // col_max_avatars) + 1
        init_x_coord = band - ((num_col - 1) * horiz_offset * 0.5)
        for avatar in range(len(band_avatar_dict[band])):
            x_coord = init_x_coord + horiz_offset * (avatar // col_max_avatars)
            y_coord = init_vert_offset + (avatar % col_max_avatars) * vert_offset
            xy = (x_coord, y_coord)
            avatar_loc = band_avatar_dict[band][avatar]
            # add xy coord to list of coords for avatar
            avatar_xy_dict[avatar_loc] = avatar_xy_dict.get(avatar_loc, []) + [xy]

        # if len(band_avatar_dict[band]) < col_max_avatars:
        #     for avatar in range(len(band_avatar_dict[band])):
        #         xy = (band, init_vert_offset + avatar*vert_offset)
        #         avatar_loc = band_avatar_dict[band][avatar]
        #         # add xy coord to list of coords for avatar
        #         avatar_xy_dict[avatar_loc] = avatar_xy_dict.get(avatar_loc, []) + [xy]
        #
        # else:  # > 10 avatars in band
        #     for avatar in range(col_max_avatars):
        #         xy = (band - 2.5, init_vert_offset + avatar*vert_offset)  # TODO: replace ints with default offsets
        #         avatar_loc = band_avatar_dict[band][avatar]
        #         avatar_xy_dict[avatar_loc] = avatar_xy_dict.get(avatar_loc, []) + [xy]
        #
        #     for avatar in range(len(band_avatar_dict[band] - 10)):
        #         avatar_loc = band_avatar_dict[band][avatar + 10]
        #         xy = (band + 2.5, init_vert_offset + avatar * vert_offset)
        #         avatar_xy_dict[avatar_loc] = avatar_xy_dict.get(avatar_loc, []) + [xy]
    return avatar_xy_dict


if __name__ == '__main__':
    test_score_avatar_dict = {1: ['foo', 'spam', 'dead', 'parrot'],
                              5: ['halibut', 'patties'],
                              8: ['original', 'recipe', 'chicken'],
                              9: ['foo', 'spam', 'dead', 'parrot'],
                              11: ['halibut', 'patties'],
                              }

    test_assign_avatars_to_bands_results = {0: ['foo', 'spam', 'dead', 'parrot', 'halibut', 'patties'],
                                            10: ['original', 'recipe', 'chicken', 'foo', 'spam', 'dead',
                                                 'parrot', 'halibut', 'patties'],
                                            20: [],
                                            30: [],
                                            40: [],
                                            50: [],
                                            60: [],
                                            70: [],
                                            80: [],
                                            90: [],
                                            100: [],
                                            }

    test_assign_avatar_coords_results = {'foo': [(0.0, 5), (10.0, 35)],
                                         'spam': [(0.0, 15), (10.0, 45)],
                                         'dead': [(0.0, 25), (10.0, 55)],
                                         'parrot': [(0.0, 35), (10.0, 65)],
                                         'halibut': [(0.0, 45), (10.0, 75)],
                                         'patties': [(0.0, 55), (10.0, 85)],
                                         'original': [(10.0, 5)],
                                         'recipe': [(10.0, 15)],
                                         'chicken': [(10.0, 25)]}

    test_generate_avatar_coords_results = {'foo': [(0.0, 5), (10.0, 35)],
                                           'spam': [(0.0, 15), (10.0, 45)],
                                           'dead': [(0.0, 25), (10.0, 55)],
                                           'parrot': [(0.0, 35), (10.0, 65)],
                                           'halibut': [(0.0, 45), (10.0, 75)],
                                           'patties': [(0.0, 55), (10.0, 85)],
                                           'original': [(10.0, 5)],
                                           'recipe': [(10.0, 15)],
                                           'chicken': [(10.0, 25)],
                                           }

    assert assign_avatars_to_bands(test_score_avatar_dict) == test_assign_avatars_to_bands_results
    assert assign_avatar_coords(test_assign_avatars_to_bands_results) == test_assign_avatar_coords_results
    assert generate_avatar_coords(test_score_avatar_dict) == test_generate_avatar_coords_results

    assert assign_avatar_coords(test_assign_avatars_to_bands_results) == generate_avatar_coords(test_score_avatar_dict)
