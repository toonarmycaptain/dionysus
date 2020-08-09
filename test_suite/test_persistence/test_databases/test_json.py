""" Test json and JSONDatabase"""

# Test  per-API then backend specific methods
# -> Test API for all databases in test_database.py, passing in each database type using parametrize?

import pytest

from pathlib import Path

from dionysus_app.class_ import Class, NewClass
from dionysus_app.persistence.database import ClassIdentifier
from dionysus_app.persistence.databases import json
from dionysus_app.persistence.databases.json import JSONDatabase
from dionysus_app.student import Student

from test_suite.test_class import test_full_class  # fixture
from test_suite.testing_class_data import (testing_registry_data_set as test_registry_data_set,
                                           test_full_class_data_set,
                                           )


def empty_json_test_db(path):
    return JSONDatabase(app_data_path=Path(path, 'app_data'),
                        class_data_path=Path(path, 'app_data', 'class_data'),
                        registry_path=Path(path, 'app_data', 'test_registry_file'),
                        default_chart_save_dir=Path(path, 'default_chart_save_dir'))


@pytest.fixture
def empty_json_database(tmpdir):
    """Return an empty JSONDatabase stored in tmpdir."""
    return empty_json_test_db(tmpdir)


# Database API tests:

class TestGetClasses:
    @pytest.mark.parametrize(
        'registry_list, returned_value',
        [([], []),
         (['one class'], [ClassIdentifier(id='one class', name='one class')]
          ),
         (['one class', 'another'], [ClassIdentifier(id='one class', name='one class'),
                                     ClassIdentifier(id='another', name='another')]),
         (['one class', 'another', 'so many'], [ClassIdentifier(id='one class', name='one class'),
                                                ClassIdentifier(id='another', name='another'),
                                                ClassIdentifier(id='so many', name='so many')]),
         pytest.param(['tricky'], ['tricky'], marks=pytest.mark.xfail(reason='Wrong format return value.')),
         pytest.param(['one class', 'another', 'so many'], [ClassIdentifier(id='one class', name='one class'),
                                                            ClassIdentifier(id='another', name='another'),
                                                            ClassIdentifier(id='wrong', name='wrong')],
                      marks=pytest.mark.xfail(reason='Inconsistent class list.')),
         pytest.param(['one class', 'another', 'so many'], [ClassIdentifier(id='one class', name='one class'),
                                                            ClassIdentifier(id='another', name='another'),
                                                            ClassIdentifier(id='so many', name='so many'),
                                                            ClassIdentifier(id='wrong', name='wrong')],
                      marks=pytest.mark.xfail(reason='Inconsistent class list - extra class.')),
         pytest.param(['one class', 'another', 'so many'], [ClassIdentifier(id='one class', name='one class'),
                                                            ClassIdentifier(id='another', name='another')],
                      marks=pytest.mark.xfail(reason='Inconsistent class list - missing class.')),
         ])
    def test_get_classes(self, empty_json_database,
                         registry_list, returned_value):
        test_json_database = empty_json_database
        empty_json_database._registry.list = registry_list

        assert test_json_database.get_classes() == returned_value


class TestClassNameExists:
    @pytest.mark.parametrize(
        'test_class_name, registry_list, returned_value',
        [('one class', ['one class'], True),
         ('one class', ['one class', 'another'], True),
         ('one class', ['one class', 'another', 'so many'], True),
         ('nonexistent class', [], False),
         ('nonexistent class', ['one class'], False),
         ('nonexistent class', ['one class', 'another'], False),
         ('nonexistent class', ['one class', 'another', 'so many'], False),
         pytest.param('one class', [], True,
                      marks=pytest.mark.xfail(reason='Class does not actually exist.')),
         pytest.param('one class', ['tricky'], True,
                      marks=pytest.mark.xfail(reason='Class does not actually exist.')),
         pytest.param('one_class', ['one_class'], False,
                      marks=pytest.mark.xfail(reason='Class does exist.')),
         ])
    def test_class_name_exists(self, empty_json_database,
                               test_class_name, registry_list, returned_value):
        test_json_database = empty_json_database
        test_json_database._registry.list = registry_list

        assert test_json_database.class_name_exists(test_class_name) == returned_value


