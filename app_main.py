"""
Main script, menu.
"""
import os
import sys

from dionysus_app.class_registry import cache_class_registry, check_registry_on_exit
from dionysus_app.data_folder import DataFolder
from dionysus_app.main_menu import run_main_menu


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


def run_app():
    """
    Env/system checks. Data setup.
    Make sure cwd is directory of app_main script.
    Check for data folders, create if not present.

    :return: None
    """
    os.chdir(sys.path[0])  # Make sure cwd is directory os script.

    data_folder_check()

    cache_class_registry()

    run_main_menu()  # startup checks successful, enter UI.

    check_registry_on_exit() # Dump cached registry to disk if different class_registry.index.


if __name__ == "__main__":
    run_app()
