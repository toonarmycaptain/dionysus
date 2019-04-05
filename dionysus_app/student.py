"""Class for student."""

from pathlib import Path
from typing import Union, Any

from dionysus_app.UI_menus.UI_functions import clean_for_filename


class Student:
    """
    Class for student objects.
    ...

    Attributes
    ----------
    name : str
        Student's name

    path_safe_name : str
        Cleaned string safe to use in file names and paths.

    avatar_path : Path or None
        Path to student's avatar.


    Methods
    -------
    json_dict()
        Returns a JSON serialisable dictionary of student's data.

    from_json_dict(json_data)
        Returns a Student object instantiated from provided dict.
    """

    def __init__(self, name: str, **kwargs: Any):
        """
        Create an instance of Student.

        Can be instantiated with name only.

        :param name: The student's name.
        :type name: str

        :keyword avatar_path: Path to the student's avatar.
        :type avatar_path: Path or str
        """
        self.name = name

        self.avatar_path = kwargs.get('avatar_path')  # Equivalent to kwargs.get('avatar_path', None)
        # NB Assuring existence is responsibility of code instantiating/adding avatar_path.

    @property
    def name(self):
        """
        Get student name.

        :return: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Set student name.

        :param name: The student's name.
        :type name: str # TODO: change other docstrings in class to this format.

        :return: None
        """
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError(f"Student name must be a str, "
                            f"got {type(name)} instead.")

    @property
    def avatar_path(self):
        """
        Get avatar path.

        :return: Path or None
        """
        return self._avatar_path

    @avatar_path.setter
    def avatar_path(self, avatar_path: Union[Path, str] = None):
        """
        Set _avatar_path. Ensure saved value is Path object, otherwise None.

        :param avatar_path: Path, str, or None.
        :return: None
        """
        self._avatar_path: Union[Path, None]
        if avatar_path:

            self._avatar_path = Path(avatar_path)
        else:
            self._avatar_path = None

    def json_dict(self):
        """
        Translates Student object into JSON-serialisable dict.

        Captures name, avatar_path attributes.
        Path is converted to string.

        :return: dict
        """
        json_data = {'name': self._name}
        if self._avatar_path:
            json_data['avatar_path'] = str(self._avatar_path)
        return json_data

    @classmethod
    def from_dict(cls, student_dict):
        """
        Instantiate a Student object from a JSON-serialisable dict.

        Dict must have keys corresponding to arguments to Student.__init__:
        'name' : str
        'avatar_path' : Path/str/None (optional, defaults to None).

        :param student_dict: dict
        :return: Student object
        """
        _name = student_dict['name']
        _avatar_path = student_dict.get('avatar_path', None)
        return Student(name=_name, avatar_path=_avatar_path)