class TestCreateClass:
    def test_create_class(self, empty_json_database, test_full_class):
        """JSON's create_class delegates calls to appropriate methods."""
        test_json_database = empty_json_database
        _setup_class_mock, _write_classlist_to_file_mock, _copy_avatars_to_class_data_mock = (
            {'called': False}, {'called': False}, {'called': False})

        def mocked__setup_class(test_class_name):
            _setup_class_mock['called'] = True
            if test_class_name != test_full_class.name:
                raise ValueError

        def mocked__write_classlist_to_file(test_class):
            _write_classlist_to_file_mock['called'] = True
            if test_class != test_full_class:
                raise ValueError

        def mocked__copy_avatars_to_class_data(test_class):
            _copy_avatars_to_class_data_mock['called'] = True
            if test_class != test_full_class:
                raise ValueError

        test_json_database._setup_class = mocked__setup_class
        test_json_database._write_classlist_to_file = mocked__write_classlist_to_file
        test_json_database._move_avatars_to_class_data = mocked__copy_avatars_to_class_data

        assert test_json_database.create_class(test_full_class) is None
        assert all([_setup_class_mock['called'],
                    _write_classlist_to_file_mock['called'],
                    _copy_avatars_to_class_data_mock['called']])


class TestLoadClass:
    def test_load_class(self, monkeypatch, empty_json_database, test_full_class):
        test_json_database = empty_json_database
        test_class_name = 'my_test_class'

        def mock_from_file(class_path):
            assert class_path == Path(test_json_database.class_data_path,
                                      test_class_name,
                                      f'{test_class_name}{test_json_database.class_data_file_type}')
            return test_full_class

        monkeypatch.setattr(json.Class, 'from_file', mock_from_file)
        assert test_json_database.load_class(test_class_name).json_dict() == test_full_class.json_dict()


class TestUpdateClass:
    def test_update_class(self, empty_json_database, test_full_class):
        test_json_database = empty_json_database
        test_class = Class(test_full_class.name, test_full_class.students)
        # create_class takes a NewClass object due to avatar moving machinery.
        test_class_new_class = NewClass(test_full_class.name, test_full_class.students)
        assert test_class.json_dict() == test_class_new_class.json_dict()  # Ensure classes are the same.

        # Create class in database.
        test_json_database.create_class(NewClass(test_full_class.name, test_full_class.students))
        # Ensure test_class in database
        test_class.id = test_class.name
        assert test_json_database.load_class(test_class.name).json_dict() == test_class.json_dict()

        # Change class by adding student, update database:
        new_student = Student(name='new student')
        assert new_student not in test_class and new_student.name not in test_class  # Confirm student not in class.
        test_class.add_student(new_student)

        assert test_json_database.update_class(test_class) is None
        # Look up name because new_student object itself is not in the loaded class object.
        assert new_student.name in test_json_database.load_class(test_class.name)


class TestCreateChart:
    def test_create_chart(self, monkeypatch, tmp_path, empty_json_database):
        test_chart_data_dict = {'class_id': 'test_class_name',
                                'class_name': 'test_class_name',
                                'chart_name': 'test_chart_name',
                                'chart_default_filename': 'test_default_chart_filename',
                                'chart_params': {'some': 'params'},
                                'score-avatar_dict': {'score': 'some student avatar paths'}
                                }
        test_filename = test_chart_data_dict['chart_default_filename'] + empty_json_database.chart_data_file_type
        test_file_folder = tmp_path.joinpath(test_chart_data_dict['class_name'], 'chart_data')
        test_file_folder.mkdir(parents=True, exist_ok=True)
        test_filepath = test_file_folder.joinpath(test_filename)

        test_text_written_to_file = 'A JSON string.'

        assert tmp_path.exists()
        assert test_file_folder.exists()

        def mocked__sanitise_avatar_path_objects(file_chart_data_dict):
            if file_chart_data_dict != test_chart_data_dict:
                raise ValueError('The dict of chart data did not contain expected items.')
            # file_chart_data_dict should be a deepcopy, not a reference to the original chart_data_dict.
            if file_chart_data_dict is test_chart_data_dict:
                raise ValueError("A reference to the original chart data dict was passed. \n"
                                 "An exact (deep)copy should be passed, because sanitise_avatar_path_objects \n"
                                 "will mutate ('sanitise') the dict passed to it.\n")

            return file_chart_data_dict

        def mocked_convert_to_json(json_safe_dict):
            if json_safe_dict != test_chart_data_dict:
                raise ValueError
            return test_text_written_to_file

        monkeypatch.setattr(json, 'convert_to_json', mocked_convert_to_json)

        test_json_database = empty_json_database
        test_json_database.class_data_path = tmp_path
        test_json_database._sanitise_avatar_path_objects = mocked__sanitise_avatar_path_objects

        test_json_database.create_chart(test_chart_data_dict)

        assert test_filepath.exists()
        with open(test_filepath, 'r') as test_file:
            assert test_file.read() == test_text_written_to_file


