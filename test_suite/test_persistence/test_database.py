""" Test Database abstract base class """
# Subclass and test that class errors when trying to instantiate subclass without implementing each function.
import abc

import pytest

from pathlib import Path
from typing import List

import matplotlib.pyplot as plt

from dionysus_app.class_ import Class, NewClass
from dionysus_app.persistence.database import (ABCMetaEnforcedAttrs,
                                               ClassIdentifier,
                                               Database,
                                               )
from dionysus_app.persistence.databases.json import JSONDatabase
from dionysus_app.student import Student
# Import test database fixtures:
from test_suite.test_class import test_class_name_only, test_full_class
from test_suite.test_persistence.test_databases.test_json import empty_json_database
from test_suite.test_persistence.test_databases.test_sqlite import empty_sqlite_database


class EmptyGenericDatabase(Database):
    """
    Generic database object without defined methods.

    Required attribute default_avatar_path instantiated to None.

    Replace methods if behaviour is desired.
    """

    def __init__(self):
        super().__init__()
        self.default_avatar_path: Path = None

    def get_classes(self) -> List[ClassIdentifier]:
        raise NotImplementedError

    def class_name_exists(self, class_name: str) -> bool:
        raise NotImplementedError

    def create_class(self, new_class: NewClass) -> None:
        raise NotImplementedError

    def load_class(self, class_id: int) -> Class:
        raise NotImplementedError

    def update_class(self, class_to_write: Class) -> None:
        raise NotImplementedError

    def get_avatar_path(self, avatar_id: int):
        raise NotImplementedError

    def create_chart(self, chart_data_dict: dict) -> None:
        raise NotImplementedError

    def save_chart_image(self, chart_data_dict: dict, mpl_plt: plt) -> Path:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


@pytest.fixture
def empty_generic_database():
    return EmptyGenericDatabase()


class TestDatabaseRequiredAttrs:
    @pytest.mark.parametrize('has_required_attrs', [True, False])
    def test_required_attrs_not_present_raising_error(self, has_required_attrs):
        """Do not instantiate subclass without required attrs."""

        class SubclassRequiresAttrs(abc.ABC, metaclass=ABCMetaEnforcedAttrs):
            required_attributes = ['some_required_attr']

        class Subclass(SubclassRequiresAttrs):
            def __init__(self):
                if has_required_attrs:
                    self.some_required_attr = 'present'

        if has_required_attrs:  # Ensure able to instantiate with required attrs:
            Subclass()
        if not has_required_attrs:
            with pytest.raises(TypeError):
                Subclass()


class TestGetClasses:
    @pytest.mark.parametrize('database_backend', ['empty_json_database',
                                                  'empty_sqlite_database',
                                                  ])
    @pytest.mark.parametrize(
        'existing_class_names, returned_id_names',
        [([], []),
         (['one class'], ['one class']),
         (['one class', 'another'], ['one class', 'another']),
         (['one class', 'another', 'so many'], ['one class', 'another', 'so many']),
         pytest.param(['one class', 'another', 'so many'], ['one class', 'another', 'wrong'],
                      marks=pytest.mark.xfail(reason='Inconsistent class list.')),
         pytest.param(['one class', 'another', 'so many'], ['one class', 'another', 'so many', 'wrong'],
                      marks=pytest.mark.xfail(reason='Inconsistent class list - extra class.')),
         pytest.param(['one class', 'another', 'so many'], ['one class', 'another'],
                      marks=pytest.mark.xfail(reason='Inconsistent class list - missing class.')),
         ])
    def test_get_classes(self, request, database_backend,
                         existing_class_names, returned_id_names):
        test_database = request.getfixturevalue(database_backend)
        for class_name in existing_class_names:
            test_database.create_class(NewClass(name=class_name))

        retrieved_class_identifiers = test_database.get_classes()
        # class_identifier.id will be different for each backend, but the names will be the same.
        assert [class_id.name for class_id in retrieved_class_identifiers] == returned_id_names


