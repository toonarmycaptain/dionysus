"""Tests for class.py"""
import os

import pytest

from pathlib import Path

from dionysus_app import class_
from dionysus_app.class_ import Class, NewClass
from dionysus_app.file_functions import convert_to_json
from dionysus_app.student import Student

from test_suite.test_student import test_student_name_only, test_student_with_avatar
from test_suite.testing_class_data import test_class_name_only_data_set, test_full_class_data_set


@pytest.fixture()
def test_class_name_only():
    """Returns empty class instantiated with name only."""
    test_class_name_only = Class(class_id=test_class_name_only_data_set['json_dict_rep']['id'],
                                 name=test_class_name_only_data_set['json_dict_rep']['name'])

    # Add attributes to test expected output.
    test_class_name_only.json_str_rep = test_class_name_only_data_set['json_str_rep']
    test_class_name_only.json_dict_rep = test_class_name_only_data_set['json_dict_rep']

    return test_class_name_only


@pytest.fixture()
def test_full_class() -> Class:
    test_full_class = Class(class_id=test_full_class_data_set['json_dict_rep']['id'],
                            name=test_full_class_data_set['json_dict_rep']['name'])
    for student in test_full_class_data_set['json_dict_rep']['students']:
        test_full_class.add_student(Student(**student))

    test_full_class.json_str_rep = test_full_class_data_set['json_str_rep']
    test_full_class.json_dict_rep = test_full_class_data_set['json_dict_rep']

    return test_full_class


@pytest.fixture()
def test_new_class_name_only():
    """Returns empty NewClass instantiated with name only."""
    test_new_class_name_only = NewClass(test_class_name_only_data_set['json_dict_rep']['name'])

    # Add attributes to test expected output.
    test_new_class_name_only.json_str_rep = test_class_name_only_data_set['json_str_rep']
    test_new_class_name_only.json_dict_rep = test_class_name_only_data_set['json_dict_rep']

    return test_new_class_name_only


@pytest.fixture()
def test_full_new_class():
    """Returns empty NewClass instantiated with students."""
    test_full_new_class = NewClass(test_full_class_data_set['json_dict_rep']['name'])
    for student in test_full_class_data_set['json_dict_rep']['students']:
        test_full_new_class.add_student(Student(**student))

    test_full_new_class.json_str_rep = test_full_class_data_set['json_str_rep']
    test_full_new_class.json_dict_rep = test_full_class_data_set['json_dict_rep']

    return test_full_new_class


@pytest.mark.parametrize(
    'class_name, class_list_arg, list_of_students',
    [('slightly silly', ['silly', 'sillier', 'silliest'], ['silly', 'sillier', 'silliest']),
     ('egg', [], []),  # Empty list of students/empty class.
     ('eggs', None, []),  # None passed explicitly.
     ])
def test_class_student_list_instantiation(class_name, class_list_arg, list_of_students):
    test_class = Class(class_name, class_list_arg)  # Need class of test students

    assert test_class.students == list_of_students


def test_class_student_list_instantiation_no_list_arg():
    test_class = Class('test_class_name')

    assert test_class.students == []


