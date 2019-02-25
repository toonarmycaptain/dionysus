"""
Settings functions


Settings dict keys:
    'user_default_chart_save_folder': string path to where charts are saved.

"""

import os

from pathlib import Path

import definitions


from dionysus_app.data_folder import DataFolder
from dionysus_app.file_functions import move_file
from dionysus_app.UI_menus.settings_functions_UI import user_decides_to_set_default_location
from dionysus_app.UI_menus.UI_functions import clear_screen, select_folder_dialogue

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

    # initialise default location
    new_default_save_location = APP_DEFAULT_CHART_SAVE_FOLDER
    original_location = definitions.DEFAULT_CHART_SAVE_FOLDER
    new_setting = {}

    if user_set:
        new_default_save_location = user_set_chart_save_folder()

    # Ensure saved value has correct separators.
    chart_save_parent_folder_path = Path(new_default_save_location)
    new_chart_save_folder_str = str(Path.joinpath(chart_save_parent_folder_path, CHART_SAVE_FOLDER_NAME))

    # Initialise and save chart save location.
    definitions.DEFAULT_CHART_SAVE_FOLDER = new_chart_save_folder_str

    new_setting['user_default_chart_save_folder'] = new_chart_save_folder_str
    create_app_settings_file()
    edit_app_settings_file(new_setting)

    if original_location:
        move_file(original_location, new_chart_save_folder_str)

    print(f'Default chart save folder set to {definitions.DEFAULT_CHART_SAVE_FOLDER}')

    # Create chart save location
    Path(new_setting['user_default_chart_save_folder']).mkdir(parents=True, exist_ok=True)


def user_set_chart_save_folder():
    dialogue_message = 'Please_select location for chart save folder, or press cancel to use default.'
    new_default_save_location = select_folder_dialogue(title_str=dialogue_message, start_dir='..')

    if not new_default_save_location:  # User presses cancel, doesn't select a folder.
        return APP_DEFAULT_CHART_SAVE_FOLDER
    # else:
    return new_default_save_location


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

    from dionysus_app.app_data.settings import dionysus_settings

    for setting in new_settings:
        dionysus_settings[setting] = new_settings[setting]

    write_settings_to_file(dionysus_settings)


def load_chart_save_folder():
    from dionysus_app.app_data.settings import dionysus_settings
    return dionysus_settings['user_default_chart_save_folder']


if __name__ == '__main__':
    app_start_set_default_chart_save_location()
