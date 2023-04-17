"""Class for database object."""
import abc

from pathlib import Path
from typing import (Any,
                    NamedTuple,
                    )

import matplotlib.pyplot as plt

from dionysus_app.class_ import Class, NewClass


class ClassIdentifier(NamedTuple):
    """
    Class identifier. Takes two args, id, name.

    Provides nice namespace for working with classes where the name of
    the class is needed for UI, without passing all the details of every
    class.

    The id can be whatever identifier the backend needs, int, string, a
    class.

    >>> from dionysus_app.persistence.database import ClassIdentifier
    >>> my_class = ClassIdentifier(1, 'first class')
    >>> my_class.id, my_class.name
    (1, 'first class')
    >>> JSON_db_class = ClassIdentifier('classname_both', 'classname_both')
    >>> JSON_db_class.id, JSON_db_class.name
    ('classname_both', 'classname_both')

    :param id: Any - database primary key/unique identifier.
    :param name: str - the name of the class
    """
    id: Any
    name: str


class ABCMetaEnforcedAttrs(abc.ABCMeta):
    """
    Metaclass enforcing attrs in subclasses.
    ...

    Subclass of abc.ABCMeta that enforces instance attribute existence.

    Desired attribute names must be registered in the
    required_attributes list in the base class' definition.

    Attribute names must be defined in the __init__ of the subclass,
    or a TypeError will be raised.
    """
    required_attributes: list[str] = []

    def __call__(cls, *args, **kwargs):
        """
        Return validated instance of subclass of base metaclass.

        Instantiates subclass of metaclass inheriting from this class,
        checking for attributes in list required_attributes defined in
        the base metaclass, raising error if they are not defined by the
        subclass, otherwise returning the instantiated subclass.

        :return: Subclass
        :raises: TypeError
        """
        obj = super(ABCMetaEnforcedAttrs, cls).__call__(*args, **kwargs)
        for attr_name in obj.required_attributes:
            if not hasattr(obj, attr_name):
                raise TypeError(f"Can't instantiate abstract class {type(obj)}"
                                f"without required attribute {attr_name}.")
        return obj


class Database(abc.ABC, metaclass=ABCMetaEnforcedAttrs):
    """
    Database object
    ...

    Interface between application and persistence.

    Defines methods/attrs that subclasses must implement.

    required_attributes is a list of attributes subclasses must
    implement.


    Attributes
    ----------
    required_attributes: list[str]
        List of attributes required to be implemented by subclasses.


    Methods
    _______
    get_classes():
        Return list of ClassIdentifiers for classes in the database.

    class_name_exists(class_name: str):
        Return bool if class name already exists in the database.

    create_class(new_class: NewClass):
        Take a Class object and create/write the class in the database.

    load_class(class_id: Any):
        Load a class from the database.

    update_class(Class_to_write: Class):
        Update existing class record.

    get_avatar_path(avatar_id: Any):
        Return path to avatar, or to a default if nonexistent.

    create_chart(chart_data_dict: dict):
        Take chart data and create/write to the database.

    save_chart_image(chart_data_dict: dict, mpl_plt: matplotlib.pyplot):
        Save chart image, return Path to location.

    close():
        Closeout database.

    """
    required_attributes = ['default_avatar_path',  # Path to default avatar.
                           ]

    @abc.abstractmethod
    def get_classes(self) -> list[ClassIdentifier]:
        """
        Return list of available classes in the database.

        Format as list of ClassIdentifiers.

        :return: list[ClassIdentifier] ie list[NamedTuple[Any, str]]
        """

    @abc.abstractmethod
    def class_name_exists(self, class_name: str) -> bool:
        """
        Return bool if class name already exists in the database.

        :param class_name: str
        :return: bool
        """

    @abc.abstractmethod
    def create_class(self, new_class: NewClass) -> None:
        """
        Take a Class object and create/write the class to the database.

        :param new_class: Class object
        :return: None
        """

    @abc.abstractmethod
    def load_class(self, class_id: Any) -> Class:
        """
        Load class object from database.

        class_id argument type will vary by database backend.

        :param class_id: Any
        :return: Class object
        """

    @abc.abstractmethod
    def update_class(self, class_to_write: Class) -> None:
        """
        Update existing class record.

        :param class_to_write: Class object.
        :return: None
        """

    def get_avatar_path(self, avatar_id: Any) -> Path:
        """
        Return path to avatar, or to a default if nonexistent.

        NB This might cache an avatar to disk, and return that path.

        :param avatar_id: Any
        :return: Path
        """
        raise NotImplementedError("Method not implemented on base class.")

    @abc.abstractmethod
    def create_chart(self, chart_data_dict: dict) -> None:
        """
        Take chart data and create/write to the database.

        NB Arg type will probably change to some sort of object.

        :param chart_data_dict: dict
        :return: None
        """

    @abc.abstractmethod
    def save_chart_image(self, chart_data_dict: dict, mpl_plt: plt) -> Path:
        """
        Save chart image, return Path to location.

        Save chart image to disk location, and to database,
        if supported.
        Location may be a temporary file (app_data/temp), but file must
        exist as it will be used to copy image to user's save location,
        even if the image data is saved in the database rather than a
        file.

        NB User copy stored elsewhere.

        :param chart_data_dict: dict
        :param mpl_plt: plt - matplotlib.pyplot object
        :return: Path
        """

    @abc.abstractmethod
    def close(self) -> None:
        """
        Close/finalise database for shutdown.

        Including closing open connections, open files, completing
        pending writes.

        # NB This method name/API likely to change.

        :return: None
        """
