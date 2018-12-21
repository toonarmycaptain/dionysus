"""
File functions - functions for dealing with files and the filesystem.

"""

import json

from shutil import copyfile, move


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


def copy_file(origin_fullpath: str, destination_fullpath: str):
    """
    Takes two filepaths, copying the origin file to the destination path and filename.

    Converts non-string object to string in case of Path object argument.



    :param origin_fullpath: str or Path
    :param destination_fullpath: str or Path
    :return: None
    """
    origin_fullpath = str(origin_fullpath)
    destination_fullpath = str(destination_fullpath)

    copyfile(origin_fullpath, destination_fullpath)


def move_file(origin_fullpath: str, destination_fullpath: str):
    """
    Takes two filepaths, copying the origin file/directory to the destination
    path and filename.

    Converts non-string object to string in case of Path object argument.



    :param origin_fullpath: str or Path
    :param destination_fullpath: str or Path
    :return: None
    """
    origin_fullpath = str(origin_fullpath)
    destination_fullpath = str(destination_fullpath)

    move(origin_fullpath, destination_fullpath)

# use Path.rename(new_name) to rename a class.