class TestClassNameExists:
    @pytest.mark.parametrize('database_backend', ['empty_json_database',
                                                  'empty_sqlite_database',
                                                  ])
    @pytest.mark.parametrize(
        'test_class_name, existing_class_names, returned_value',
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
    def test_class_name_exists(self, request, database_backend,
                               test_class_name, existing_class_names, returned_value):
        test_database = request.getfixturevalue(database_backend)
        for class_name in existing_class_names:
            test_database.create_class(NewClass(name=class_name))

        assert test_database.class_name_exists(test_class_name) == returned_value


class TestCreateClass:
    @pytest.mark.parametrize('database_backend', ['empty_json_database',
                                                  'empty_sqlite_database',
                                                  ])
    @pytest.mark.parametrize('class_data', ['test_class_name_only', 'test_full_class'])
    def test_create_class(self, request, database_backend, class_data):
        test_database = request.getfixturevalue(database_backend)
        test_class = request.getfixturevalue(class_data)
        # Create test NewClass object, mocking avatar_files.
        test_class = NewClass.from_dict(test_class.json_dict())
        for student in test_class:
            if student.avatar_id:
                Path(test_class.temp_avatars_dir, student.avatar_id).write_text(student.avatar_id)

        # Assure no classes in db:
        assert not test_database.get_classes()

        # Create class in db:
        assert test_database.create_class(test_class) is None

        # Find class id, load class to verify:
        classes = test_database.get_classes()
        existing_class_id = classes[0].id  # As the only class will be first item.

        # Loaded class will have ids:
        test_saved_class_with_student_ids = Class.from_dict(test_class.json_dict())
        if isinstance(test_database, JSONDatabase):
            for student in test_saved_class_with_student_ids.students:
                student.id = student.name
        if not isinstance(test_database, JSONDatabase):
            for test_id, student in enumerate(test_saved_class_with_student_ids.students, start=1):
                student.id = test_id

        assert test_database.load_class(
            existing_class_id).json_dict() == test_saved_class_with_student_ids.json_dict()


class TestLoadClass:
    @pytest.mark.parametrize('database_backend', ['empty_json_database',
                                                  'empty_sqlite_database',
                                                  ])
    @pytest.mark.parametrize('class_data', ['test_class_name_only', 'test_full_class'])
    def test_load_class(self, request, database_backend, class_data):
        """JSON's create_class delegates calls to appropriate methods."""
        test_database = request.getfixturevalue(database_backend)
        preexisting_class = request.getfixturevalue(class_data)
        # Create test NewClass object, mocking avatar_files.
        preexisting_class = NewClass.from_dict(preexisting_class.json_dict())
        for student in preexisting_class:
            if student.avatar_id:
                Path(preexisting_class.temp_avatars_dir, student.avatar_id).write_text(student.avatar_id)
        # Create class in db:
        test_database.create_class(preexisting_class)

        # Find class id, load class to verify:
        classes = test_database.get_classes()
        test_full_class_id = classes[0].id  # As the only class will be first item.

        # Loaded class will have ids:
        test_loaded_class_with_student_ids = Class.from_dict(preexisting_class.json_dict())
        if isinstance(test_database, JSONDatabase):
            for student in test_loaded_class_with_student_ids.students:
                student.id = student.name
        if not isinstance(test_database, JSONDatabase):
            for test_id, student in enumerate(test_loaded_class_with_student_ids.students, start=1):
                student.id = test_id

        assert test_database.load_class(
            test_full_class_id).json_dict() == test_loaded_class_with_student_ids.json_dict()


class TestUpdateClass:
    """Not tested as method is unused and mostly unimplemented."""


class TestGetAvatarPath:
    @pytest.mark.parametrize(
        'database_backend',
        [pytest.param('empty_json_database', marks=pytest.mark.xfail(
            reason='JSON db does not implement method.')),
         'empty_sqlite_database',
         ])
    @pytest.mark.parametrize('avatar_provided',
                             [pytest.param(True, id='avatar provided'),
                              pytest.param(False, id='no avatar provided'),
                              ])
    def test_get_avatar_path(self, tmpdir, request, database_backend, avatar_provided):
        """"""
        test_database = request.getfixturevalue(database_backend)

        # Create avatar:
        test_avatar_data = b'some binary data'
        test_avatar_path = Path(tmpdir, 'test_avatar.png')
        test_avatar_path.write_bytes(test_avatar_data)
        # Add avatar to db:
        test_class = NewClass(name='test class',
                              students=[
                                  Student(name='test_student',
                                          avatar_id=(test_avatar_path if avatar_provided else None),
                                          )
                                  ])
        test_database.create_class(test_class)

        # Find avatar_id, load class to verify:
        classes = test_database.get_classes()
        test_class_id = classes[0].id  # As the only class will be first item.
        loaded_test_class = test_database.load_class(test_class_id)
        test_avatar_id = loaded_test_class.students[0].avatar_id

        # Path may be different/random - test data:
        assert test_database.get_avatar_path(test_avatar_id).read_bytes() == (
            test_avatar_data if avatar_provided
            else test_database.default_avatar_path.read_bytes())


class TestCreateChart:
    @pytest.mark.parametrize('database_backend', ['empty_json_database',
                                                  'empty_sqlite_database',
                                                  ])
    def test_create_chart(self, request, database_backend):
        """
        Verify API works.

        NB No verification in API test, as API for verifying does not exist.
        TODO: Verify saved chart contents when load/edit features added.
        """
        test_database = request.getfixturevalue(database_backend)
        test_class = NewClass(name='test_class', students=[Student(name='bad student'),
                                                           Student(name='mediocre student'),
                                                           Student(name='excellent student'),
                                                           ])
        test_database.create_class(test_class)

        test_chart_data_dict = {'class_id': test_class.id,
                                'class_name': test_class.name,
                                'chart_name': 'test_chart_name',
                                'chart_default_filename': 'test_default_chart_filename',
                                'chart_params': {'some': 'params'},
                                'score-students_dict': {0: [test_class.students[0]],
                                                        50: [test_class.students[1]],
                                                        100: [test_class.students[2]],
                                                        }
                                }

        assert test_database.create_chart(test_chart_data_dict) is None
