"""Tests for Student class."""
import pytest

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from dionysus_app.student import Student


@pytest.fixture()
def test_student_name_only():
    test_name = 'Arthur, King of the Britons'
    yield Student(test_name)


class TestStudentNamePathSafeName:
    """
    Test Student name and path_safe_name properties.
    """

    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """

        self.test_name = 'Arthur, King of the Britons'
        self.test_path_safe_name = 'Arthur_King_of_the_Britons'

        self.test_changed_name = 'Sir Lancelot: the not-so-brave'
        self.test_changed_path_safe_name = 'Sir_Lancelot_the_not-so-brave'

    def test_name_getter(self, test_student_name_only):
        assert test_student_name_only.name == self.test_name

    def test_path_safe_name_getter(self, test_student_name_only):
        assert test_student_name_only.path_safe_name == self.test_path_safe_name

    def test_name_setter_unmocked(self, test_student_name_only):
        assert test_student_name_only.name != self.test_changed_name
        assert test_student_name_only.path_safe_name != self.test_changed_path_safe_name

        # Change name
        test_student_name_only.name = self.test_changed_name

        assert test_student_name_only.name == self.test_changed_name
        #  Assert name change carried over to path_safe_name attribute.
        assert test_student_name_only.path_safe_name == self.test_changed_path_safe_name


class TestStudentNameMocked(TestCase):
    def setUp(self):
        self.test_name = 'Arthur, King of the Britons'
        self.test_path_safe_name = 'Arthur_King_of_the_Britons'

        self.test_student = Student(self.test_name)

        self.test_changed_name = 'Sir Lancelot: the not-so-brave'
        self.test_changed_path_safe_name = 'Sir_Lancelot_the_not-so-brave'

    @patch('dionysus_app.student.clean_for_filename')
    def test_name_setter_mocked(self, mocked_clean_for_filename):
        # Assert name, path_safe_name initial value != changed value
        assert self.test_student.name != self.test_changed_name
        assert self.test_student.path_safe_name != self.test_changed_path_safe_name

        mocked_clean_for_filename.return_value = self.test_changed_path_safe_name

        # Change name
        self.test_student.name = self.test_changed_name

        assert self.test_student.name == self.test_changed_name
        #  Assert name change carried over to path_safe_name attribute.
        assert self.test_student.path_safe_name == self.test_changed_path_safe_name

        mocked_clean_for_filename.assert_called_once_with(self.test_changed_name)


class TestStudentAvatar:
    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.test_name = 'Arthur, King of the Britons'
        self.test_avatar_path_str = 'camelot'
        self.test_avatar_path_path = Path('camelot')

    def test_no_avatar_on_instantiation(self, test_student_name_only):
        assert test_student_name_only.avatar_path is None

    def test_change_avatar_passing_str(self, test_student_name_only):
        assert test_student_name_only.avatar_path != self.test_avatar_path_path

        test_student_name_only.avatar_path = self.test_avatar_path_path

        assert isinstance(test_student_name_only.avatar_path, Path)
        assert test_student_name_only.avatar_path == self.test_avatar_path_path

    def test_change_avatar_passing_path(self, test_student_name_only):
        assert test_student_name_only.avatar_path != self.test_avatar_path_path

        test_student_name_only.avatar_path = self.test_avatar_path_path

        assert isinstance(test_student_name_only.avatar_path, Path)
        assert test_student_name_only.avatar_path == self.test_avatar_path_path

    # Test instantiate with avatar_path:

    def test_instantiate_with_avatar_path_str(self):
        test_instantiate_student_with_avatar = Student(self.test_name,
                                                       self.test_avatar_path_str)

        assert test_instantiate_student_with_avatar.avatar_path == self.test_avatar_path_path

        assert isinstance(test_instantiate_student_with_avatar.avatar_path, Path)

    def test_instantiate_with_avatar_path_path(self):
        test_instantiate_student_with_avatar = Student(self.test_name,
                                                       self.test_avatar_path_path)

        assert test_instantiate_student_with_avatar.avatar_path == self.test_avatar_path_path

        assert isinstance(test_instantiate_student_with_avatar.avatar_path, Path)
