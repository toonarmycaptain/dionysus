"""Tests for class.py"""
import pytest

from unittest import TestCase
from unittest.mock import patch

from dionysus_app.class_ import Class
from dionysus_app.file_functions import convert_to_json
from dionysus_app.student import Student

from test_suite.test_student import test_student_name_only, test_student_with_avatar
from test_suite.testing_class_data import test_class_name_only_data_set, test_full_class_data_set


@pytest.fixture()
def test_class_name_only():
    """Returns empty class instantiated with name only."""
    test_class_name_only = Class(test_class_name_only_data_set['json_dict_rep']['name'])

    # Add attributes to test expected output.
    test_class_name_only.json_str_rep = test_class_name_only_data_set['json_str_rep']
    test_class_name_only.json_dict_rep = test_class_name_only_data_set['json_dict_rep']

    return test_class_name_only


@pytest.fixture()
def test_full_class():
    test_full_class = Class(test_full_class_data_set['json_dict_rep']['name'])
    for student in test_full_class_data_set['json_dict_rep']['students']:
        test_full_class.add_student(Student(**student))

    test_full_class.json_str_rep = test_full_class_data_set['json_str_rep']
    test_full_class.json_dict_rep = test_full_class_data_set['json_dict_rep']

    return test_full_class


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
    """
    Test Class name and path_safe_name properties.
    """

    def setup_method(self):
        """
        Setup class name and name for change.
        """

        self.test_name = "The Knights of the Round-table: we don't say 'Ni!'"
        self.test_path_safe_name = "The_Knights_of_the_Round-table__we_don_t_say__Ni__"

        self.test_changed_name = 'Adaptable Knights: We now say Ni!, but we dont have to.'
        self.test_changed_path_safe_name = 'Adaptable_Knights__We_now_say_Ni___but_we_dont_have_to_'

    def test_name_getter(self, test_class_name_only):
        assert test_class_name_only.name == self.test_name

    def test_path_safe_name_getter(self, test_class_name_only):
        assert test_class_name_only.path_safe_name == self.test_path_safe_name

    def test_name_setter_unmocked(self, test_class_name_only):
        assert test_class_name_only.name != self.test_changed_name
        assert test_class_name_only.path_safe_name != self.test_changed_path_safe_name

        # Change name
        test_class_name_only.name = self.test_changed_name

        assert test_class_name_only.name == self.test_changed_name
        #  Assert name change carried over to path_safe_name attribute.
        assert test_class_name_only.path_safe_name == self.test_changed_path_safe_name


class TestClassNameMocked(TestCase):
    def setUp(self):
        self.test_name = "The Knights of the Round-table: we don't say 'Ni!'"
        self.test_path_safe_name = "The_Knights_of_the_Round-table_we_don't_say__Ni__"

        self.test_class = Class(self.test_name)

        self.test_changed_name = 'Adaptable Knights: We now say Ni!, but we dont have to.'
        self.test_changed_path_safe_name = 'Adaptable_Knights__We_now_say_Ni___but_we_dont_have_to_'

    @patch('dionysus_app.class_.clean_for_filename')
    def test_name_setter_mocked(self, mocked_clean_for_filename):
        # Assert name, path_safe_name initial value != changed value
        assert self.test_class.name != self.test_changed_name
        assert self.test_class.path_safe_name != self.test_changed_path_safe_name

        mocked_clean_for_filename.return_value = self.test_changed_path_safe_name

        # Change name
        self.test_class.name = self.test_changed_name

        assert self.test_class.name == self.test_changed_name
        #  Assert name change carried over to path_safe_name attribute.
        assert self.test_class.path_safe_name == self.test_changed_path_safe_name

        mocked_clean_for_filename.assert_called_once_with(self.test_changed_name)


class TestContainsMethod:
    def test__contains__student_obj_in_class(self, test_student_name_only, test_class_name_only):
        assert test_class_name_only.students == []  # No students in class
        test_class_name_only.add_student(test_student_name_only)

        assert test_student_name_only in test_class_name_only

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
                                         avatar_filename=test_student_with_avatar.avatar_filename)

        assert len(test_class_name_only.students) is 1
        # Test student attributes are as expected
        assert test_class_name_only.students[0].name == test_student_with_avatar.name
        assert test_class_name_only.students[0].avatar_filename == test_student_with_avatar.avatar_filename

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
    def test_test_class_name_only_to_json_dict(self, test_class_name_only):
        assert test_class_name_only.json_dict() == {'name': test_class_name_only.name,
                                                    'students': test_class_name_only.students
                                                    }

    def test_test_full_class_to_json_dict(self, test_full_class):
        assert test_full_class.json_dict() == test_full_class_data_set['json_dict_rep']


