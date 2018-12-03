"""
Process input data for image generation code.
"""


chart_params = None  # dict of default params, information for how to set coords for default


def generate_avatar_coords(score_avatar_dict, custom_chart_params=None):  # set chart params to a default?
    """
    score_avatar_dict - dict of scores to lists of avatar image locations for each score.

    :param score_avatar_dict: dict
    :param custom_chart_params: dict
    :return:
    """
    # take chart_data_dict['score-avatar_dict'] and translate into dict
    # with keys: avatar path, values: list of x, y tuples eg [(80, 80), (90, 90)]

    # chart_data_dict['chart_params'] - dict of any chart option settings etc.
    #
    if custom_chart_params:
        chart_param = custom_chart_params  # or pull values from default chart_param dict

    pass
    # return avatar_coord_dict
