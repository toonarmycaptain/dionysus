"""Tests for Student class."""
from unittest import mock, TestCase

from dionysus_app.student import Student


class TestStudent(TestCase):
    def setUp(self):
        self.test_name = 'Arthur, King of the Britons'
        self.test_path_safe_name = 'Arthur_King_of_the_Britons'

        self.test_student = Student(self.test_name)

    def test_name_method(self):
        assert self.test_student.name is self.test_name