"""
Main script, menu.
"""
import os
from enum import Enum
import sys

from dionysus_app.main_menu import run_main_menu


class DataFolder(Enum):
    APP_DATA = './dionysus_app/app_data'
    CLASS_DATA = './dionysus_app/app_data/class_data'
    IMAGE_DATA = './dionysus_app/app_data/image_data'


def data_folder_check():
    """
    Check data folders exist, create them if they do not.

    :return: None
    """

    data_folders = {
        DataFolder.APP_DATA: generate_rel_path(DataFolder.APP_DATA.value),
        DataFolder.CLASS_DATA: generate_rel_path(DataFolder.CLASS_DATA.value),
        DataFolder.IMAGE_DATA: generate_rel_path(DataFolder.IMAGE_DATA.value),
    }
    for key in data_folders:
        if not os.path.exists(data_folders[key]):
            os.makedirs(data_folders[key])


def generate_rel_path(path):
    if not path:
        return os.getcwd()
    path = path.split('/')
    return os.path.abspath(os.path.join(os.getcwd(), *path))


def run_app():
    """
    Env/system checks. Data setup.
    Make sure cwd is directory of app_main script.
    Check for data folders, create if not present.

    :return: None
    """
    os.chdir(sys.path[0])  # Make sure cwd is directory os script.

    data_folder_check()

    run_main_menu()


if __name__ == "__main__":
    run_app()
