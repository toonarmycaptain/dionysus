"""Tests for class.py"""
import pytest

from unittest import TestCase
from unittest.mock import patch

from dionysus_app.class_ import Class
from dionysus_app.student import Student
from test_suite.test_student import test_student_name_only


@pytest.fixture()
def test_class_name_only():
    """Returns empty class instantiated with name only."""
    test_name = "The Knights of the Round-table: we don't say 'Ni!'"
    yield Class(test_name)


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
    Test Student name and path_safe_name properties.
    """

    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """

        self.test_name = "The Knights of the Round-table: we don't say 'Ni!'"
        self.test_path_safe_name = "The_Knights_of_the_Round-table__we_don_t_say_'Ni__"

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


class TestAddStudent(TestCase):
    """Test add_student method."""

    def setUp(self):
        self.test_class = Class('my test_class')
        self.test_student = Student('Arthur')

    def test_add_student_student_arg_is_student_obj(self):
        assert self.test_class.students == []
        assert isinstance(self.test_student, Student)
        self.test_class.add_student(self.test_student)

        assert self.test_class.students == [self.test_student]

    def test_add_student_student_arg_is_string(self):
        assert self.test_class.students == []

        self.test_class.add_student('test_student_name')

        assert self.test_class.students == []

    def test_add_student_with_kwargs(self):
        pass

    def test_add_student_with_non_str_name_kwarg(self):
        pass

# add Student obj *
# positional argument given but not Student obj (eg 'student name' *
# add Student from params
# do nothing if name= param is not str.

# test_student_name_only_object = test_student_name_only