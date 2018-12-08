# import signal
# from unittest import TestCase
#
# from dionysus_app.chart_generator.take_graph_data import take_score_entry
# import pexpect.run


def test_take_score_entry():
    """
    Test for regular parameters (ie default 0-100 range)
    Need further tests using different range.

    :return:
    """

    test_dict = {
        '_': None,
        '0': 0.0,
        '1.25': 1.25,
        '5.7': 5.7,
        '7': 7.0,
        '99': 99.0,
        '100': 100.0,
        '101': "InputError: Please enter a number between 0 and 100.",
        'i am bad data': "InputError: please enter a number or '_' to exclude student.",
        }

    for i in test_dict:
        assert i == i
        # mock input
        # assert take_score_entry() == return_value_from_function
