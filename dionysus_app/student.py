"""Class for student."""

from pathlib import Path
from typing import Union

from dionysus_app.UI_menus.UI_functions import clean_for_filename


class Student:
    """
    Class for student objects.
    ...

    Attributes
    ----------
    :attr name: str Student's name
    :attr path_safe_name: str
    :attr avatar: Path or None - Path to student's avatar.

    Methods
    -------

    """

    def __init__(self, name: str, avatar_path: Union[Path, str] = None):

        self.name = name
        self.path_safe_name = name

        self.avatar_path = avatar_path
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
        Set student name. Also sets path_safe_name.

        :param name: str
        :return: None
        """
        self._name = name
        self.path_safe_name = self._name

    @property
    def path_safe_name(self):
        """
        Get path_safe_name: filename-safe student name string.

        :return: str
        """
        return self._path_safe_name

    @path_safe_name.setter
    def path_safe_name(self, student_name: str):
        """
        Set path_safe_name: filename-safe student name string.

        :param student_name: str
        :return: None
        """
        self._path_safe_name = clean_for_filename(student_name)

    @property
    def avatar_path(self):
        """
        Get avatar path.

        :return: Path or None
        """
        return self._avatar

    @avatar_path.setter
    def avatar_path(self, avatar_path: Union[Path, str] = None):
        """
        Set _avatar_path. Ensure saved value is Path object, otherwise None.

        :param avatar_path: Path, str, or None.
        :return: None
        """
        self._avatar: Union[Path, None]
        if avatar_path:

            self._avatar = Path(avatar_path)
        else:
            self._avatar = None