class TestClassNamePathSafeName:
    """Test Class name and path_safe_name properties."""

    def test_name_getter(self):
        test_name = "The Knights of the Round-table: we don't say 'Ni!'"
        assert Class(test_name).name == test_name

    def test_path_safe_name_getter(self):
        assert Class("The Knights of the Round-table: we don't say 'Ni!'"
                     ).path_safe_name == "The_Knights_of_the_Round-table__we_don_t_say__Ni__"

    def test_path_safe_name_getter_mocking_calls(self, monkeypatch):
        mock_path_safe_name = "Something completely different."

        def mocked_clean_for_filename(class_name):
            return mock_path_safe_name

        monkeypatch.setattr(class_, 'clean_for_filename', mocked_clean_for_filename)

        assert Class("The Knights of the Round-table: we don't say 'Ni!'").path_safe_name == mock_path_safe_name

    def test_name_setter(self):
        test_name = "The Knights of the Round-table: we don't say 'Ni!'"

        test_changed_name = 'Adaptable Knights: We now say Ni!, but we dont have to.'
        test_changed_path_safe_name = 'Adaptable_Knights__We_now_say_Ni___but_we_dont_have_to_'

        test_class = Class(test_name)

        # Original test_class attributes not equal to changed:
        assert (test_class.name, test_class.path_safe_name) != (test_changed_name, test_changed_path_safe_name)

        # Change name
        test_class.name = test_changed_name

        assert (test_class.name, test_class.path_safe_name) == (test_changed_name, test_changed_path_safe_name)

    def test_name_setter_mocking_calls(self, monkeypatch):
        test_name = "The Knights of the Round-table: we don't say 'Ni!'"

        test_changed_name = 'Adaptable Knights: We now say Ni!, but we dont have to.'
        mock_changed_path_safe_name = "Adaptable_Knights: We're Niiiearly completely un!safe?!$"

        test_class = Class(test_name)

        # Original test_class attributes not equal to changed:
        assert (test_class.name, test_class.path_safe_name) != (test_changed_name, mock_changed_path_safe_name)

        def mocked_clean_for_filename(class_name):
            return mock_changed_path_safe_name

        monkeypatch.setattr(class_, 'clean_for_filename', mocked_clean_for_filename)

        # Change name
        test_class.name = test_changed_name

        assert (test_class.name, test_class.path_safe_name) == (test_changed_name, mock_changed_path_safe_name)


class TestClassId:
    """Test Class Id"""

    @pytest.mark.parametrize(
        'id_arg,',
        [17,  # Integer eg sql db id
         'some student_name',  # JSON db id
         Student(name='Student used to represent complex object'),  # Ensure 'Any' typing is accurate.
         ])
    def test_id(self, id_arg):
        assert Class(name='Four Yorkshiremen', class_id=id_arg).id == id_arg

    def test_class_id_default_arg(self):
        assert Class(name='Four Yorkshiremen').id is None


class TestContainsMethod:
    def test__contains__student_obj_in_class(self, test_student_name_only, test_class_name_only):
        """Test that student object from class compares as `in` class."""
        assert test_class_name_only.students == []  # No students in class
        test_class_name_only.add_student(test_student_name_only)

        assert test_student_name_only in test_class_name_only

    def test__contains__identical_but_not_actual_student_obj_in_class(self, test_student_name_only,
                                                                      test_class_name_only):
        """
        Test identical student object in class.
        Should return False, since the specific object is not in the class.
        eg id(test_student) != id(test_class_name_only.students[0])
        """
        assert test_class_name_only.students == []  # No students in class
        name, avatar_id = 'test_student', 'test_student_avatar'
        test_student = Student(name=name, avatar_id=avatar_id)
        test_class_name_only.add_student(name=name, avatar_id=avatar_id)

        assert test_student not in test_class_name_only

    def test__contains__student_obj_not_in_empty_class(self, test_student_name_only, test_class_name_only):
        assert test_class_name_only.students == []  # No students in class

        assert test_student_name_only not in test_class_name_only

    def test__contains___str_name_in_class(self, test_class_name_only):
        test_student_name = 'Mostly silly'
        assert test_class_name_only.students == []  # No students in class
        test_class_name_only.add_student(name=test_student_name)

        assert test_student_name in test_class_name_only

    def test__contains__fixture_student_name_in_class(self, test_student_name_only, test_class_name_only):
        assert test_class_name_only.students == []  # No students in class
        test_class_name_only.add_student(test_student_name_only)

        assert test_student_name_only.name in test_class_name_only

    def test__contains__str_name_in_full_class(self, test_full_class):
        """Test with more than one student in class."""
        test_student_name = 'Mostly silly'
        test_full_class.add_student(name=test_student_name)

        assert test_student_name in test_full_class

    def test__contains__str_name_not_in_class(self, test_class_name_only):
        assert test_class_name_only.students == []  # No students in class

        assert 'Slightly silly' not in test_class_name_only

    def test__contains__fixture_student_str_name_not_in_class(self, test_student_name_only, test_class_name_only):
        assert test_class_name_only.students == []  # No students in class

        assert test_student_name_only.name not in test_class_name_only

    def test__contains__str_name_not_in_full_class(self, test_full_class):
        """Test with more than one student in class."""
        assert 'Some Name' not in test_full_class

    @pytest.mark.parametrize(
        'contains_arg',
        [{'passing a dict': 'Some value'},  # dict
         ['passing', 'a', 'list'],  # list
         ('passed', 'tuple',),  # tuple
         ])
    def test_non_str_or_student_obj_arg_throws_value_error(self, test_class_name_only, contains_arg):
        with pytest.raises(ValueError, match=str(type(contains_arg))):
            confirm = contains_arg in test_class_name_only
            assert confirm is not True


