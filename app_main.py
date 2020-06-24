"""
Main script, menu.
"""
import os
import sys

import definitions

from dionysus_app.initialise_app import app_init, clear_temp
from dionysus_app.persistence.database_functions import load_database
from dionysus_app.settings_functions import load_chart_save_folder
from dionysus_app.UI_menus.main_menu import run_main_menu


def quit_app():
    """
    Quits application.

    Perform graceful termination tasks, eg clear temp/, close/finalise
    database (eg close connections, flush data).

    :return: None
    """
    definitions.DATABASE.close()
    clear_temp()  # Clear temp files.
    sys.exit()


def run_app():
    """
    Env/system checks. Data setup.
    Make sure cwd is directory of app_main script.
    Check for data folders, create if not present.

    :return: None
    """
    os.chdir(sys.path[0])  # Make sure cwd is directory of script.

    app_init()

    # Load runtime variables.
    definitions.DEFAULT_CHART_SAVE_DIR = load_chart_save_folder()

    definitions.DATABASE = load_database()

    run_main_menu()  # Startup checks successful, enter UI.

    quit_app()


if __name__ == "__main__":
    run_app()
