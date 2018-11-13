"""
File functions - functions for dealing with files and the filesystem.

"""

import json


def convert_to_json(data_to_convert):
    """
    Serialise data in JSON format, return as JSON string.

    :param data_to_convert:
    :return: str
    """
    converted_data = json.dumps(data_to_convert, indent=4)
    return converted_data


def load_from_json(data_to_convert: str):
    """
    Convert data from JSON to python object.

    :param data_to_convert: str
    :return:
    """
    converted_data = json.loads(data_to_convert)
    return converted_data


# use Path.rename(new_name) to rename a class.
