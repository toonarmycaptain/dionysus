"""Test Registry object for JSONDatabase."""
from pathlib import Path

import pytest

from dionysus_app.persistence.databases.json_registry import Registry


class TestCacheClassRegistry:
    @pytest.mark.parametrize('test_registry_list',
                             [[],  # ie empty list, no classes
                              ['one_class'],
                              ['mock_registry_list', 'contains multiple", "classes'],
                              ])
    def test_cache_class_registry(self, monkeypatch, tmpdir,
                                  test_registry_list):
        """
        Registry is cached from data on disk and written to registry.index.
        """
        test_registry = Registry()

        def mocked_write_registry_to_disk(registry_list):
            if registry_list is not test_registry_list:
                raise ValueError("List written is not list given/generated.")

        # Mock instance attributes/methods:
        test_registry.registry_path = Path(tmpdir, 'class_registry.index')
        test_registry.class_data_path = Path(tmpdir, 'test_APP_DATA/CLASS_DATA')
        test_registry.generate_registry_from_filesystem = lambda: test_registry_list
        # test_registry.generate_registry_from_filesystem = mocked_generate_registry_from_filesystem
        test_registry.write_registry_to_disk = mocked_write_registry_to_disk

        assert test_registry.cache_class_registry() == test_registry_list


class TestGenerateRegistryFromFilesystem:
    @pytest.mark.parametrize('test_registry_list',
                             [[],
                              ['test one class'],
                              ['test_class_1', 'test_class_2', 'test_class_4'],
                              ])
    def test_generate_registry_from_filesystem(self, tmpdir,
                                               test_registry_list):
        """Class data files are found and included in list."""
        # Create mock dir tree and class data files.
        test_class_data_path = Path(tmpdir, 'class_data')
        test_class_data_file_type = '.classlist_data_type'
        Path.mkdir(test_class_data_path)
        for class_name in test_registry_list:
            test_class_dir = test_class_data_path.joinpath(class_name)
            Path.mkdir(test_class_dir)
            test_class_path = Path.joinpath(test_class_dir, f'{class_name}{test_class_data_file_type}')
            with open(test_class_path, 'w') as test_class_data_file:
                test_class_data_file.write('some class data')
        # Create test registry, patch paths:
        test_registry = Registry()
        test_registry.class_data_path = test_class_data_path
        test_registry.class_data_file_type = test_class_data_file_type

        assert (test_registry.generate_registry_from_filesystem() == test_registry_list
                # Concession to occasional instance contents are equal but order is different, which is still ok.
                or sorted(test_registry.generate_registry_from_filesystem()) == sorted(test_registry_list))


class TestWriteRegistryToDisk:
    @pytest.mark.parametrize('test_registry_list',
                             [[],
                              ['test one class'],
                              ['test_class_1', 'test_class_2', 'test_class_4'],
                              ])
    def test_write_registry_to_disk(self, tmpdir,
                                    test_registry_list):
        """
        Write class names in list  followed by newlines with trailing newlines
        to registry location.
        """
        test_registry_path = Path(tmpdir, 'registry_file')
        test_registry = Registry()
        test_registry.registry_path = test_registry_path
        expected_registry_file = ''.join(f'{class_name}\n' for class_name in test_registry_list)

        test_registry.write_registry_to_disk(test_registry_list)
        assert open(test_registry_path).read() == expected_registry_file


class TestRegisterClass:
    @pytest.mark.parametrize('test_registry_list',
                             [[],
                              ['test one class'],
                              ['test_class_1', 'test_class_2', 'test_class_4'],
                              ])
    def test_register_class(self, monkeypatch, tmpdir,
                            test_registry_list):
        """New class added to registry list and file copy of registry."""
        test_class_name = 'Arthur_s Knights'

        test_registry_path = Path(tmpdir, 'registry_file')
        test_registry = Registry()
        test_registry.registry_path = test_registry_path
        test_registry.list = test_registry_list
        test_registry.write_registry_to_disk(test_registry_list)

        assert test_registry.register_class(test_class_name) is None
        # Class name in registry file:
        file_registry_str = open(test_registry.registry_path).readlines()
        assert f'{test_class_name}\n' in file_registry_str
        # Class name in cached registry:
        assert test_class_name in test_registry.list
        # Check existing classes still in registry.
        for class_name in test_registry_list:
            assert class_name in test_registry.list
            assert f'{class_name}\n' in file_registry_str

    def test_register_class_raising_error_uninitialised_registry(self, tmpdir):
        """None Registry.list throws error when adding class."""
        test_registry_path = Path(tmpdir, 'registry_file')
        test_registry = Registry()
        test_registry.registry_path = test_registry_path
        test_registry.list = None
        with pytest.raises(ValueError):
            test_registry.register_class('some_class')


