"""
Main script, menu.
"""
import os
import sys

import definitions

from dionysus_app.class_registry_functions import cache_class_registry, check_registry_on_exit
from dionysus_app.initialise_app import app_init
from dionysus_app.UI_menus.main_menu import run_main_menu
from dionysus_app.settings_functions import load_chart_save_folder


def run_app():
    """
    Env/system checks. Data setup.
    Make sure cwd is directory of app_main script.
    Check for data folders, create if not present.

    :return: None
    """
    os.chdir(sys.path[0])  # Make sure cwd is directory os script.

    app_init()


    # load runtime variables
    definitions.REGISTRY = cache_class_registry()

    definitions.DEFAULT_CHART_SAVE_FOLDER = load_chart_save_folder()


    run_main_menu()  # startup checks successful, enter UI.

    check_registry_on_exit()  # Dump cached registry to disk if different class_registry.index.


if __name__ == "__main__":
    run_app()
