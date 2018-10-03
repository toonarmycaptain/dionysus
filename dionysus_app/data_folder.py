import os
from enum import Enum
from pathlib import Path
from definitions import ROOT_DIR


class DataFolder(Enum):
    APP_DATA = './dionysus_app/app_data'
    CLASS_DATA = './dionysus_app/app_data/class_data'
    IMAGE_DATA = './dionysus_app/app_data/image_data'

    @staticmethod
    def generate_rel_path(path):
        if not path:
            return os.getcwd()

        path = path.split('/')
        path.insert(0, ROOT_DIR)
        return Path(*path).resolve()
