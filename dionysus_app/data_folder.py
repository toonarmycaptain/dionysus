from enum import Enum
from pathlib import Path

from definitions import ROOT_DIR


CLASSLIST_DATA_FILE_TYPE = '.cld'
CHART_DATA_FILE_TYPE = '.cdf'


class DataFolder(Enum):
    APP_DATA = './dionysus_app/app_data/'

    CLASS_DATA = APP_DATA + 'class_data/'

    CLASS_REGISTRY = APP_DATA + 'class_registry.index'

    APP_SETTINGS = APP_DATA + 'settings.py'
    APP_DEFAULT_CHART_SAVE_FOLDER = '..'

    CHART_GENERATOR = 'chart_generator/'
    DEFAULT_AVATAR = CHART_GENERATOR + 'default_avatar.png'

    @staticmethod
    def generate_rel_path(path):
        """
        Returns a abs path from relative path.
        eg for APP_DATA use:
        APP_DATA_path = DataFolder.generate_rel_path(APP_DATA.value)

        If None is passed as an argument, returns the Path of the
        current working directory.

        If a path is given, the ROOT_DIR of the project is inserted
        before it.

        :param path: string or None.
        :return: Path object.
        """
        if not path:
            return Path.cwd().as_uri()

        path = path.split('/')
        path.insert(0, ROOT_DIR)
        return Path(*path).resolve()
