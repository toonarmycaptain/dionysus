"""Class for class data."""
import json
import shutil
import tempfile

from pathlib import Path
from typing import Any, Iterator, Union

from dionysus_app.file_functions import convert_to_json
from dionysus_app.student import Student
from dionysus_app.settings_functions import TEMP_DIR
from dionysus_app.UI_menus.UI_functions import clean_for_filename


class Class:
    """
    Class to contain a class' data eg student objects, related methods.
    ...

    Attributes
    ----------
    class_id : Any
        Class' id in database.

    name : str
        Class' name

    path_safe_name : str
        Cleaned string safe to use in file names and paths.

    students : list[Student]
        List of student objects for students in the class.

    Methods
    _______
    add_student(student: Student = None, **kwargs: Any):
        Adds a student to the class.

    json_dict():
        Translates Class object into JSON-serialisable dict.

    to_json_str():
        Converts Class in JSON-serialisable form to JSON string.

    Class Methods
    _____________
    from_dict(class_dict: dict):
        Instantiate Class object from JSON-serialisable dict.

    from_json(json_data: str):
        Return Class object from json string.

    from_file(cdf_path: Union[Path, str]):
        Return Class object from cdf file.

    """

    def __init__(self, name: str, students: list[Student]|None = None, *, class_id: Any = None) -> None:
        """
        Create Class instance.

        Can be instantiated with name only.

        :param name: str - name of the class.
        :param students: list[Student] - list of Student objects.
        :param class_id: Any - unique id of class in database.
        """
        self.id: Any = class_id
        self.name = name
        self.path_safe_name = name

        self.students = students if students else []

    @property
    def name(self) -> str:
        """
        Get class name.

        :return: str
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Set class name. Also sets path_safe_name.

        :param name: str
        :return: None
        """
        self._name = name
        self.path_safe_name = self._name

    @property
    def path_safe_name(self) -> str:
        """
        Get path_safe_name: filename-safe class name string.

        :return: str
        """
        return self._path_safe_name

    @path_safe_name.setter
    def path_safe_name(self, class_name: str) -> None:
        """
        Set path_safe_name: filename-safe class name string.

        :param class_name: str
        :return: None
        """
        self._path_safe_name = clean_for_filename(class_name)

    def __contains__(self, item: Union[str, Student]) -> bool:
        """
        Implement use of 'in' operator for membership testing or
        iterating over students in the class eg:
            name_str in instance_of_Class -> True/False
            Student_instance in instance_of_Class -> True/False

        NB if Student is imported via from student import Student, or in
        a manner other than rather than from dionysus_app.student (as it
        is here in class_.py), the comparison, will be between:
            <class 'dionysus_app.student.Student'> and
            <class 'student.Student'>
        - and will return False even though the .__class__.__name__ and
        .__class__.__qualname__ will both return 'Student'.

        NB2 if the student object is exactly equivalent to a student in
        the class (eg same name, avatar etc), but that specific object
        isn't in the class, the comparison will return False, instead,
        using the name is more robust.

        :param item: str or Student object
        :return: bool
        """
        if isinstance(item, str):
            name = item
            return name in (student.name for student in self.students)
        elif isinstance(item, Student):
            student = item
            return student in self.students
        else:
            raise ValueError(f'Expected type str or Student: '
                             f'received type {type(item)}.')

    def __iter__(self) -> Iterator[Student]:
        """
        Implement 'for' operator for iterating over students in class:

        eg:
            for student in instance_of_Class: # do something
             eg print(student.name)

        :yield: Student object
        """
        return iter(self.students)
        # Equivalent to:
        # yield from self.students
        # and:
        # for student in self.students:
        #     yield student

    def add_student(self, student: Student|None = None, **kwargs: Any) -> None:
        """
        Adds a student to the class.

        May be called with a student object as first argument, otherwise
        adds a Student object instantiated with supplied named
        parameters to list of students in class:

        Class.add_student(my_student_object)
        or
        Class.add_student(name='student_name', ...)

        NB If Student object is passed to student parameter, any kwargs
        are ignored, such that an avatar cannot be added to a student
        object while adding it to a class with a kwarg via this method.

        :param student: Student object.
        :type student: Student

        :keyword name: str - Name of student,
                                first arg to Student.__init__.

        For other keyword arguments, see Student object documentation.

        :raises: TypeError if non-Student positional argument passed.

        :return: None
        """
        if student:
            # Python 3.8:
            # if not isinstance(new_student := student, Student):
            #     raise TypeError(f"Student name must be a str, "
            #                     f"got {type(name)} instead.")
            if not isinstance(student, Student): raise TypeError(f"Student expected, got {type(student)} instead.")
            # raise inline with isinstance to show code causing error.
            # else:
            self.students.append(student)

        elif kwargs:  # and not student:
            self.students.append(Student(**kwargs))

    def json_dict(self) -> dict:
        """
        Translates Class object into JSON-serialisable dict.

        Captures name, converts Student objects to JSON-serialisable
        dicts. Omits id if not present.
        NB id will be last entry in dict and last entry in json string.

        :return: dict
        """
        json_data = {'name': self._name,
                     'students': [student.json_dict() for student in self.students]
                     }
        if self.id:
            json_data['id'] = self.id
        return json_data

    def to_json_str(self) -> str:
        """
        Converts Class in JSON-serialisable form to JSON string.

        :return: str
        """
        return convert_to_json(self.json_dict())

    # Alternate constructors

    @classmethod
    def from_dict(cls, class_dict: dict) -> Union['Class', 'NewClass']:
        """
        Instantiate Class object from JSON-serialisable dict.

        :param class_dict: dict
        :return: Class object
        """
        _id = class_dict.get('id')  # Class may not have id if not in db.
        _name = class_dict['name']
        _students = [Student.from_dict(student) for student in class_dict['students']]
        return cls(class_id=_id, name=_name, students=_students)

    @classmethod
    def from_json(cls, json_data: str) -> Union['Class', 'NewClass']:
        """
        Return Class object from json string.

        :param json_data: str
        :return: Class object
        """
        class_dict = json.loads(json_data)
        return cls.from_dict(class_dict)

    @classmethod
    def from_file(cls, cdf_path: Union[Path, str]) -> Union['Class', 'NewClass']:
        """
        Return Class object from cdf file.

        :param cdf_path: Path or str
        :return: Class object
        """
        with open(Path(cdf_path)) as class_data_file:
            class_json = json.load(class_data_file)
        return cls.from_dict(class_json)

    # String representations
    def __repr__(self) -> str:
        repr_str = (f'{self.__class__.__module__}.{self.__class__.__name__}('
                    f'id={self.id!r}, '
                    f'name={self._name!r}, '
                    f'path_safe_name={self._path_safe_name!r}, '
                    f'students={self.students!r}'
                    f')'
                    )
        return repr_str

    def __str__(self):
        if self.students:
            student_list_str = ', '.join([student.name for student in self.students])
            students_stmt = (f'containing {len(self.students)} students, '
                             f'with names: {student_list_str}')
        else:
            students_stmt = 'containing 0 students'

        return f'Class {self.name}, with id={self.id}, {students_stmt}.'


