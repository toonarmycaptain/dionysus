"""Class for class data."""
import json

from pathlib import Path
from typing import Any, List, Union

from dionysus_app.file_functions import convert_to_json
from dionysus_app.student import Student
from dionysus_app.UI_menus.UI_functions import clean_for_filename


# pre-commit note to self: uses
#   - instantiate class without students and add students one by one
#   - instantiate from JSON dict

class Class:
    """
    Class to contain a class' data (ie student objects) and related methods.
    ...

    Attributes
    ----------
    name : str
        Class' name

    path_safe_name : str
        Cleaned string safe to use in file names and paths.

    students : list[Student]


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

        # func return number of students in class
        # return list of student names
        # return list of student avatar paths
        # method for adding or removing students
        # 'save' method as well as or instead of
        # implement default avatar at class level by initialising with None or path to app default avatar.
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

    def add_student(self, student: [Student] = None, **kwargs: Any):
        """
        Adds a student to the class.

        May be called with a student object as first argument, otherwise adds
        a Student object instantiated with supplied named parameters to list of
        students in class:

        Class.add_student(my_student_object)
        or
        Class.add_student(name='student_name', ...)

        NB If Student object is passed to student parameter, any kwargs are
        ignored, such that an avatar cannot be added to a student object while
        adding it to a class.

        :param student: Student object.
        :type student: Student

        :keyword name: str - Name of student, first arg to Student __init__.

        For other keyword arguments, see Student object documentation.

        :return: None
        """
        if student and isinstance(student, Student):
            self.students.append(student)
        else:
            if isinstance(kwargs['name'], str):
                self.students.append(Student(**kwargs))

    def json_dict(self):
        """
        Translates Class object into JSON-serialisable dict.

        Captures name, converts Student objects to JSON-serialisable dicts.

        :return: dict
        """
        class_dict = {'name': self._name,
                      'students': [student.json_dict() for student in self.students]}

        return class_dict

    def to_json_str(self):
        """
        Converts Class in JSON-serialisable form to JSON string.

        :return: str
        """
        json_class_data = convert_to_json(self.json_dict())
        return json_class_data

    @classmethod
    def from_dict(cls, class_dict: dict):
        """
        Instantiate Class object from JSON-serialisable dict.

        :param class_dict: dict
        :return: Class object
        """
        _name = class_dict['name']
        _students = [Student.from_dict(student) for student in class_dict['students']]
        return Class(_name, _students)

    @classmethod
    def from_json(cls, json_data: str):
        """
        Return Class object from json string.

        :param json_data: str
        :return: Class object
        """
        class_dict = json.load(json_data)
        return Class.from_dict(class_dict)

    @classmethod
    def from_file(cls, cdf_path: Union[Path, str]):
        """
        Return Class object from cdf file.

        :param cdf_path: Path or str
        :return: Class object
        """
        with open(Path(cdf_path)) as class_data_file:
            class_json = json.load(class_data_file)
        return Class.from_json(class_json)
