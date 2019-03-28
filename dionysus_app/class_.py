"""Class for class data."""
from typing import List

from dionysus_app.student import Student
from dionysus_app.UI_menus.UI_functions import clean_for_filename


# pre-commit note to self: uses
#   - instantiate class without students and add students one by one
#   - instantiate from JSON dict

class Class:  # class name, classlist as dict
    """
    Class to contain a class' data (ie student objects) and related methods.
    ...

    Attributes
    ----------
    name : str
        Class' name

    path_safe_name : str
        Cleaned string safe to use in file names and paths.


    Methods
    -------

    """
    def __init__(self, name: str, students: List[Student] = None):
        self.name = name
        self.path_safe_name = name

        if students:
            self.students = students
        else:
            self.students = []
        # func return number of students in classh
        # return list of student names
        # return list of student avatar paths
        # method for adding or removing students

    @property
    def name(self):
        """
        Get class name.

        :return: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Set class name. Also sets path_safe_name.

        :param name: str
        :return: None
        """
        self._name = name
        self.path_safe_name = self._name

    @property
    def path_safe_name(self):
        """
        Get path_safe_name: filename-safe class name string.

        :return: str
        """
        return self._path_safe_name

    @path_safe_name.setter
    def path_safe_name(self, class_name: str):
        """
        Set path_safe_name: filename-safe class name string.

        :param class_name: str
        :return: None
        """
        self._path_safe_name = clean_for_filename(class_name)

    def add_student(self, student, avatar):
        "adds a student to the class"
