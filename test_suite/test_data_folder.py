import os

from pathlib import Path
from unittest import TestCase

from definitions import ROOT_DIR
from dionysus_app.class_registry_functions import write_registry_to_disk
from dionysus_app.data_folder import DataFolder
from dionysus_app.initialise_app import data_folder_check
from dionysus_app.settings_functions import write_settings_to_file


class TestDataFolder(TestCase):

    def setUp(self):
        # set correct cwd:
        os.chdir(ROOT_DIR)
        self.default_paths = [
            r'/dionysus_app'  
            r'/dionysus_app/app_data',
            r'/dionysus_app/app_data/class_data',
            r'/dionysus_app/app_data/class/registry.index',
            r'/dionysus_app/app_data/settings.py',
            r'/dionysus_app/chart_generator',
            r'/dionysus_app/chart_generator/default_avatar.png',
            ]

    def test_generate_data_path_defaults(self):
        os.chdir(ROOT_DIR)
        cwd_path = Path.cwd()
        for rel_path_str in self.default_paths:
            path_result = DataFolder.generate_rel_path(rel_path_str)
            
            # Assert relative app paths in generated absolute paths:
            assert rel_path_str in path_result.as_uri()
            # Assert cwd in generated absolute paths:
            assert cwd_path.as_uri() in path_result.as_uri()

    def test_generate_data_path_None(self):
        # Should return current working directory:
        none_path_result = DataFolder.generate_rel_path(None)
        cwd_path = Path.cwd()
        
        assert cwd_path == none_path_result


class TestDataFolderPathsExist(TestCase):
    def setUp(self):
        """
        Ensure file system and key files with paths in DataFolder exist.

        This only semi-circular (ie x= value; assert value = x), because
        the files are created by the code the app would normally use to
        create these files, and if they're creating them in a place
        other than at the specified paths, the test *should* fail.
        """
        # Create app file system, key files with paths in DataFolder
        data_folder_check()  # App data folders

        # Create dummy registry file if necessary
        self.dummy_registry_file = False
        self.registry_path = DataFolder.generate_rel_path(DataFolder.CLASS_REGISTRY.value)
        if not os.path.exists(self.registry_path):
            self.dummy_registry_file = True
            registry_list = ['A_test_class', 'Another_test_class']
            write_registry_to_disk(registry_list)

        # Create dummy settings file if necessary
        self.dummy_settings_file = False
        self.settings_path = DataFolder.generate_rel_path(DataFolder.APP_SETTINGS.value)
        if not os.path.exists(self.settings_path):
            self.dummy_settings_file = True
            settings_dict = {'There were': 'no settings set.'}
            write_settings_to_file(settings_dict)

    def test_paths_exist(self):
        for path in DataFolder:
                path = DataFolder.generate_rel_path(path.value)
                assert os.path.exists(path)

    def tearDown(self):
        # Remove dummy files.
        if self.dummy_registry_file:
            os.remove(self.registry_path)
        if self.dummy_settings_file:
            os.remove(self.settings_path)
