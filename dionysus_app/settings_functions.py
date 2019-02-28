"""
Settings functions


Settings dict keys:
    'user_default_chart_save_folder': string path to where charts are saved.

"""

import os
from pathlib import Path

import definitions

from dionysus_app.UI_menus.settings_functions_UI import (user_decides_to_set_default_location,
                                                         user_set_chart_save_folder,
                                                         )
from dionysus_app.data_folder import DataFolder
from dionysus_app.file_functions import move_file

APP_DATA = DataFolder.generate_rel_path(DataFolder.APP_DATA.value)
APP_DEFAULT_CHART_SAVE_FOLDER = DataFolder.generate_rel_path(DataFolder.APP_DEFAULT_CHART_SAVE_FOLDER.value)
APP_SETTINGS_FILE = DataFolder.generate_rel_path(DataFolder.APP_SETTINGS.value)

CHART_SAVE_FOLDER_NAME = 'dionysus_charts'


def app_start_set_default_chart_save_location():
    """
    Prints welcome statement asking user if they would like to set a
    default chart save location.
    Calls set_default_chart_save_location with user's choice, setting
    save location. Clears screen.

    :return: None
    """
    if user_decides_to_set_default_location():
        set_default_chart_save_location(user_set=True)
    else:
        set_default_chart_save_location(user_set=False)


def set_default_chart_save_location(user_set):
    # Initialise default location.
    new_default_save_location = APP_DEFAULT_CHART_SAVE_FOLDER
    original_location = definitions.DEFAULT_CHART_SAVE_FOLDER

    if user_set:
        new_default_save_location = user_set_chart_save_folder()

    new_chart_save_folder_path = Path(new_default_save_location, CHART_SAVE_FOLDER_NAME)

    # Initialise and save chart save location.
    definitions.DEFAULT_CHART_SAVE_FOLDER = str(new_chart_save_folder_path)
    save_new_default_chart_save_location_setting(new_chart_save_folder_path)

    create_chart_save_folder(new_chart_save_folder_path, original_location)


def create_chart_save_folder(new_path, original_location=None):
    """
    Create a new chart_save_folder, moving files from old location, if
    it exists.

    :param new_path: str or Path
    :param original_location: None, str or Path
    :return: None
    """
    # Create new chart save location.
    # Path(new_path).mkdir(parents=True, exist_ok=True)
    # Move older folder to new location.
    if original_location:
        move_file(original_location, new_path)


def save_new_default_chart_save_location_setting(new_location):
    """
    Save new default chart save location to settings.

    :param new_location: str or Path
    :return:
    """
    new_setting = {'user_default_chart_save_folder': str(new_location)}
    edit_app_settings_file(new_setting)


def write_settings_to_file(settings_dict: dict):
    with open(APP_SETTINGS_FILE, 'w+') as app_settings_file:
        write_string = 'dionysus_settings = ' + str(settings_dict)
        app_settings_file.write(write_string)


def create_app_settings_file(settings_dict=None):
    # create __init__.py in app_data so that settings.py may be imported.
    init_py_path = os.path.join(APP_DATA, '__init__.py')

    with open(init_py_path, 'w+') as init_py:
        init_py.write('"""__init__.py so that settings.py may be imported."""')

    if not settings_dict:
        settings_dict = 'dionysus_settings = {}'

    write_settings_to_file(settings_dict)


def edit_app_settings_file(new_settings: dict):
    if not Path.exists(APP_SETTINGS_FILE):
        create_app_settings_file()

    from dionysus_app.app_data.settings import dionysus_settings

    for setting in new_settings:
        dionysus_settings[setting] = new_settings[setting]

    write_settings_to_file(dionysus_settings)


def load_chart_save_folder():
    from dionysus_app.app_data.settings import dionysus_settings
    return dionysus_settings['user_default_chart_save_folder']


if __name__ == '__main__':
    app_start_set_default_chart_save_location()
