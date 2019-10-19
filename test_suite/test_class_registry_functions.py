import unittest

import pytest

import dionysus_app.class_registry_functions as class_registry_functions

from dionysus_app.class_registry_functions import (register_class,
                                                   check_registry_on_exit,
                                                   classlist_exists,
                                                   )


class TestLoadNonexistentRegistryWithNoClassData(unittest.TestCase):
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #
    # confirm blank registry created on startup when no data exists
    # confirm empty cached registry dict/global


class TestLoadExistingRegistry(unittest.TestCase):
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #     dummy class data (existent classes)
    #
    # confirm registry file created on startup
    # confirm registry dict/global created on startup
    # confirm created registry file has correct data
    # confirm created registry dict/global has correct data


class TestLoadNonexistentRegistryWithClassData:
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #     dummy class data (existent classes)
    #
    # confirm registry file created on startup
    # confirm registry dict/global created on startup
    # confirm created registry file has correct data


class TestAddClassToNewRegistry(unittest.TestCase):
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #     dummy classlist_name
    #
    # test add class to registry
    # confirm registry created
    # confirm classlist_name in cached registry dict
    # confirm classlist_name in registry file


class TestAddClassExistingRegistry(unittest.TestCase):
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #     dummy existing class registry
    #     dummy classlist_name
    #
    # test add class to registry
    # confirm classlist_name in cached registry dict
    # confirm classlist_name in registry file

class TestRegisterClass:
    # @pytest.mark.parametrize('mock_registry',
    #                          [(['a class', 'some_class', 'some_other_class']),
    #                           (['a class', 'some_other_class']),
    #                           ([]),
    #                           pytest.param(None, marks=pytest.mark.xfail),
    #                           ])
    # def test_register_class(mock_registry,
    #                         monkeypatch):
    #     pass


    def test_register_class_raising_error_uninitialised_registry(self, monkeypatch):
        monkeypatch.setattr(class_registry_functions.definitions, 'REGISTRY', None)
        with pytest.raises(ValueError):
            register_class('some_class')


class TestClasslistExists:
    @pytest.mark.parametrize('test_class_name, mock_registry, return_value',
                             [('some_class', ['a class', 'some_class', 'some_other_class'], True),
                              ('some_class', ['a class', 'some_other_class'], False),
                              ('some_class', [], False),
                              pytest.param('some_class', None, False, marks=pytest.mark.xfail),
                              ])
    def test_classlist_exists(self, test_class_name, mock_registry, return_value,
                              monkeypatch):
        monkeypatch.setattr(class_registry_functions.definitions, 'REGISTRY', mock_registry)
        assert classlist_exists(test_class_name) is return_value

    def test_classlist_exists_uninitialised_registry_raising_error(self, monkeypatch):
        # Registry is uninitialised.
        monkeypatch.setattr(class_registry_functions.definitions, 'REGISTRY', None)
        with pytest.raises(ValueError):
            classlist_exists('some_class')


class TestCheckRegistryOnExit:
    # @pytest.mark.parametrize('mock_registry',
    #                          [(['a class', 'some_class', 'some_other_class']),
    #                           (['a class', 'some_other_class']),
    #                           ([]),
    #                           pytest.param(None, marks=pytest.mark.xfail),
    #                           ])
    # def test_check_registry_on_exit(mock_registry,
    #                                 monkeypatch):
    #     pass


    def test_check_registry_on_exit_raising_error_uninitialised_registry(self, monkeypatch):
        monkeypatch.setattr(class_registry_functions.definitions, 'REGISTRY', None)
        with pytest.raises(ValueError):
            check_registry_on_exit()
