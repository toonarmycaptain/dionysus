"""Tests for class.py"""
import pytest

from unittest import TestCase
from unittest.mock import patch

from dionysus_app.class_ import Class
from dionysus_app.student import Student

from test_suite.test_student import test_student_name_only, test_student_with_avatar_path
from test_suite.testing_class_data import test_class_name_only_data_set, test_full_class_data_set


@pytest.fixture()
def test_class_name_only():
    """Returns empty class instantiated with name only."""
    test_class_name_only = Class(test_class_name_only_data_set['json_dict_rep']['name'])

    # Add attributes to test expected output.
    test_class_name_only.json_str_rep = test_class_name_only_data_set['json_str_rep']
    test_class_name_only.json_dict_rep = test_class_name_only_data_set['json_dict_rep']

    return test_class_name_only

@ pytest.fixture()
def test_full_class():
    test_class = Class(test_full_class_data_set['json_dict_rep']['name'])
    for student in test_full_class_data_set['json_dict_rep']['students']:
        test_class.add_student(Student(**student))
    return test_class


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
                                   test_student_with_avatar_path):
        # Ensure empty class and students are student object.
        assert test_class_name_only.students == []
        assert isinstance(test_student_name_only, Student)
        assert isinstance(test_student_with_avatar_path, Student)

        test_class_name_only.add_student(test_student_name_only)
        test_class_name_only.add_student(test_student_with_avatar_path)

        assert test_class_name_only.students == [test_student_name_only,
                                                 test_student_with_avatar_path]

    def test_add_student_with_kwargs(self,
                                     test_class_name_only,
                                     test_student_with_avatar_path):
        # Ensure class initially empty.
        assert test_class_name_only.students == []

        test_class_name_only.add_student(name=test_student_with_avatar_path.name,
                                         avatar_path=test_student_with_avatar_path.avatar_path)

        assert len(test_class_name_only.students) is 1
        # Test student attributes are as expected
        assert test_class_name_only.students[0].name == test_student_with_avatar_path.name
        assert test_class_name_only.students[0].avatar_path == test_student_with_avatar_path.avatar_path

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
                              test_student_with_avatar_path,  # Student object
                              ])
    def test_add_student_with_non_str_name_kwarg(self,
                                                 test_class_name_only,
                                                 name_arg,
                                                 test_student_name_only,
                                                 test_student_with_avatar_path,
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
