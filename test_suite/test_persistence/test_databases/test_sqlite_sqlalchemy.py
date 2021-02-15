""" Test sqlite accessed with SQLAlchemy and SQLDatabase"""
from pathlib import Path
from random import randint

import pytest

from sqlalchemy import inspect

from dionysus_app.persistence.databases.sqlite_sqlalchemy import SQLiteSQLAlchemyDatabase


# Test  per-API then backend specific methods
# -> Test API for all databases in test_database.py, passing in each database type using parametrize?

def empty_sqlite_sqlalchemy_test_db(db_path) -> SQLiteSQLAlchemyDatabase:
    """
    Return empty SQLiteSQLAlchemyDatabase at path for testing.

    :param db_path: Path
    :return: SQLite_sqlalchemyDatabase
    """
    # give random db ref to avoid having to drop the tables and recreate each time....much faster!
    num = randint(1, 1000000000)
    # for some reason this didn't work on linux, but does on Win10:
    # return SQLiteDatabase(database_path=f'file:test_db{num}?mode=memory&cache=shared')
    # Slower, but cross platform:
    return SQLiteSQLAlchemyDatabase(database_path=Path(db_path, f'test_db{num}'))


@pytest.fixture
def empty_sqlite_sqlalchemy_database(tmpdir) -> SQLiteSQLAlchemyDatabase:
    """
    Initialised empty SQLite_sqlalchemyDatabase.

    Basing in tmpdir works where basing in a 'file:' fails on linux,
    and also ensures test atomicity, each test starting with a fresh,
    empty database.

    :param tmpdir: temporary directory path (fixture)
    :return: SQLiteSQLAlchemyDatabase
    """
    test_db = empty_sqlite_sqlalchemy_test_db(tmpdir)
    return test_db


def test_empty_sqlite_sqlalchemy_database_fixture(empty_sqlite_sqlalchemy_database):
    """Ensure test db can be connected to and tables exist."""
    # THIS MIGHT NEED MODIFYING FOR SQLAlchemy db
    assert empty_sqlite_sqlalchemy_database

    tables = ['class', 'student', 'chart', 'score', 'avatar']
    test_db_tables = inspect(empty_sqlite_sqlalchemy_database.engine).get_table_names()
    for table in tables:
        assert table in test_db_tables
