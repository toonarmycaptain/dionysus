import os
import shutil

from pathlib import Path

from dionysus_app.data_folder import DataFolder
from dionysus_app.settings_functions import (APP_SETTINGS_FILE,
                                             app_start_set_default_chart_save_location,
                                             TEMP_DIR)


def app_config() -> None:
    """
    Initialise app settings if no settings file (ie on first run).

    Set user default chart save folder.
    """

    if not Path.exists(APP_SETTINGS_FILE):
        app_start_set_default_chart_save_location()


def data_folder_check() -> None:
    """
    Check data folders exist, create them if they do not.

    :return: None
    """

    data_folders = {
        DataFolder.APP_DATA: DataFolder.generate_rel_path(DataFolder.APP_DATA.value),
        DataFolder.CLASS_DATA: DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value),
        DataFolder.TEMP_DIR: DataFolder.generate_rel_path(DataFolder.TEMP_DIR.value)
    }

    for key in data_folders:
        data_folders[key].mkdir(parents=True, exist_ok=True)


def clear_temp() -> None:
    """
    Removes temp folder if there are files in it.

    Should not throw an error if temp dir doesn't exist.

    This is a candidate to run using atexit module, see
    https://docs.python.org/3/library/atexit.html - but doing so without
    implementing logging to log any errors would remove any files in temp that
    might assist in debugging.

    :return: None
    """
    if TEMP_DIR.exists() and os.listdir(TEMP_DIR):
        # Log any files if logging is implemented.
        shutil.rmtree(TEMP_DIR)


def app_init() -> None:
    """
    Clear temp folder if it contains files.
    Ensures existence of key data folders.
    Run app_config.

    :return: None
    """
    clear_temp()
    data_folder_check()  # Data paths need to exist before creating/editing settings file.
    app_config()


if __name__ == '__main__':
    pass