class TestClasslistExists:
    @pytest.mark.parametrize('test_class_name, mock_registry, return_value',
                             [('some_class', ['a class', 'some_class', 'some_other_class'], True),
                              ('some_class', ['a class', 'some_other_class'], False),
                              ('some_class', [], False),
                              pytest.param('some_class', None, False, marks=pytest.mark.xfail),
                              ])
    def test_classlist_exists(self, monkeypatch,
                              mock_registry, test_class_name, return_value,
                              ):
        """Return whether class name is in registry."""
        test_registry = Registry()
        test_registry.list = mock_registry
        assert test_registry.classlist_exists(test_class_name) is return_value

    def test_classlist_exists_uninitialised_registry_raising_error(self, monkeypatch):
        """Registry uninitialised/None raises ValueError."""
        test_registry = Registry()
        # Registry is uninitialised.
        test_registry.list = None
        with pytest.raises(ValueError):
            test_registry.classlist_exists('some_class')


class TestCheckRegistryOnExit:
    @pytest.mark.parametrize(
        'test_registry_list, test_registry_file_str, registry_should_be_written_to_disk',
        # Correct registry file, not written to.
        [(['a class', 'some_class', 'some_other_class'], 'a class\nsome_class\nsome_other_class\n', False),
         (['a class', 'some_other_class'], 'a class\nsome_other_class\n', False),
         ([], '', False),
         # Incorrect disk registry - registry written to.
         (['a class', 'some_class', 'some_other_class'],
          'a class\nsome_class\nsome_other_class\nbut_with_an_extra_class\n', True),
         (['missing_a_class', 'some_other_class'], 'missing_a_class\n', True),
         (['extra_class', 'some_other_class'], 'extra_class\ninbetween\nsome_other_class\n', True),
         ([], 'there_is_an_extra_class_here\n', True),
         pytest.param(None, '', False, marks=pytest.mark.xfail),
         ])
    def test_check_registry_on_exit(self, tmpdir,
                                    test_registry_list, test_registry_file_str,
                                    registry_should_be_written_to_disk,
                                    ):
        """
        Registry file written to with cached registry if file copy does not match cached.
        """
        # Test sanity check: Registry list and file copy should be different if file is to be written to.
        assert (''.join(f'{class_name}\n' for class_name in test_registry_list) != test_registry_file_str
                ) is registry_should_be_written_to_disk

        test_registry_path = Path(tmpdir, 'mocked_registry')
        # Fake out registry file.
        with open(test_registry_path, 'w+') as test_registry_file:
            test_registry_file.write(test_registry_file_str)

        test_registry = Registry()
        test_registry.registry_path = test_registry_path
        test_registry.list = test_registry_list

        write_registry_to_disk_mock = {'called': False}

        def mocked_write_registry_to_disk(registry):
            write_registry_to_disk_mock['called'] = True
            if not registry_should_be_written_to_disk:
                raise ValueError("Registry file was correct, should not have been written to.")

        test_registry.write_registry_to_disk = mocked_write_registry_to_disk
        assert test_registry.check_registry_on_exit() is None
        # Ensure write_registry_to_disk is called when it should be.
        assert write_registry_to_disk_mock['called'] == registry_should_be_written_to_disk

    def test_check_registry_on_exit_raising_error_uninitialised_registry(self, monkeypatch):
        """Registry uninitialised/None raises ValueError."""
        test_registry = Registry()
        test_registry.list = None
        with pytest.raises(ValueError):
            test_registry.check_registry_on_exit()

    def test_check_registry_not_failing_on_no_registry_file(self, tmpdir):
        """Write registry to disk when no registry file exists."""
        test_registry_path = Path(tmpdir, 'registry_file')

        test_registry = Registry()
        test_registry.registry_path = test_registry_path
        test_registry.list = ['some', 'classes']

        write_registry_to_disk_mock = {'called': False}

        def mocked_write_registry_to_disk(registry):
            write_registry_to_disk_mock['called'] = True

        test_registry.write_registry_to_disk = mocked_write_registry_to_disk

        test_registry.check_registry_on_exit()
        assert write_registry_to_disk_mock['called']


class TestDel:
    def test__del__(self):
        """Registry dumped to disk on exit."""
        test_registry = Registry()

        check_registry_on_exit_mock = {'called': False}

        def mocked_check_registry_on_exit():
            check_registry_on_exit_mock['called'] = True

        test_registry.check_registry_on_exit = mocked_check_registry_on_exit

        test_registry.__del__()
        assert check_registry_on_exit_mock['called']