class TestIterMethod:
    def test_iter_method_returns_iterator(self, test_class_name_only):
        assert isinstance(test_class_name_only.__iter__(), type([].__iter__()))


class TestAddStudent:
    """Test Class.add_student method."""

    def test_add_student_student_arg_is_student_obj(self,
                                                    test_class_name_only,
                                                    test_student_name_only):
        # Ensure empty class and student is student object.
        assert test_class_name_only.students == []
        assert isinstance(test_student_name_only, Student)

        test_class_name_only.add_student(test_student_name_only)

        assert test_class_name_only.students == [test_student_name_only]

    def test_add_multiple_students(self,
                                   test_class_name_only,
                                   test_student_name_only,
                                   test_student_with_avatar):
        # Ensure empty class and students are student object.
        assert test_class_name_only.students == []
        assert isinstance(test_student_name_only, Student)
        assert isinstance(test_student_with_avatar, Student)

        test_class_name_only.add_student(test_student_name_only)
        test_class_name_only.add_student(test_student_with_avatar)

        assert test_class_name_only.students == [test_student_name_only,
                                                 test_student_with_avatar]

    def test_add_student_with_kwargs(self,
                                     test_class_name_only,
                                     test_student_with_avatar):
        # Ensure class initially empty.
        assert test_class_name_only.students == []

        test_class_name_only.add_student(name=test_student_with_avatar.name,
                                         avatar_id=test_student_with_avatar.avatar_id)

        assert len(test_class_name_only.students) == 1
        # Test student attributes are as expected
        assert test_class_name_only.students[0].name == test_student_with_avatar.name
        assert test_class_name_only.students[0].avatar_id == test_student_with_avatar.avatar_id

    @pytest.mark.parametrize('student_arg',
                             ['student name',  # string
                              ['passing', 'a', 'list'],  # list
                              ('passed', 'tuple',),  # tuple
                              {'passing a dict': 'Some value'},  # dict
                              ])
    def test_add_student_non_student_student_arg_raises_error(self,
                                                              test_class_name_only,
                                                              student_arg):
        """
        Test non Student positional argument.
        String could conceivably be passed if intending to pass non-kwarg student name.

        Test error is raised for each bad type, error msg contains type.
        """
        # Ensure class initially empty.
        assert test_class_name_only.students == []

        with pytest.raises(TypeError, match=str(type(student_arg))):
            test_class_name_only.add_student(student_arg)

        # Ensure class still empty (since no student should have been added).
        assert test_class_name_only.students == []

    @pytest.mark.parametrize('name_arg',
                             [{'passing a dict': 'Some value'},  # dict
                              ['passing', 'a', 'list'],  # list
                              ('passed', 'tuple',),  # tuple
                              test_student_name_only,  # Student object
                              test_student_with_avatar,  # Student object
                              ])
    def test_add_student_with_non_str_name_kwarg(self,
                                                 test_class_name_only,
                                                 name_arg,
                                                 test_student_name_only,
                                                 test_student_with_avatar,
                                                 ):
        """
        Test Class.add_student(name=) argument.
        String could conceivably be passed if intending to pass non-kwarg student name.

        Test error is raised for each bad type, error msg contains type.
        """
        # Ensure class initially empty.
        assert test_class_name_only.students == []

        with pytest.raises(TypeError, match=str(type(name_arg))):
            test_class_name_only.add_student(name=name_arg)

        # Ensure class still empty (since no student should have been added).
        assert test_class_name_only.students == []


