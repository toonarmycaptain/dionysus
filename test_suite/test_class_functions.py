"""Test functions in class_functions.py"""

import os

from unittest import TestCase

import definitions

from dionysus_app.class_functions import CLASSLIST_DATA_PATH, copy_avatar_to_app_data, setup_class_data_storage




class TestSetupClassDataStorage(TestCase):
    pass


class TestCopyAvatarToAppData(TestCase):
    def setUp(self):
        # arguments to copy_avatar_to_app_data
        self.test_classlist_name = 'arthurs_knights'
        self.test_avatar_filename = 'sir_lancelot_the_looker.image'
        self.copied_avatar_save_filename = 'sir_lancelot.png'

        # create test file and structure.
        with open(self.test_avatar_filename, 'w+') as avatar_file:
                        pass

        # Mock out global for test:

        # Save original value to restore in tearDown
        self.DEFAULT_CHART_SAVE_FOLDER_value = definitions.DEFAULT_CHART_SAVE_FOLDER
        # Mock value
        definitions.DEFAULT_CHART_SAVE_FOLDER = '.'


        setup_class_data_storage(self.test_classlist_name)
        self.test_class_datafolder_path = CLASSLIST_DATA_PATH.joinpath(self.test_classlist_name)
        self.test_class_avatar_subfolder_path = self.test_class_datafolder_path.joinpath('avatars')
        self.test_class_chart_data_subfolder_path = self.test_class_datafolder_path.joinpath('chart_data')

    def test_copy_avatar_to_app_data(self):
        # assert test preconditions met
        assert os.path.exists(self.test_avatar_filename)
        assert os.path.exists(self.test_class_avatar_subfolder_path)

        self.copied_avatar_filepath = self.test_class_avatar_subfolder_path.joinpath(self.copied_avatar_save_filename)
        assert not os.path.exists(self.copied_avatar_filepath)

        copy_avatar_to_app_data(self.test_classlist_name, self.test_avatar_filename, self.copied_avatar_save_filename)
        assert os.path.exists(self.copied_avatar_filepath)

    def tearDown(self):
        os.remove(self.test_avatar_filename)  # remove test avatar file

        os.remove(self.copied_avatar_filepath)  # remove copied avatar
        os.rmdir(self.test_class_avatar_subfolder_path)  # remove class_datafolder/avatars
        os.rmdir(self.test_class_chart_data_subfolder_path)  # remove class_datafolder/chart_data
        os.rmdir(self.test_class_datafolder_path)  # remove class_datafolder
        os.rmdir(self.test_classlist_name)  # remove user_save_charts folder

        # Restore definitions.DEFAULT_CHART_SAVE_FOLDER to original value
        definitions.DEFAULT_CHART_SAVE_FOLDER = self.DEFAULT_CHART_SAVE_FOLDER_value