class TestSaveChartImage:
    def test_save_chart_image(self, empty_json_database):
        test_json_database = empty_json_database

        class MockMplPlt:
            def savefig(self, app_data_save_pathname, dpi):
                assert app_data_save_pathname == test_image_save_path
                assert dpi == 120

        mocked_mpl_plt = MockMplPlt()

        test_data_dict = {
            'class_id': 'test_class_name',
            'class_name': "test_class_name",
            'chart_name': "test_chart_name",
            'chart_default_filename': "test_chart_default_filename",
            'chart_params': {"some": "chart", "default": "params"},
            'score-avatar_dict': {0: [Path('path to Cali_avatar.png')],
                                  1: [test_json_database.default_avatar_path,
                                      test_json_database.default_avatar_path],
                                  3: [test_json_database.default_avatar_path,
                                      test_json_database.default_avatar_path],
                                  50: [test_json_database.default_avatar_path],
                                  99: [test_json_database.default_avatar_path],
                                  100: [test_json_database.default_avatar_path],
                                  2: [Path('path to Ashley_avatar.png')],
                                  4: [test_json_database.default_avatar_path],
                                  6: [Path('path to Danielle.png'), test_json_database.default_avatar_path],
                                  7: [test_json_database.default_avatar_path],
                                  8: [test_json_database.default_avatar_path]
                                  },
            }

        test_image_save_path = test_json_database.class_data_path.joinpath(
            test_data_dict['class_name'],
            'chart_data',
            f"{test_data_dict['chart_default_filename']}.png")

        assert test_json_database.save_chart_image(test_data_dict, mocked_mpl_plt) == test_image_save_path
        # Ensure dir to save image in exists, as not actually saving an image.
        assert test_image_save_path.parent.exists()


class TestGetAvatarPath:
    def test_get_avatar_path(self, empty_json_database):
        test_json_database = empty_json_database
        with pytest.raises(NotImplementedError):
            test_json_database.get_avatar_path(12345)


class TestGetAvatarPathClassFilename:
    @pytest.mark.parametrize('test_student_avatar', ['some avatar', None])
    def test_get_avatar_path_class_filename(self, empty_json_database,
                                            test_student_avatar):
        """Returns existent avatar path, else db.default_avatar_path."""

        def mocked__avatar_path_from_string(class_name, student_avatar_filename):
            if not test_student_avatar:
                raise ValueError('Should not be called as not avatar to get abs path for.')
            return test_student_avatar

        test_json_database = empty_json_database
        test_json_database.default_avatar_path = 'path to a default avatar'
        test_json_database._avatar_path_from_string = mocked__avatar_path_from_string

        assert test_json_database.get_avatar_path_class_filename(
            'some class', test_student_avatar) == (test_student_avatar if test_student_avatar
                                                   else test_json_database.default_avatar_path)


class TestAvatarPathFromString:
    def test__avatar_path_from_string(self, empty_json_database):
        """Returns abs avatar path."""
        test_json_database = empty_json_database

        test_class_name = 'a test class'
        test_avatar_filename = 'some filename'
        test_avatar_path = test_json_database.class_data_path.joinpath(test_class_name,
                                                                       'avatars',
                                                                       test_avatar_filename)

        assert test_json_database._avatar_path_from_string(
            test_class_name, test_avatar_filename) == test_avatar_path


class TestClose:
    def test_close(self, empty_json_database):
        _registry_check_registry_on_exit_mock = {'called': False}

        def mock__registry_check_registry_on_exit():
            _registry_check_registry_on_exit_mock['called'] = True

        test_json_database = empty_json_database
        test_json_database._registry.check_registry_on_exit = mock__registry_check_registry_on_exit

        test_json_database.close()
        assert _registry_check_registry_on_exit_mock['called']


