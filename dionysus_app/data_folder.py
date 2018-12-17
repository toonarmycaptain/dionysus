from enum import Enum
from pathlib import Path

from definitions import ROOT_DIR


CLASSLIST_DATA_FILE_TYPE = '.cld'
CHART_DATA_FILE_TYPE = '.cdf'


class DataFolder(Enum):
    APP_DATA = './dionysus_app/app_data/'

    CLASS_DATA = APP_DATA + 'class_data/'
    IMAGE_DATA = APP_DATA + 'image_data/'

    CLASS_REGISTRY = APP_DATA + 'class_registry.index'

    APP_SETTINGS = APP_DATA + 'settings.py'
    APP_DEFAULT_CHART_SAVE_FOLDER = '..'

    CHART_GENERATOR = 'chart_generator/'
    DEFAULT_AVATAR = CHART_GENERATOR + 'default_avatar.png'

    @staticmethod
    def generate_rel_path(path):
        if not path:
            return Path.cwd().as_uri()

        path = path.split('/')
        path.insert(0, ROOT_DIR)
        return Path(*path).resolve()
