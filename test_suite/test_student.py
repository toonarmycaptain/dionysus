"""Tests for Student class."""
from unittest import mock, TestCase

from dionysus_app.student import Student


class TestStudent(TestCase):
    def setUp(self):
        self.test_name = 'Arthur, King of the Britons'
        self.test_path_safe_name = 'Arthur_King_of_the_Britons'

        self.test_student = Student(self.test_name)

        self.test_changed_name = 'Sir Lancelot: the not-so-brave'
        self.test_changed_path_safe_name = 'Sir_Lancelot_the_not-so-brave'

    def test_name_method(self):
        assert self.test_student.name == self.test_name

    def test_path_safe_name_method(self):
        assert self.test_student.path_safe_name == self.test_path_safe_name

    def test_change_name(self):
        assert self.test_student.name != self.test_changed_name
        assert self.test_student.path_safe_name != self.test_changed_path_safe_name

        # Change name
        self.test_student.name = self.test_changed_name

        assert self.test_student.name == self.test_changed_name
        #  Assert name change carried over to path_safe_name attribute.
        assert self.test_student.path_safe_name == self.test_changed_path_safe_name
