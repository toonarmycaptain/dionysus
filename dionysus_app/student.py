"""Class for student."""

from dionysus_app.UI_menus.UI_functions import clean_for_filename


class Student:
    def __init__(self, name: str):
        self.name = name
        self.path_safe_name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.path_safe_name = self._name

    @property
    def path_safe_name(self):
        return self._path_safe_name

    @path_safe_name.setter
    def path_safe_name(self, path_safe_name):
        self._path_safe_name = clean_for_filename(path_safe_name)