class NewClass(Class):
    """
    Subclass of Class for creating new classes.

    Adds machinery to facilitate creation of new classes in database.

    Adds temp directory for class to cache files before writing to
    database.
    This temp directory is garbage collected with the object upon object
    destruction.

    Temp directory is prefixed with the class' path_safe_name, plus a hash, and
    contains a subdirectory named 'avatars' to hold avatars before writing to
    database:

            TEMP_DIR
            ├── class_path_safe_name+hash
            |   ├── avatars

    NB: In future may be subclassed or housed in Database objects to
    allow database specific implementation.
    ...

    Attributes
    ----------
    As for baseclass Class.

    temp_dir: Path
        Path to class' temp directory.

    temp_avatars_dir: Path
        Path to avatars folder in class' temp directory.
    """

    def __init__(self, name: str, students: list[Student]|None = None, *, class_id: Any = None) -> None:
        super().__init__(name=name, students=students, class_id=class_id)

        # Create class temp directory.
        Path.mkdir(TEMP_DIR, exist_ok=True, parents=True)  # Ensure path exists.
        self.temp_dir: Path = Path(tempfile.mkdtemp(prefix=self._path_safe_name, dir=TEMP_DIR))
        # Create avatars directory within class temp directory.
        self.temp_avatars_dir: Path = self.temp_dir.joinpath('avatars')
        Path.mkdir(self.temp_avatars_dir)

    def __del__(self) -> None:
        """
        Temp folder garbage collected with object.

        :return: None
        """
        shutil.rmtree(self.temp_dir)
