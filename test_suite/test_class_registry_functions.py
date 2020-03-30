from pathlib import Path

import pytest

import definitions

from dionysus_app import class_registry_functions
from dionysus_app.class_registry_functions import (cache_class_registry,
                                                   check_registry_on_exit,
                                                   classlist_exists,
                                                   register_class,
                                                   )


class TestCacheClassRegistry:
    def test_cache_class_registry(self, monkeypatch):
        mock_registry_object = 'mock_registry_object'

        def mocked_generate_registry_from_filesystem():
            return mock_registry_object

        def mocked_write_registry_to_disk(registry):
            if registry != mock_registry_object:
                raise ValueError

        monkeypatch.setattr(class_registry_functions, 'generate_registry_from_filesystem',
                            mocked_generate_registry_from_filesystem)
        monkeypatch.setattr(class_registry_functions, 'write_registry_to_disk', mocked_write_registry_to_disk)

        assert cache_class_registry() == mock_registry_object

    def test_cache_class_registry_no_classes(self, monkeypatch, tmpdir):
        monkeypatch.setattr(class_registry_functions, 'CLASS_REGISTRY_PATH', Path(tmpdir, 'class_registry.index'))
        monkeypatch.setattr(class_registry_functions, 'CLASSLIST_DATA_PATH', Path(tmpdir, 'test_APP_DATA/CLASS_DATA'))
        # No class registry.
        assert not class_registry_functions.CLASS_REGISTRY_PATH.exists()

        assert cache_class_registry() == list()  # As opposed to None, this compares to empty list.
        assert class_registry_functions.CLASS_REGISTRY_PATH.exists()  # class_registry file is created.
        assert open(class_registry_functions.CLASS_REGISTRY_PATH, 'r').readlines() == list()  # Registry is empty list.

    def test_cache_class_registry_some_classes(self, monkeypatch, tmpdir):
        """This also tests existing registry where no classes exist, as """
        mock_registry_object = ['mock_registry_object', 'contains two class names']

        def mocked_generate_registry_from_filesystem():
            return mock_registry_object

        # def mocked_write_registry_to_disk(registry):
        #     if registry != mock_registry_object:
        #         raise ValueError

        monkeypatch.setattr(class_registry_functions, 'CLASS_REGISTRY_PATH', Path(tmpdir, 'class_registry.index'))
        monkeypatch.setattr(class_registry_functions, 'CLASSLIST_DATA_PATH', Path(tmpdir, 'test_APP_DATA/CLASS_DATA'))
        monkeypatch.setattr(class_registry_functions, 'generate_registry_from_filesystem',
                            mocked_generate_registry_from_filesystem)
        # monkeypatch.setattr(class_registry_functions, 'write_registry_to_disk', mocked_write_registry_to_disk)

        assert cache_class_registry() == mock_registry_object  # As opposed to None, this compares to empty list.
        assert class_registry_functions.CLASS_REGISTRY_PATH.exists()  # class_registry file is created.
        # Number of classes is same as mock object.
        assert len(open(class_registry_functions.CLASS_REGISTRY_PATH, 'r').readlines()) == len(mock_registry_object)


class TestRegisterClass:
    def test_register_class(self, monkeypatch, tmpdir):
        test_class_name = 'Arthur_s Knights'
        monkeypatch.setattr(class_registry_functions, 'CLASS_REGISTRY_PATH', Path(tmpdir, 'class_registry.index'))
        monkeypatch.setattr(definitions, 'REGISTRY', [])

        assert register_class(test_class_name) is None
        # Class name in registry file:
        assert f'{test_class_name}\n' in open(class_registry_functions.CLASS_REGISTRY_PATH).readlines()
        # Class name in cached registry:
        assert test_class_name in definitions.REGISTRY

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
    @pytest.mark.parametrize('mock_registry',
                             [(['a class', 'some_class', 'some_other_class']),
                              (['a class', 'some_other_class']),
                              ([]),
                              pytest.param(None, marks=pytest.mark.xfail),
                              ])
    def test_check_registry_on_exit_writing_registry(self, monkeypatch, tmpdir,
                                                     mock_registry,
                                                     ):
        mocked_class_registry_path = Path(tmpdir, 'mocked_registry')

        def mocked_write_registry_to_disk(registry):
            if registry != mock_registry:
                raise ValueError("Registry written incorrectly.")

        monkeypatch.setattr(class_registry_functions, 'write_registry_to_disk', mocked_write_registry_to_disk)
        monkeypatch.setattr(class_registry_functions.definitions, 'REGISTRY', mock_registry)
        monkeypatch.setattr(class_registry_functions, 'CLASS_REGISTRY_PATH', mocked_class_registry_path)

        assert check_registry_on_exit()

    @pytest.mark.parametrize('mock_registry',
                             [(['a class', 'some_class', 'some_other_class']),
                              (['a class', 'some_other_class']),
                              ([]),
                              pytest.param(None, marks=pytest.mark.xfail),
                              ])
    def test_check_registry_on_exit_writing_registry(self, monkeypatch, tmpdir,
                                                     mock_registry,
                                                     ):
        mocked_class_registry_path = Path(tmpdir, 'mock_registry')

        with open(mocked_class_registry_path, 'w') as mock_registry_file:
            mock_registry_file.write('definitely not a correct registry!')

        monkeypatch.setattr(class_registry_functions.definitions, 'REGISTRY', mock_registry)
        monkeypatch.setattr(class_registry_functions, 'CLASS_REGISTRY_PATH', mocked_class_registry_path)

        assert check_registry_on_exit() is None

        assert open(mocked_class_registry_path).readlines() == [f'{classname}\n' for classname in mock_registry]

    def test_check_registry_on_exit_raising_error_uninitialised_registry(self, monkeypatch):
        monkeypatch.setattr(class_registry_functions.definitions, 'REGISTRY', None)
        with pytest.raises(ValueError):
            check_registry_on_exit()
