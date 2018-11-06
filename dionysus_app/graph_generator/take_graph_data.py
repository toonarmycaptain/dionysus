"""
Script for taking and saving data for graph.
"""


# score entry:

import json

# from dionysus_app.data_folder import CHART_DATA_FILE_TYPE
# from dionysus_app.file_functions import convert_to_json

def take_score_entry(minimum=0, maximum=100):
    """

    :param minimum: int minimum allowed score
    :param maximum: int maximum allowed score
    :return: float
    """
    while True:
        score = input("Enter student score: ")

        if score == '_':
            return None  # do not include student in graph eg if absent

        try:
            score_float = float(score)
        except ValueError:
            print("InputError: please enter a number or '_' to exclude student.")
            continue
        # else:
        if score_float < minimum or score_float > maximum:
            print(f'InputError: Please enter a number between {minimum} and {maximum}.')
            continue
        return score_float




if __name__ == '__main__':
    take_score_entry()  # Do not alter this as it is used in testing.
