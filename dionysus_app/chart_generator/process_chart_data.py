"""
Process input data for image generation code.
"""



DEFAULT_CHART_PARAMS = {'column_max_avatars': 10,  # max number of avatars vertically. Nominally pixels from x-axis to top of image//height of avatar.
                        'column_width': None,
                        'min_score' : 0,
                        'max_score' : 100,
                        # TODO: put avatar offets here
                        }

def generate_avatar_coords(score_avatar_dict, chart_params=None):  # set chart params to a default?
    """
    score_avatar_dict - dict of scores to lists of avatar image locations for each score.

    :param score_avatar_dict: dict
    :param chart_params: dict
    :return:
    """
    # take chart_data_dict['score-avatar_dict'] and translate into dict
    # with keys: avatar path, values: list of x, y tuples eg [(80, 80), (90, 90)]

    # chart_data_dict['chart_params'] - dict of any chart option settings etc.
    #
    if not chart_params:
        chart_param = DEFAULT_CHART_PARAMS  # pull values from DEFAULT_CHART_PARAMS dict

    # Re-sort in ascending score order.
    score_avatar_dict = {score: score_avatar_dict[score] for score in sorted(score_avatar_dict)}

    banded_avatars = assign_avatars_to_bands(score_avatar_dict)
  
    avatar_coord_dict = assign_avatar_coords(banded_avatars)

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


def assign_avatar_coords(band_avatar_dict):
    # iterate over avatars in lists from lowest to highest
    # if more than one column, place in left-most column first so highest scores are rightmost

    # if 2 columns, offest by 2.5 either side of band eg 87.5, 92.5 for 90

    # import itertools
    # y_image_coords = itertools.count(start=init_avatar_offset_from_axis, step=offset_per_avatar)
    # next(y_image_coords)  # yields 4, 11, 18, 25...each time it is called.

    avatar_xy_dict = {}

    for band in band_avatar_dict.keys():  # iterate over bands in band_avatar_dict
        if len(band_avatar_dict[band]) < 10:
            for avatar in range(len(band_avatar_dict[band])):
                xy = (band, 5 + avatar*10)
                avatar_loc = band_avatar_dict[band][avatar]
                # add xy coord to list of coords for avatar
                avatar_xy_dict[avatar_loc] = avatar_xy_dict.get(avatar_loc, []) + [xy]

        else:  # > 10 avatars in band
            for avatar in range(10):
                xy = (band - 2.5, 5 + avatar*10)  # TODO: replace ints with default offsets
                avatar_loc = band_avatar_dict[band][avatar]
                avatar_xy_dict[avatar_loc] = avatar_xy_dict.get(avatar_loc, []) + [xy]

            for avatar in range(len(band_avatar_dict[band] - 10)):
                avatar_loc = band_avatar_dict[band][avatar + 10]
                xy = (band + 2.5, 5 + avatar * 10)
                avatar_xy_dict[avatar_loc] = avatar_xy_dict.get(avatar_loc, []) + [xy]
    return avatar_xy_dict


if __name__ == '__main__':
    test_score_avatar_dict = {1: ['chicken', 'tenders'],
                              5: ['halibut', 'patties'],
                              11: ['original', 'recipe', 'chicken']}

    print(test_score_avatar_dict, generate_avatar_coords(test_score_avatar_dict))