# Database backend specific tests:


class TestSetupClass:
    def test__setup_class(self, empty_json_database):
        """Class data folders and entry in registry created."""
        test_classlist_name = 'the_knights_who_say_ni'
        test_json_database = empty_json_database

        _setup_class_data_storage_mock, registry_register_class_mock = {'called': False}, {'called': False}

        def mock__setup_class_data_storage(class_name):
            _setup_class_data_storage_mock['called'] = True
            if class_name != test_classlist_name:
                raise ValueError

        def mock_registry_register_class(class_name):
            registry_register_class_mock['called'] = True
            if class_name != test_classlist_name:
                raise ValueError

        test_json_database._setup_class_data_storage = mock__setup_class_data_storage
        test_json_database._registry.register_class = mock_registry_register_class

        assert test_json_database._setup_class(test_classlist_name) is None
        assert _setup_class_data_storage_mock['called']
        assert registry_register_class_mock['called']


class TestSetupClassDataStorage:
    def test_setup_class_data_storage(self, empty_json_database):
        """Class data directories created."""
        test_class_name = 'the_knights_who_say_ni'
        test_json_database = empty_json_database

        assert test_json_database._setup_class_data_storage(test_class_name) is None

        assert test_json_database.class_data_path.joinpath(test_class_name, 'avatars').exists()
        assert test_json_database.class_data_path.joinpath(test_class_name, 'chart_data').exists()
        assert test_json_database.default_chart_save_dir.joinpath(test_class_name).exists()

    def test_setup_class_data_storage_raising_error(self, empty_json_database):
        """Error thrown on uninitialised default_chart_save_dir value."""
        test_json_database = empty_json_database
        test_json_database.default_chart_save_dir = None
        with pytest.raises(ValueError):
            test_json_database._setup_class_data_storage('some_class')


class TestWriteClasslistToFile:
    def test_write_classlist_to_file(self, empty_json_database, test_full_class):
        test_json_database = empty_json_database
        test_class_data_file_path = Path(test_json_database.class_data_path,
                                         test_full_class.name,
                                         f'{test_full_class.name}{test_json_database.class_data_file_type}')
        # Assert class data file doesn't exist:
        assert not test_class_data_file_path.exists()

        assert test_json_database._write_classlist_to_file(test_full_class) is None

        # Assert file created:
        assert test_class_data_file_path.exists()
        # Verify file contents:
        with open(test_class_data_file_path, 'r') as test_class_data_file:
            assert test_class_data_file.read() == test_full_class.to_json_str()


class TestMoveAvatarsToClassData:
    @pytest.mark.parametrize(
        'test_new_class, expected_moved_avatars',
        [(NewClass('test empty class'), []),  # No students
         # All students have avatar_id
         (NewClass.from_dict({'name': 'test_class',
                              'students': [{'name': 'Cali', 'avatar_id': 'Cali_avatar.png'},
                                           {'name': 'Zach', 'avatar_id': 'Zach_avatar.png'},
                                           {'name': 'Ashley', 'avatar_id': 'Ashley_avatar.png'},
                                           {'name': 'Danielle', 'avatar_id': 'Danielle.png'}, ]
                              }),
          ['Cali_avatar.png',
           'Zach_avatar.png',
           'Ashley_avatar.png',
           'Danielle.png',
           ]),
         # Some students have avatar_id
         (NewClass.from_dict(test_full_class_data_set['json_dict_rep']), ['Cali_avatar.png',
                                                                          'Zach_avatar.png',
                                                                          'Ashley_avatar.png',
                                                                          'Danielle.png',
                                                                          ]
          ),
         # No students have avatar_id
         (NewClass.from_dict({'name': 'test_class',
                              'students': [{'name': 'Cali'},
                                           {'name': 'Zach'},
                                           {'name': 'Ashley'},
                                           {'name': 'Danielle'}, ]
                              }),
          []),
         ])
    def test_move_avatars_to_class_data(self, empty_json_database,
                                        test_new_class, expected_moved_avatars):
        """Avatar files copied from original locations to class data."""
        test_json_database = empty_json_database
        moved_avatars = []

        def mock_move_avatar_to_class_data(test_class: NewClass, avatar_filename: str):
            assert test_class is test_new_class
            moved_avatars.append(avatar_filename)

        empty_json_database._move_avatar_to_class_data = mock_move_avatar_to_class_data

        assert test_json_database._move_avatars_to_class_data(test_new_class) is None
        assert moved_avatars == expected_moved_avatars


