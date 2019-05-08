"""
File functions - functions for dealing with files and the filesystem.

"""

import json

from pathlib import Path
from shutil import copyfile, move
from typing import Union


def convert_to_json(data_to_convert):
    """
    Serialise data in JSON format, return as JSON string.

    CAUTION: If dict has int keys when converted to JSON, these will be
    converted to str keys, and remain so on json.loads, as JSON does not have
    int keys.

    :param data_to_convert:
    :return: str
    """
    converted_data = json.dumps(data_to_convert, indent=4)
    return converted_data


def load_from_json(data_to_convert: str):
    """
    Convert data from JSON to python object.

    CAUTION: If dict had int keys when converted to JSON, these will be str keys
    when loaded from JSON due to JSON not having int keys.

    :param data_to_convert: str
    :return:
    """
    converted_data = json.loads(data_to_convert)
    return converted_data


def load_from_json_file(json_file_path: Union[Path, str]):
    """
    Take a filepath and load json from that file.

    :param json_file_path: Path (or str)
    :return: dict
    """
    with open(json_file_path) as json_file:
        json_data = json_file.read()
        loaded_data = load_from_json(json_data)
        return loaded_data


def copy_file(origin_fullpath: Union[Path, str], destination_fullpath: Union[Path, str]):
    """
    Takes two filepaths, copying the origin file to the destination path and
    filename, doing nothing if the origin filepath doesn't exist.

    Converts non-string object to string in case of Path object argument.

    :param origin_fullpath: Path or str
    :param destination_fullpath: Path or str
    :return: None
    """
    origin_fullpath = Path(origin_fullpath)
    if origin_fullpath.exists():
        origin_fullpath = str(origin_fullpath)
        destination_fullpath = str(destination_fullpath)

        copyfile(origin_fullpath, destination_fullpath)


def move_file(origin_fullpath: Union[Path, str], destination_fullpath: Union[Path, str]):
    """
    Takes two filepaths, copying the origin file/directory to the destination
    path and filename, doing nothing if the origin filepath doesn't exist.

    Converts non-string object to string in case of Path object argument.

    :param origin_fullpath: Path or str
    :param destination_fullpath: Path or str
    :return: None
    """
    origin_fullpath = Path(origin_fullpath)
    if origin_fullpath.exists():
        origin_fullpath = str(origin_fullpath)
        destination_fullpath = str(destination_fullpath)

        move(origin_fullpath, destination_fullpath)

# use Path.rename(new_name) to rename a class.
