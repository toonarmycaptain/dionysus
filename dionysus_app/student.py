"""Class for student."""

from typing import Union, Any


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


    avatar_filename : sre or None
        Filename of student's avatar.
    """

    def __init__(self, name: str, **kwargs: Any):
        """
        Create an instance of Student.

        Can be instantiated with name only.

        :param name: The student's name.
        :type name: str

        :keyword avatar_filename: Filename of student's avatar.
        :type avatar_filename: str
        """
        self.name = name

        self.avatar_filename = kwargs.get('avatar_filename')  # Equivalent to kwargs.get('avatar_filename', None)
        # NB Assuring existence is responsibility of code instantiating/adding avatar_filename.

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
        # Python 3.8:
        # if not isinstance(self._name := name, str):
        #     raise TypeError(f"Student name must be a str, "
        #                     f"got {type(name)} instead.")
        if not isinstance(name, str): raise TypeError(f"Student name must be a str, got {type(name)} instead.")
        # Raise inline with isinstance to show code causing error.
        # else:
        self._name = name

    @property
    def avatar_filename(self):
        """
        Get avatar path.

        :return: str or None
        """
        return self._avatar_filename

    @avatar_filename.setter
    def avatar_filename(self, avatar_filename: str = None):
        """
        Set _avatar_filename, defaults to None.

        :param avatar_filename: str or None.
        :return: None
        """
        self._avatar_filename: Union[str, None]
        if avatar_filename:

            self._avatar_filename = avatar_filename
        else:
            self._avatar_filename = None

    def json_dict(self):
        """
        Translates Student object into JSON-serialisable dict.

        Captures name, avatar_filename attributes.

        :return: dict
        """
        json_data = {'name': self._name}
        if self._avatar_filename:
            json_data['avatar_filename'] = str(self._avatar_filename)
        return json_data

    # Alternate constructors

    @classmethod
    def from_dict(cls, student_dict: dict):
        """
        Instantiate a Student object from a JSON-serialisable dict.

        Dict must have keys corresponding to arguments to Student.__init__:
            'name' : str
            'avatar_filename' : str/None (optional, defaults to None).

        :param student_dict: dict
        :return: Student object
        """
        _name = student_dict['name']
        _avatar_filename = student_dict.get('avatar_filename', None)
        return Student(name=_name,
                       avatar_filename=_avatar_filename,
                       )

    # String representations
    def __repr__(self):
        repr_str = (f'{self.__class__.__module__}.{self.__class__.__name__}('
                    f'name={self._name!r}, '
                    f'avatar_filename={self._avatar_filename!r}'
                    f')'
                    )
        return repr_str

    def __str__(self):
        avatar_stmt = f'avatar {self.avatar_filename}' if self.avatar_filename is not None else 'no avatar'
        return f'Student {self.name}, with {avatar_stmt}.'