class TestJSONDict:
    @pytest.mark.parametrize('test_class', ('test_class_name_only', 'test_full_class'))
    def test_class_to_json_dict(self, request, test_class):
        test_class = request.getfixturevalue(test_class)
        assert test_class.json_dict() == test_class.json_dict_rep


class TestToJsonStr:
    @pytest.mark.parametrize('test_class', ('test_class_name_only', 'test_full_class'))
    def test_class_to_json_str(self, request, test_class):
        """
        Have to be very careful with the string formatting here.
        To avoid hard-coding, have to insert values using f-strings, but insert
        on multiple lines as the {} not used by the fstring in JSON formatting
        raises errors. Also have to include \n in correct locations.
        """
        test_class = request.getfixturevalue(test_class)
        assert test_class.to_json_str() == test_class.json_str_rep

    @pytest.mark.parametrize('test_class', ('test_class_name_only', 'test_full_class'))
    def test_to_json_str_is_equivalent_to_converting_dict_directly(self, request, test_class):
        test_class = request.getfixturevalue(test_class)
        assert convert_to_json(test_class.json_dict()) == test_class.to_json_str()


class TestFromDict:
    @pytest.mark.parametrize('class_def', [Class, NewClass])
    @pytest.mark.parametrize('test_class', ('test_class_name_only', 'test_full_class'))
    def test_from_dict_instantiation(self, request, class_def, test_class):
        test_class = request.getfixturevalue(test_class)
        assert class_def.from_dict(test_class.json_dict_rep).json_dict() == test_class.json_dict()

    @pytest.mark.parametrize('class_def', [Class, NewClass])
    @pytest.mark.parametrize('test_class', ('test_class_name_only', 'test_full_class'))
    def test_from_dict_instantiation_class_is_correct_type(self, request, class_def, test_class):
        """Method should return instance of calling class/subclass."""
        test_class = request.getfixturevalue(test_class)
        assert isinstance(class_def.from_dict(test_class.json_dict_rep), class_def)


class TestFromJson:
    @pytest.mark.parametrize('class_def', [Class, NewClass])
    @pytest.mark.parametrize('test_class', ('test_class_name_only', 'test_full_class'))
    def test_from_json_instantiation(self, request, class_def, test_class):
        test_class = request.getfixturevalue(test_class)
        assert class_def.from_json(test_class.json_str_rep).json_dict() == test_class.json_dict()

    @pytest.mark.parametrize('class_def', [Class, NewClass])
    @pytest.mark.parametrize('test_class', ('test_class_name_only', 'test_full_class'))
    def test_from_json_instantiation_class_is_correct_type(self, request, class_def, test_class):
        """Method should return instance of calling class/subclass."""
        test_class = request.getfixturevalue(test_class)
        assert isinstance(class_def.from_json(test_class.json_str_rep), class_def)


class TestFromFile:
    @pytest.mark.parametrize('class_def', [Class, NewClass])
    @pytest.mark.parametrize('test_class', ('test_class_name_only', 'test_full_class'))
    def test_from_file_load_full_class(self, request, tmp_path,
                                       class_def, test_class):
        test_class = request.getfixturevalue(test_class)
        # Setup test data file:
        class_data_file_name = test_class.path_safe_name + '.cdf'
        class_data_file_path = tmp_path.joinpath(class_data_file_name)

        with open(class_data_file_path, 'w+') as class_data_file:
            class_data_file.write(test_class.json_str_rep)

        assert class_def.from_file(class_data_file_path).json_dict() == test_class.json_dict()

    @pytest.mark.parametrize('class_def', [Class, NewClass])
    @pytest.mark.parametrize('test_class', ('test_class_name_only', 'test_full_class'))
    def test_from_file_load_full_class_is_correct_type(self, request, tmp_path,
                                                       class_def, test_class):
        """Method should return instance of calling class/subclass."""
        test_class = request.getfixturevalue(test_class)
        # Setup test data file:
        class_data_file_name = test_class.path_safe_name + '.cdf'
        class_data_file_path = tmp_path.joinpath(class_data_file_name)

        with open(class_data_file_path, 'w+') as class_data_file:
            class_data_file.write(test_class.json_str_rep)

        assert isinstance(class_def.from_file(class_data_file_path), class_def)