class TestMoveAvatarToClassData:
    def test_move_avatar_to_class_data(self, monkeypatch, empty_json_database):
        """Avatar moved from original location to class data."""
        test_class = NewClass('test_class')
        test_class.id = test_class.name  # Set NewClass id to save in db.
        test_filename = 'test avatar filename'
        test_json_database = empty_json_database

        def mock_move_file(origin_path: Path, destination_path: Path):
            if origin_path != test_class.temp_dir.joinpath('avatars', test_filename):
                raise ValueError("Origin path incorrect.")
            if destination_path != test_json_database.class_data_path.joinpath(test_class.name, 'avatars',
                                                                               test_filename):
                raise ValueError("Destination path incorrect")

        monkeypatch.setattr(json, 'move_file', mock_move_file)

        assert test_json_database._move_avatar_to_class_data(test_class, test_filename) is None

    def test_move_avatar_to_class_data_avatar_preexisting(self, monkeypatch, empty_json_database):
        """No attempt to move avatar that already exists in class_data."""
        test_class = NewClass('test_class')
        test_class.id = test_class.name  # Set NewClass id to save in db.
        test_json_database = empty_json_database
        # Make existing avatar in tmpdir test_class class data:
        destination_avatar_path = test_json_database.class_data_path.joinpath(
            test_class.name, 'avatars', 'test_avatar_filename')
        Path.mkdir(destination_avatar_path.parent, parents=True)
        with open(destination_avatar_path, 'w'):
            pass

        def mock_move_file(origin_path: Path, destination_path: Path):
            raise ValueError("Move file should not be called.")

        monkeypatch.setattr(json, 'move_file', mock_move_file)

        assert test_json_database._move_avatar_to_class_data(test_class, destination_avatar_path.name) is None


class TestSanitiseAvatarPathObjects:
    def test_santise_avatar_path_objects(self, empty_json_database):
        test_json_database = empty_json_database
        test_json_database.default_avatar_path = Path('default/path')

        test_data_dict = {
            'class_name': "test_class_name",
            'chart_name': "test_chart_name",
            'chart_default_filename': "test_chart_default_filename",
            'chart_params': {"some": "chart", "default": "params"},
            'score-avatar_dict': {0: [Path('path to Cali_avatar.png')],
                                  1: [test_json_database.default_avatar_path,
                                      test_json_database.default_avatar_path],
                                  3: [test_json_database.default_avatar_path,
                                      test_json_database.default_avatar_path],
                                  50: [test_json_database.default_avatar_path],
                                  99: [test_json_database.default_avatar_path],
                                  100: [test_json_database.default_avatar_path],
                                  2: [Path('path to Ashley_avatar.png')],
                                  4: [test_json_database.default_avatar_path],
                                  6: [Path('path to Danielle.png'), test_json_database.default_avatar_path],
                                  7: [test_json_database.default_avatar_path],
                                  8: [test_json_database.default_avatar_path]
                                  },
            }
        test_returned_sanitised_data_dict = {
            'class_name': "test_class_name",
            'chart_name': "test_chart_name",
            'chart_default_filename': "test_chart_default_filename",
            'chart_params': {"some": "chart", "default": "params"},
            'score-avatar_dict': {0: ['path to Cali_avatar.png'],
                                  1: [str(test_json_database.default_avatar_path),
                                      str(test_json_database.default_avatar_path)],
                                  3: [str(test_json_database.default_avatar_path),
                                      str(test_json_database.default_avatar_path)],
                                  50: [str(test_json_database.default_avatar_path)],
                                  99: [str(test_json_database.default_avatar_path)],
                                  100: [str(test_json_database.default_avatar_path)],
                                  2: ['path to Ashley_avatar.png'],
                                  4: [str(test_json_database.default_avatar_path)],
                                  6: ['path to Danielle.png', str(test_json_database.default_avatar_path)],
                                  7: [str(test_json_database.default_avatar_path)],
                                  8: [str(test_json_database.default_avatar_path)]
                                  },
            }

        assert test_json_database._sanitise_avatar_path_objects(test_data_dict) == test_returned_sanitised_data_dict
