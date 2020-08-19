import sqlite3

from pathlib import Path
from random import randint

import pytest

from dionysus_app.class_ import Class, NewClass
from dionysus_app.persistence.database import ClassIdentifier
from dionysus_app.persistence.databases.sqlite import SQLiteDatabase
from dionysus_app.student import Student

from test_suite.test_class import test_class_name_only, test_full_class  # Fixture imports.


def empty_sqlite_test_db(db_path):
    # give random db ref to avoid having to drop the tables and recreate each time....much faster!
    num = randint(1, 1000000000)
    # for some reason this didn't work on linux, but does on Win10.
    # return SQLiteDatabase(database_path=f'file:test_db{num}?mode=memory&cache=shared')
    # Slower, but cross platform:
    return SQLiteDatabase(database_path=Path(db_path, f'test_db{num}'))


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
    tables = ['class', 'student', 'chart', 'score', 'avatar']
    test_db_tables = empty_sqlite_database._connection().execute(
        """SELECT name from sqlite_master WHERE type='table' """).fetchall()
    for table in tables:
        assert (table,) in test_db_tables


class TestSchema:
    @pytest.mark.parametrize(
        'table, columns',
        [('class', ['id', 'name']),
         ('student', ['id', 'name', 'class_id', 'avatar_id']),
         ('chart', ['id', 'name', 'image', 'date']),
         ('score', ['id', 'chart_id', 'student_id', 'value']),
         ('avatar', ['id', 'image']),
         pytest.param('student', ['height', 'weight'], marks=pytest.mark.xfail),
         pytest.param('class_parrot', ['dead', 'sleeping'], marks=pytest.mark.xfail),
         ])
    def test_schema(self, empty_sqlite_database, table, columns):
        """Test table schema as expected."""
        conn = empty_sqlite_database._connection()
        # Ensure all columns are present:
        cursor = conn.cursor().execute(f"""SELECT * from {table}""")
        assert columns == [description[0] for description in cursor.description]


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
        # Create test NewClass object, mocking avatar_files.
        test_class = NewClass.from_dict(test_class_data.json_dict())
        for student in test_class:
            if student.avatar_id:
                Path(test_class.temp_avatars_dir, student.avatar_id).write_text(student.avatar_id)

        # no students or class in empty db:
        assert not test_database._connection().cursor().execute("""SELECT * FROM class""").fetchall()
        assert not test_database._connection().cursor().execute("""SELECT * FROM student""").fetchall()

        # Create class in db:
        assert test_database.create_class(test_class) is None

        # Find class id, load class to verify:
        classes = test_database.get_classes()
        test_class_id = classes[0].id

        # Class will have ids:
        test_loaded_class_with_student_ids = Class.from_dict(
            test_class.json_dict()).json_dict()
        test_id = 1
        for student in test_loaded_class_with_student_ids['students']:
            student['id'] = test_id
            test_id += 1

        assert test_database.load_class(  # NB Returned object will be Class, not NewClass:
            test_class_id).json_dict() == test_loaded_class_with_student_ids


class TestLoadClass:
    @pytest.mark.parametrize('class_data', ['test_class_name_only', 'test_full_class'])
    def test_load_class(self, request, empty_sqlite_database, class_data):
        test_database = empty_sqlite_database
        test_existing_class_data = request.getfixturevalue(class_data)
        # Create test NewClass object, mocking avatar_files.
        test_existing_class = NewClass.from_dict(test_existing_class_data.json_dict())
        for student in test_existing_class:
            if student.avatar_id:
                Path(test_existing_class.temp_avatars_dir, student.avatar_id).write_text(student.avatar_id)
        # Create class in db:
        test_database.create_class(test_existing_class)

        # Find class id to load:
        classes = test_database.get_classes()
        test_full_class_id = classes[0].id

        # Class will have ids:
        test_loaded_class_with_student_ids = Class.from_dict(
            test_existing_class.json_dict()).json_dict()
        test_id = 1
        for student in test_loaded_class_with_student_ids['students']:
            student['id'] = test_id
            test_id += 1

        # Load class, verify data.
        assert test_database.load_class(  # NB Returned object will be Class, not NewClass:
            test_full_class_id).json_dict() == test_loaded_class_with_student_ids

        assert test_database._connection().cursor().execute("""SELECT * FROM class""").fetchall()
        if test_existing_class.students:
            assert test_database._connection().cursor().execute("""SELECT * FROM student""").fetchall()
            # Ensure students are given non null id:
            assert test_database.load_class(test_full_class_id).students[0]


class TestUpdateClass:
    """Method is unused and unimplemented."""

    def test_update_class(self, empty_sqlite_database):
        with pytest.raises(NotImplementedError):
            empty_sqlite_database.update_class(Class(name='some class'))


class TestGetAvatarPath:
    def test_get_avatar_path(self, empty_sqlite_database):
        """Return avatar."""
        test_database = empty_sqlite_database
        # Create avatar:
        test_avatar_data = b'some binary data'

        # Add avatar to db:
        with test_database._connection() as conn:
            conn.cursor().execute("""INSERT INTO avatar(image) VALUES(?)""", (test_avatar_data,))
            conn.commit()

        # Path may be different/random - test data:
        # Avatar id will be 1 as it is only one in empty db:
        assert test_database.get_avatar_path(1).read_bytes() == test_avatar_data

    def test_get_avatar_path_returning_default_avatar(self, empty_sqlite_database):
        """Return default avatar if None/Falsy argument."""
        test_database = empty_sqlite_database

        assert test_database.get_avatar_path(
            None).read_bytes() == empty_sqlite_database.default_avatar_path.read_bytes()


class TestCreateChart:
    def test_create_chart(self, empty_sqlite_database):
        """
        Verify API works.

        NB No verification in API test, as API for verifying does not exist.
        TODO: Verify saved chart contents when load/edit features added.
        """
        test_database = empty_sqlite_database
        test_class = NewClass(name='test_class', students=[Student(name='bad student'),
                                                           Student(name='mediocre student'),
                                                           Student(name='excellent student'),
                                                           Student(name='another mediocre student'),
                                                           ])
        test_database.create_class(test_class)

        test_chart_data_dict = {'class_id': test_class.id,
                                'class_name': test_class.name,
                                'chart_name': 'test_chart_name',
                                'chart_default_filename': 'test_default_chart_filename',
                                'chart_params': {'some': 'params'},
                                'score-students_dict': {0: [test_class.students[0]],
                                                        50: [test_class.students[1], test_class.students[3]],
                                                        100: [test_class.students[2]],
                                                        }
                                }

        assert test_database.create_chart(test_chart_data_dict) is None

        # Verify chart data in db:
        # A load_chart method might go here.

        assert test_database._connection().cursor().execute(
            """SELECT chart.name FROM chart""").fetchone()[0] == test_chart_data_dict['chart_name']

        scores_data = []
        for score, students in test_chart_data_dict['score-students_dict'].items():
            # NB One chart in db -> chart.id = 1
            scores_data += [(1, student.id, score) for student in students]
        assert test_database._connection().cursor().execute(
            """SELECT chart_id, student_id, value FROM score""").fetchall() == scores_data
        # Ensure chart id added to chart_data_dict:
        assert test_chart_data_dict['chart_id'] == 1


class TestConnection:
    def test__connection(self, empty_sqlite_database):
        """Connection function returns connection."""
        assert isinstance(empty_sqlite_database._connection(), sqlite3.Connection)
