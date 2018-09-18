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
    
    :return: 
    """

    data_folders = {
        'relpath_app_data': r'./dionysus_app/app_data',  # TODO: check these paths work on Windows
        'relpath_class_data': r'./dionysus_app/app_data/class_data',
        'relpath_image_data': r'./dionysus_app/app_data/image_data',
    }
    for key in data_folders:
        if not os.path.exists(data_folders[key]):
            os.makedirs(data_folders[key])


def run_app():
    """
    Env/system checks. Data setup.
    Make sure cwd is directory of app_main script.
    Check for data folders, create if not present.

    
    :return: 
    """
    os.chdir(sys.path[0])  # Make sure cwd is directory os script.

    data_folder_check()

    run_main_menu()


if __name__ == "__main__":
    run_app()
