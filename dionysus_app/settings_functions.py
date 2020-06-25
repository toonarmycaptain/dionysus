"""
Settings functions


Settings dict keys:
    'user_default_chart_save_folder': string path to where charts are saved.

"""
from pathlib import Path
from typing import Union

import definitions

from dionysus_app.data_folder import DataFolder
from dionysus_app.file_functions import move_file
from dionysus_app.UI_menus.settings_functions_UI import (user_decides_to_set_database_backend,
                                                         user_decides_to_set_default_location,
                                                         user_set_chart_save_folder,
                                                         user_set_database_backend,
                                                         )

APP_DATA = DataFolder.generate_rel_path(DataFolder.APP_DATA.value)
TEMP_DIR = DataFolder.generate_rel_path(DataFolder.TEMP_DIR.value)
APP_DEFAULT_CHART_SAVE_DIR = DataFolder.generate_rel_path(DataFolder.APP_DEFAULT_CHART_SAVE_DIR.value)
APP_SETTINGS_FILE = DataFolder.generate_rel_path(DataFolder.APP_SETTINGS.value)

CHART_SAVE_DIR_NAME = 'dionysus_charts'


def app_start_set_default_chart_save_location() -> None:
    """
    Print welcome, prompt user to set a default chart save location.

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


def set_default_chart_save_location(user_set: bool) -> None:
    """
    Set default_chart_save_location, based on user input, or default.

    Set and save default_chart_save_location, taking user input, or defaulting
    to original location. Creates chart save folder.

    :param user_set: Path or str
    :return: None
    """
    # Initialise default location.
    new_default_save_location = APP_DEFAULT_CHART_SAVE_DIR
    original_location = definitions.DEFAULT_CHART_SAVE_DIR

    if user_set:
        new_default_save_location = user_set_chart_save_folder()

    new_chart_save_folder_path = Path(new_default_save_location, CHART_SAVE_DIR_NAME)

    # Initialise and save chart save location.
    definitions.DEFAULT_CHART_SAVE_DIR = new_chart_save_folder_path
    save_new_default_chart_save_location_setting(new_chart_save_folder_path)

    create_chart_save_folder(new_chart_save_folder_path, original_location)


def app_start_set_database() -> None:
    """
    Prints welcome statement asking user if they would like to set a
    default chart save location.
    Calls set_default_chart_save_location with user's choice, setting
    save location. Clears screen.

    :return: None
    """
    if user_decides_to_set_database_backend():
        set_database_backend(user_set=True)
    else:
        set_database_backend(user_set=False)


def set_database_backend(user_set: bool) -> None:
    """
    Set database backend, taking user input, or default.

    :param user_set: Path or str
    :return: None
    """
    database_backend: Union[str, bool] = definitions.DEFAULT_DATABASE_BACKEND
    # Database choice selection
    if user_set:
        user_chosen_database = user_set_database_backend()
        if user_chosen_database:
            database_backend = user_chosen_database

    edit_app_settings_file({'database': database_backend})


def create_chart_save_folder(new_path: Path,
                             original_location: Path = None,
                             ) -> None:
    """
    Create a new chart_save_folder, move files from old location.

    :param new_path: Path
    :param original_location: Path , default: None
    :return: None
    """
    # Create new chart save location.
    new_path = Path(new_path)
    if original_location:  # Move older folder to new location.
        move_chart_save_folder(original_location, new_path)
    # Ensure directory creation if no orig location, or in event move fails.
    new_path.mkdir(parents=True, exist_ok=True)


def move_chart_save_folder(original_location: Path,
                           new_location: Path) -> None:
    """
    Move existent chart save folder to new location.

    Tests if the supplied path to the original chart save folder exists,
    moving to the supplied new location if it does. Otherwise does
    nothing.

    :param original_location: Path
    :param new_location: Path
    :return: None
    """
    original_location_path = Path(original_location)
    if original_location_path.exists():
        move_file(original_location, new_location)


def save_new_default_chart_save_location_setting(new_location: Union[Path, str]) -> None:
    """
    Save new default chart save location to settings.

    :param new_location: Path or str
    :return: None
    """
    new_setting = {'user_default_chart_save_folder': str(new_location)}
    edit_app_settings_file(new_setting)


def write_settings_to_file(settings_dict: dict) -> None:
    """
    Writes settings dict to file, overwriting any previous settings file.

    :param settings_dict: dict
    :return: None
    """
    with open(APP_SETTINGS_FILE, 'w+') as app_settings_file:
        write_string = 'dionysus_settings = ' + str(settings_dict)
        app_settings_file.write(write_string)


def create_app_settings_file(settings_dict: dict = None) -> None:
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


def create_app_data__init__() -> None:
    """
    Create __init__.py in app_data so that settings.py may be imported.

    :return: None
    """
    init_py_path = Path(APP_DATA, '__init__.py')

    with open(init_py_path, 'w+') as init_py:
        init_py.write('"""__init__.py so that settings.py may be imported."""')


def edit_app_settings_file(new_settings: dict) -> None:
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


def load_chart_save_folder() -> Path:
    """
    Return location for chart save folder.
    Import in function as module level import would error functions run before/
    if settings file doesn't exist.

    :return: Path
    """
    from dionysus_app.app_data.settings import dionysus_settings
    return Path(dionysus_settings['user_default_chart_save_folder'])
