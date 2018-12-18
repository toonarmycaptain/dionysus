import os

from dionysus_app.data_folder import DataFolder
from dionysus_app.settings_functions import APP_SETTINGS_FILE, app_start_set_default_chart_save_location


def app_config():
    """
    Initialise app settings if no settings file (ie on first run).

    Set user default chart save folder.
    """

    if not os.path.exists(APP_SETTINGS_FILE):
        app_start_set_default_chart_save_location()


def data_folder_check():
    """
    Check data folders exist, create them if they do not.

    :return: None
    """

    data_folders = {
        DataFolder.APP_DATA: DataFolder.generate_rel_path(DataFolder.APP_DATA.value),
        DataFolder.CLASS_DATA: DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value),
        }

    for key in data_folders:
        data_folders[key].mkdir(parents=True, exist_ok=True)


def app_init():
    data_folder_check()  # data paths need to exist before creating/editing settings file.
    app_config()


if __name__ == '__main__':
    pass
