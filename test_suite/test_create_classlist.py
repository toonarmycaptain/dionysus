import signal
from unittest import TestCase

import pexpect.popen_spawn


class TestClassList(TestCase):
    def setUp(self):
        pass  # skip these tests

        # self.child = pexpect.popen_spawn.PopenSpawn('python app_main.py')
        # self.child.expect('1. Create a classlist', timeout=3)
        # self.child.sendline('1')

    def tearDown(self):
        """
        To do: remove created fooclass files after test.
        :return:
        """
        pass  # skip these tests
        # self.child.kill(signal.SIGINT)

    def test_can_create_empty_class(self):
        pass  # skip these tests
        # self.child.expect('Please enter a name for the class:', timeout=3)
        # self.child.sendline('fooclass')  # NB this will fail on subsequent runs when run locally.
        # self.child.expect("Enter student name, or 'end', and hit enter: ", timeout=3)
        # self.child.sendline('end')
        # self.child.expect('Do you want to create an empty class?', timeout=3)
        # self.child.sendline('y')
        # self.child.expect('Class name: fooclass', timeout=5)
        # self.child.expect('No students entered', timeout=5)

    def test_create_nonempty_class(self):
        pass

    def test_create_class_with_already_existing_classname(self):
        pass
