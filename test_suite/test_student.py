"""Tests for Student class."""
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from dionysus_app.student import Student


class TestStudent(TestCase):
    def setUp(self):
        self.test_name = 'Arthur, King of the Britons'
        self.test_path_safe_name = 'Arthur_King_of_the_Britons'

        self.test_student = Student(self.test_name)

        self.test_changed_name = 'Sir Lancelot: the not-so-brave'
        self.test_changed_path_safe_name = 'Sir_Lancelot_the_not-so-brave'

        self.test_avatar_path_str = 'camelot'
        self.test_avatar_path_path = Path('camelot')

    def test_name_getter(self):
        assert self.test_student.name == self.test_name

    def test_path_safe_name_getter(self):
        assert self.test_student.path_safe_name == self.test_path_safe_name

    def test_name_setter_unmocked(self):
        assert self.test_student.name != self.test_changed_name
        assert self.test_student.path_safe_name != self.test_changed_path_safe_name

        # Change name
        self.test_student.name = self.test_changed_name

        assert self.test_student.name == self.test_changed_name
        #  Assert name change carried over to path_safe_name attribute.
        assert self.test_student.path_safe_name == self.test_changed_path_safe_name

    @patch('dionysus_app.student.clean_for_filename')
    def test_name_setter_mocked(self, mocked_clean_for_filename):
        assert self.test_student.name != self.test_changed_name
        assert self.test_student.path_safe_name != self.test_changed_path_safe_name

        mocked_clean_for_filename.return_value = self.test_changed_path_safe_name

        # Change name
        self.test_student.name = self.test_changed_name

        assert self.test_student.name == self.test_changed_name
        #  Assert name change carried over to path_safe_name attribute.
        assert self.test_student.path_safe_name == self.test_changed_path_safe_name

        mocked_clean_for_filename.assert_called_once_with(self.test_changed_name)

    def test_no_avatar_on_instantiation(self):
        assert self.test_student.avatar_path is None

    def test_change_avatar_passing_str(self):
        assert self.test_student.avatar_path != self.test_avatar_path_path

        self.test_student.avatar_path = self.test_avatar_path_path

        assert isinstance(self.test_student.avatar_path, Path)
        assert self.test_student.avatar_path == self.test_avatar_path_path

    def test_change_avatar_passing_path(self):
        assert self.test_student.avatar_path != self.test_avatar_path_path

        self.test_student.avatar_path = self.test_avatar_path_path

        assert isinstance(self.test_student.avatar_path, Path)
        assert self.test_student.avatar_path == self.test_avatar_path_path

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
