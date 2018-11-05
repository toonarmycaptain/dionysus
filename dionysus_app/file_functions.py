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
