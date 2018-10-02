"""
Main script, menu.
"""
import os
# import pathlib
import sys

from dionysus_app.main_menu import run_main_menu


def data_folder_check():
    """
    Check data folders exist, create them if they do not.

    :return: None
    """

    data_folders = {
        'relpath_app_data': r'./dionysus_app/app_data',  # TODO: check these paths work on Windows
        'relpath_class_data': r'./dionysus_app/app_data/class_data',  # data for classes
        'relpath_image_data': r'./dionysus_app/app_data/image_data',  # created images
    }
    for key in data_folders:
        if not os.path.exists(data_folders[key]):
            os.makedirs(data_folders[key])


# TODO: if the file structure already exists, check for previously created classes
    # Check for a class_registry.index in app_data directory
        # If list exists, compare with folders (? or .cld files ?) within class_data.
            # Use pathlib.iterdir() - https://docs.python.org/3.4/library/pathlib.html#basic-use
            #                       - https://stackoverflow.com/a/44228436/7942600
            
        # Else check for classes, create class_registry.


def run_app():
    """
    Env/system checks. Data setup.
    Make sure cwd is directory of app_main script.
    Check for data folders, create if not present.

    :return: None
    """
    os.chdir(sys.path[0])  # Make sure cwd is directory os script.

    data_folder_check()

    run_main_menu() # startup checks sucessful, enter UI.


if __name__ == "__main__":
    run_app()
