import signal
from unittest import TestCase

import pexpect.popen_spawn


class TestClassList(TestCase):

    def setUp(self):
        self.child = pexpect.popen_spawn.PopenSpawn('python app_main.py')
        self.child.expect('1. Create a classlist', timeout=2)
        self.child.sendline('1')

    def tearDown(self):
        self.child.kill(signal.SIGINT)  # TODO: remove created fooclass files after test.

    def test_can_create_empty_class(self):
        self.child.expect('Please enter a name for the class:', timeout=2)
        self.child.sendline('fooclass')
        self.child.expect("Enter student name, or 'end':", timeout=2)
        self.child.sendline('end')
        self.child.expect('Do you want to create an empty class?', timeout=2)
        self.child.sendline('y')
        self.child.expect('Class name: fooclass', timeout=5)
        self.child.expect('No students entered', timeout=5)