class TestClassRepr:
    @pytest.mark.parametrize('class_object',
                             [Class(name='name_only_class'),
                              Class(name='name only class with id', class_id='a class id'),
                              Class.from_dict(test_full_class_data_set['json_dict_rep']),
                              ])
    def test_repr(self, class_object):
        assert repr(class_object) == (f'{class_object.__class__.__module__}.{class_object.__class__.__name__}('
                                      f'id={class_object.id if class_object.id else None !r}, '
                                      f'name={class_object._name!r}, '
                                      f'path_safe_name={class_object._path_safe_name!r}, '
                                      f'students={class_object.students!r}'
                                      f')')


class TestClassStr:
    @pytest.mark.parametrize(
        'class_object,'
        'expected_str',
        [(Class(name='name_only_class'),
          f"Class {'name_only_class'}, with id=None, containing 0 students."),
         (Class(class_id='some class id', name='name_only_class with id'),
          f"Class {'name_only_class with id'}, with id={'some class id'}, containing 0 students."),
         (Class.from_dict(test_full_class_data_set['json_dict_rep']),
          f"Class {Class.from_dict(test_full_class_data_set['json_dict_rep']).name}, "
          f"with id={Class.from_dict(test_full_class_data_set['json_dict_rep']).id}, "
          f"containing {len(Class.from_dict(test_full_class_data_set['json_dict_rep']).students)} students, "
          f"with names: {', '.join([student.name for student in Class.from_dict(test_full_class_data_set['json_dict_rep']).students])}."),
         (Class(class_id='some class id', name='small_class with id',
                students=[Student(name='one'), Student(name='two')]),
          f"Class {'small_class with id'}, "
          f"with id={'some class id'}, "
          f"containing 2 students, "
          f"with names: one, two."),

         ])
    def test_str(self, class_object, expected_str):
        assert str(class_object) == expected_str


class TestNewClass:
    def test_new_class_temp_dir_created(self, monkeypatch, tmpdir):
        test_temp_dir = Path(tmpdir, 'temp_dir')
        test_temp_dir.mkdir(parents=True)  # Make temp_dir.
        assert not os.listdir(test_temp_dir)  # Nothing in test_temp_dir.

        monkeypatch.setattr(class_, 'TEMP_DIR', test_temp_dir)

        test_class = NewClass("Sir Robin's baboons")

        assert test_class.temp_dir.exists()
        assert test_class.temp_dir.name in os.listdir(test_temp_dir)
        # Check temp_avatars_dir
        assert test_class.temp_avatars_dir.exists()
        # noinspection PyTypeChecker
        assert test_class.temp_avatars_dir.name in os.listdir(test_class.temp_dir)

    def test_new_class_temp_dir_deleted_on_deletion(self, monkeypatch, tmpdir):
        test_temp_dir = Path(tmpdir, 'temp_dir')
        test_temp_dir.mkdir(parents=True)  # Make temp_dir.
        assert not os.listdir(test_temp_dir)  # Nothing in test_temp_dir.

        monkeypatch.setattr(class_, 'TEMP_DIR', test_temp_dir)

        test_class = NewClass("Sir Robin's baboons")
        assert test_class.temp_dir.exists() and os.listdir(test_temp_dir)  # Class temp dir in test_temp_dir.
        del test_class  # NB May throw an (ignored) Exception because the class is garbage collected before this line.
        # No class temp dir in test_temp_dir:
        assert not os.listdir(test_temp_dir)

    def test_new_class_uses_path_safe_name(self):
        # Ensure class name has disallowed characters - validate test.
        test_new_class = NewClass("S|r Røbin's ß@boon$")
        assert test_new_class.name != test_new_class.path_safe_name

        # Ensure class_name_with_disallowed chars in temp dir path.
        assert test_new_class.name not in str(test_new_class.temp_dir)
        # Ensure path_safe_name is in temp dir path.
        assert test_new_class.path_safe_name in str(test_new_class.temp_dir)
