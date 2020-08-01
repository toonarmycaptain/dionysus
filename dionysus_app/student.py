"""Class for student."""

from pathlib import Path
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

    student_id : Any
        Student's id in database.

    avatar_id : Any
        id or filename of student's avatar.

    class_id : Any
        Class' id in database.


    Methods
    _______
    json_dict():
        Translates Student object into JSON-serialisable dict.

    Class Methods
    _____________
    from_dict(student_dict: dict):
        Instantiate a Student object from a JSON-serialisable dict.

    """

    def __init__(self, name: str, **kwargs: Any):
        """
        Create an instance of Student.

        Can be instantiated with name only.

        :param name: The student's name.
        :type name: str

        :keyword avatar_id: Filename of student's avatar.
        :keyword student_id: Any - unique id of student in database.
        :keyword class_id: Any - unique id of student's class in database.
        :type avatar_id: str
        """
        self.name: str = name

        self.avatar_id: Any = kwargs.get('avatar_id')  # Equivalent to kwargs.get(key, None)
        # NB Assuring existence is responsibility of code instantiating/adding avatar_id.
        self.id: Any = kwargs.get('student_id')  # student id in database.
        self.class_id: Any = kwargs.get('class_id')  # class id in database

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
        :type name: str

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
    def avatar_id(self):
        """
        Get avatar path.

        :return: str or None
        """
        return self._avatar_id

    @avatar_id.setter
    def avatar_id(self, avatar_id: Any = None):
        """
        Set _avatar_id, defaults to None.

        :param avatar_id: Any or None.
        :return: None
        """
        self._avatar_id: Union[Any, None]
        self._avatar_id = avatar_id if avatar_id else None

    def json_dict(self):
        """
        Translates Student object into JSON-serialisable dict.

        Captures name, avatar_id attributes. Omits id if not present.

        :return: dict
        """
        json_data = {'name': self._name
                     }
        if self.id:
            json_data['id'] = self.id
        if self._avatar_id:
            json_data['avatar_id'] = self.avatar_id
        return json_data

    # Alternate constructors

    @classmethod
    def from_dict(cls, student_dict: dict) -> 'Student':
        """
        Instantiate a Student object from a JSON-serialisable dict.

        Dict must have keys corresponding to args to Student.__init__:
            'name' : str
            'avatar_id' : str/None (optional, defaults to None).

        :param student_dict: dict
        :return: Student object
        """
        _id = student_dict.get('id')  # Student may not have id if not in db.
        _name = student_dict['name']
        _avatar_id = student_dict.get('avatar_id', None)
        return cls(class_id=_id,
                   name=_name,
                   avatar_id=_avatar_id,
                   )

    # String representations
    def __repr__(self) -> str:
        repr_str = (f'{self.__class__.__module__}.{self.__class__.__name__}('
                    f'id={self.id!r}, '
                    f'name={self._name!r}, '
                    f'avatar_id={self._avatar_id!r}'
                    f')'
                    )
        return repr_str

    def __str__(self) -> str:
        avatar_stmt = (f'avatar {self.avatar_id}' if self.avatar_id is not None
                       else 'no avatar')
        return f'Student {self.name}, with {avatar_stmt}, and id={self.id}.'
