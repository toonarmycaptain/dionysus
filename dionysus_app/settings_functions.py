"""
Settings functions


Settings dict keys:
    'user_default_chart_save_folder': string path to where charts are saved.

"""

import os

from pathlib import Path
from typing import Union

import definitions

from dionysus_app.data_folder import DataFolder
from dionysus_app.file_functions import move_file
from dionysus_app.UI_menus.settings_functions_UI import (user_decides_to_set_default_location,
                                                         user_set_chart_save_folder,
                                                         )

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


def set_default_chart_save_location(user_set: bool):
    """
    Set and save default_chart_save_location, taking user input, or defaulting
    to original location. Creates chart save folder.

    :param user_set: Path or str
    :return: None
    """
    # Initialise default location.
    new_default_save_location = APP_DEFAULT_CHART_SAVE_FOLDER
    original_location = definitions.DEFAULT_CHART_SAVE_FOLDER

    if user_set:
        new_default_save_location = user_set_chart_save_folder()

    new_chart_save_folder_path = Path(new_default_save_location, CHART_SAVE_FOLDER_NAME)

    # Initialise and save chart save location.
    definitions.DEFAULT_CHART_SAVE_FOLDER = new_chart_save_folder_path
    save_new_default_chart_save_location_setting(new_chart_save_folder_path)

    create_chart_save_folder(new_chart_save_folder_path, original_location)


def create_chart_save_folder(new_path: Union[Path, str],
                             original_location: Union[Path, str] = None):
    """
    Create a new chart_save_folder, moving files from old location, if
    it exists.

    :param new_path: Path or str
    :param original_location: Path or str, default: None
    :return: None
    """
    # Create new chart save location.
    new_path = Path(new_path)
    if original_location:  # Move older folder to new location.
        move_chart_save_folder(original_location, new_path)
    # Ensure directory creation if no orig location, or in event move fails.
    new_path.mkdir(parents=True, exist_ok=True)


def move_chart_save_folder(original_location: Union[Path, str], new_location: Union[Path, str]):
    """
    Tests if the supplied path to the original chart save folder exists, moving
    to the supplied new location if it does. Otherwise does nothing.

    :param original_location: Path or str
    :param new_location: Path or str
    :return: None
    """
    original_location_path = Path(original_location)
    if original_location_path.exists():
        move_file(original_location, new_location)


def save_new_default_chart_save_location_setting(new_location: Union[Path, str]):
    """
    Save new default chart save location to settings.

    :param new_location: Path or str
    :return: None
    """
    new_setting = {'user_default_chart_save_folder': str(new_location)}
    edit_app_settings_file(new_setting)


def write_settings_to_file(settings_dict: dict):
    """
    Writes settings dict to file, overwriting any previous settings file.

    :param settings_dict: dict
    :return: None
    """
    with open(APP_SETTINGS_FILE, 'w+') as app_settings_file:
        write_string = 'dionysus_settings = ' + str(settings_dict)
        app_settings_file.write(write_string)


def create_app_settings_file(settings_dict: dict=None):
    """
    Create settings file, ensuring __init__.py in containing folder.

    Future: could have a dict containing some default settings, to pass to
    write_settings_to_file (or to add to provided dict to supply unprovided
    settings) if no settings_dict argument is provided.

    :param settings_dict: dict, default: None
    :return: None
    """
    create_app_data__init__()

    if not settings_dict:
        settings_dict = {}  # If default settings are desired, pass them here.

    write_settings_to_file(settings_dict)


def create_app_data__init__():
    """
    Create __init__.py in app_data so that settings.py may be imported.

    :return: None
    """
    init_py_path = os.path.join(APP_DATA, '__init__.py')

    with open(init_py_path, 'w+') as init_py:
        init_py.write('"""__init__.py so that settings.py may be imported."""')


def edit_app_settings_file(new_settings: dict):
    """
    Writes settings to settings file.

    Checks if settings file exists, creates if it does not.
    Imports settings (module level import might error if file nonexistent).
    Add/change settings in loaded settings, writes modified
    settings dict to file.


    :param new_settings: dict
    :return: None
    """
    if not Path.exists(APP_SETTINGS_FILE):
        create_app_settings_file()

    from dionysus_app.app_data.settings import dionysus_settings

    for setting in new_settings:
        dionysus_settings[setting] = new_settings[setting]

    write_settings_to_file(dionysus_settings)


def load_chart_save_folder():
    """
    Return location for chart save folder.
    Import in function as module level import would error functions run before/
    if settings file doesn't exist.

    :return: Path
    """
    from dionysus_app.app_data.settings import dionysus_settings
    return Path(dionysus_settings['user_default_chart_save_folder'])