class TestToJsonStr:
    def test_test_class_name_only_to_json_str(self, test_class_name_only):
        """
        Have to be very careful with the string formatting here.
        To avoid hard-coding, have to insert values using f-strings, but insert
        on multiple lines as the {} not used by the fstring in JSON formatting
        raises errors. Also have to include \n in correct locations.
        """
        assert test_class_name_only.to_json_str() == test_class_name_only.json_str_rep

    def test_test_full_class_to_json_str(self, test_full_class):
        assert test_full_class.to_json_str() == test_full_class_data_set['json_str_rep']

    def test_to_json_str_is_equivalent_to_converting_dict_directly(self, test_full_class):
        assert convert_to_json(test_full_class.json_dict()) == test_full_class.to_json_str()


class TestFromDict:
    def test_from_dict_instantiation_class_name_only(self, test_class_name_only):
        assert Class.from_dict(test_class_name_only.json_dict_rep).json_dict() == test_class_name_only.json_dict()

    def test_from_dict_instantiation_full_class(self, test_full_class):
        assert Class.from_dict(test_full_class.json_dict_rep).json_dict() == test_full_class.json_dict()


class TestFromJson:
    def test_from_json_instantiation_class_name_only(self, test_class_name_only):
        assert Class.from_json(test_class_name_only.json_str_rep).json_dict() == test_class_name_only.json_dict()

    def test_from_json_instantiation_full_class(self, test_full_class):
        assert Class.from_json(test_full_class.json_str_rep).json_dict() == test_full_class.json_dict()


class TestFromFile:
    def test_from_file_load_class_name_only(self, tmp_path,
                                            test_class_name_only):
        # Setup test data file:
        class_data_file_name = test_class_name_only.path_safe_name + '.cdf'
        class_data_file_path = tmp_path.joinpath(class_data_file_name)

        with open(class_data_file_path, 'w+') as class_data_file:
            class_data_file.write(test_class_name_only.json_str_rep)

        assert Class.from_file(class_data_file_path).json_dict() == test_class_name_only.json_dict()

    def test_from_file_load_full_class(self, tmp_path,
                                       test_full_class):
        # Setup test data file:
        class_data_file_name = test_full_class.path_safe_name + '.cdf'
        class_data_file_path = tmp_path.joinpath(class_data_file_name)

        with open(class_data_file_path, 'w+') as class_data_file:
            class_data_file.write(test_full_class.json_str_rep)

        assert Class.from_file(class_data_file_path).json_dict() == test_full_class.json_dict()


class TestClassRepr:
    @pytest.mark.parametrize('class_object',
                             [Class(name='name_only_class'),
                              Class.from_dict(test_full_class_data_set['json_dict_rep']),
                              ])
    def test_repr(self, class_object):
        assert repr(class_object) == (f'{class_object.__class__.__module__}'
                                      f'.{class_object.__class__.__name__}('
                                      f'name={class_object._name!r}, '
                                      f'path_safe_name={class_object._path_safe_name!r}, '
                                      f'students={class_object.students!r})')


class TestClassStr:
    @pytest.mark.parametrize(
        'student_object,'
        'expected_str',
        [(Class(name='name_only_class'),
          f"Class {'name_only_class'}, containing 0 students."),
         (Class.from_dict(test_full_class_data_set['json_dict_rep']),
          f"Class {Class.from_dict(test_full_class_data_set['json_dict_rep']).name}, "
          f"containing {len(Class.from_dict(test_full_class_data_set['json_dict_rep']).students)} students, "
          f"with names: {', '.join([student.name for student in Class.from_dict(test_full_class_data_set['json_dict_rep']).students])}."),
         ])
    def test_str(self, student_object, expected_str, test_student_name_only, test_student_with_avatar):
        assert str(student_object) == expected_str
