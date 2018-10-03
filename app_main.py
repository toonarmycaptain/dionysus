"""
Main script, menu.
"""
import os
import sys

from dionysus_app.main_menu import run_main_menu
from dionysus_app.data_folder import DataFolder


def data_folder_check():
    """
    Check data folders exist, create them if they do not.

    :return: None
    """

    data_folders = {
        DataFolder.APP_DATA: DataFolder.generate_rel_path(DataFolder.APP_DATA.value),
        DataFolder.CLASS_DATA: DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value),
        DataFolder.IMAGE_DATA: DataFolder.generate_rel_path(DataFolder.IMAGE_DATA.value),
    }
    for key in data_folders:
        data_folders[key].mkdir(parents=True, exist_ok=True)


# TODO: if the file structure already exists, check for previously created classes
"""
     Check for a class_registry.index in app_data directory
         If list exists, compare with folders (? or .cld files ?) within class_data.
             Use pathlib.iterdir() - https://docs.python.org/3.4/library/pathlib.html#basic-use
                                   - https://stackoverflow.com/a/44228436/7942600
         Else check for classes, create class_registry.
"""


def run_app():
    """
    Env/system checks. Data setup.
    Make sure cwd is directory of app_main script.
    Check for data folders, create if not present.

    :return: None
    """
    os.chdir(sys.path[0])  # Make sure cwd is directory os script.

    data_folder_check()

    run_main_menu()  # startup checks successful, enter UI.


if __name__ == "__main__":
    run_app()
