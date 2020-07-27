import sqlite3

from random import randint

import pytest

from dionysus_app.class_ import Class, NewClass
from dionysus_app.persistence.database import ClassIdentifier
from dionysus_app.persistence.databases.sqlite import SQLiteDatabase

from test_suite.test_class import test_class_name_only, test_full_class  # Fixture imports.


def empty_sqlite_test_db(db_path):
    # give random db ref to avoid having to drop the tables and recreate each time....much faster!
    num = randint(1, 1000000000)
    # for some reason this didn't work on linux, but does on Win10.
    # return SQLiteDatabase(database_path=f'file:test_db{num}?mode=memory&cache=shared')
    # Slower, but cross platform:
    return SQLiteDatabase(database_path=f'{db_path}/test_db{num}')


@pytest.fixture
def empty_sqlite_database(tmpdir):
    """return in-RAM empty SQLiteDatabase.

    Basing in tmpdir works where basing in a 'file:' fails on linux,
    and also ensures test atomicity, each test starting with a fresh,
    empty database.
    """
    test_db = empty_sqlite_test_db(tmpdir)
    return test_db


def test_empty_sqlite_database_fixture(empty_sqlite_database):
    """Ensure test db can be connected to and tables exist."""
    assert empty_sqlite_database
    tables = ['class', 'student', 'chart', 'score']
    test_db_tables = empty_sqlite_database._connection().execute(
            """SELECT name from sqlite_master WHERE type='table' """).fetchall()
    for table in tables:
        assert (table,) in test_db_tables


class TestGetClasses:
    @pytest.mark.parametrize(
            'existing_class_names, returned_value',
            [([], []),
             (['one class'], [ClassIdentifier(id=1, name='one class')]
              ),
             (['one class', 'another'], [ClassIdentifier(id=1, name='one class'),
                                         ClassIdentifier(id=2, name='another')]),
             (['one class', 'another', 'so many'], [ClassIdentifier(id=1, name='one class'),
                                                    ClassIdentifier(id=2, name='another'),
                                                    ClassIdentifier(id=3, name='so many')]),
             pytest.param(['tricky'], ['tricky'], marks=pytest.mark.xfail(reason='Wrong format return value.')),
             pytest.param(['one class', 'another', 'so many'], [ClassIdentifier(id=1, name='one class'),
                                                                ClassIdentifier(id=2, name='another'),
                                                                ClassIdentifier(id=3, name='wrong')],
                          marks=pytest.mark.xfail(reason='Inconsistent class list.')),
             pytest.param(['one class', 'another', 'so many'], [ClassIdentifier(id=1, name='one class'),
                                                                ClassIdentifier(id=2, name='another'),
                                                                ClassIdentifier(id=3, name='so many'),
                                                                ClassIdentifier(id=4, name='wrong')],
                          marks=pytest.mark.xfail(reason='Inconsistent class list - extra class.')),
             pytest.param(['one class', 'another', 'so many'], [ClassIdentifier(id=1, name='one class'),
                                                                ClassIdentifier(id=2, name='another')],
                          marks=pytest.mark.xfail(reason='Inconsistent class list - missing class.')),
             ])
    def test_get_classes(self, empty_sqlite_database,
                         existing_class_names, returned_value):
        test_sqlite_database = empty_sqlite_database
        for class_name in existing_class_names:
            empty_sqlite_database.create_class(NewClass(name=class_name))

        assert test_sqlite_database.get_classes() == returned_value


class TestClassNameExists:
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
    def test_class_name_exists(self, empty_sqlite_database,
                               test_class_name, existing_class_names, returned_value):
        test_database = empty_sqlite_database
        for class_name in existing_class_names:
            test_database.create_class(NewClass(name=class_name))

        assert test_database.class_name_exists(test_class_name) == returned_value


class TestCreateClass:
    @pytest.mark.parametrize('class_data', ['test_class_name_only', 'test_full_class'])
    def test_create_class(self, request, empty_sqlite_database, class_data):
        test_database = empty_sqlite_database
        test_class_data = request.getfixturevalue(class_data)
        test_class = NewClass.from_dict(test_class_data.json_dict())

        # no students or class in empty db:
        assert not test_database._connection().cursor().execute("""SELECT * FROM class""").fetchall()
        assert not test_database._connection().cursor().execute("""SELECT * FROM student""").fetchall()

        # Create class in db:
        assert test_database.create_class(test_class) is None

        # Find class id, load class to verify:
        classes = test_database.get_classes()
        test_class_id = classes[0].id

        assert test_database.load_class(  # NB Returned object will be Class, not NewClass:
                test_class_id).json_dict() == Class.from_dict(test_class_data.json_dict()).json_dict()


class TestLoadClass:
    @pytest.mark.parametrize('class_data', ['test_class_name_only', 'test_full_class'])
    def test_create_class(self, request, empty_sqlite_database, class_data):
        test_database = empty_sqlite_database
        test_existing_class_data = request.getfixturevalue(class_data)
        test_existing_class = NewClass.from_dict(test_existing_class_data.json_dict())
        # Create class in db:
        test_database.create_class(test_existing_class)

        # Find class id to load:
        classes = test_database.get_classes()
        test_full_class_id = classes[0].id

        # Load class, verify data.
        assert test_database.load_class(  # NB Returned object will be Class, not NewClass:
                test_full_class_id).json_dict() == Class.from_dict(
                test_existing_class_data.json_dict()).json_dict()

        assert test_database._connection().cursor().execute("""SELECT * FROM class""").fetchall()
        if test_existing_class.students:
            assert test_database._connection().cursor().execute("""SELECT * FROM student""").fetchall()


class Test_Connection:
    def test__connection(self, empty_sqlite_database):
        """Connection function returns connection."""
        assert isinstance(empty_sqlite_database._connection(), sqlite3.Connection)
