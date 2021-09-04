""" Test sqlite accessed with SQLAlchemy and SQLDatabase"""
import io
from pathlib import Path
from random import randint

import pytest

from matplotlib import pyplot as plt
from matplotlib.testing.compare import compare_images
from sqlalchemy import inspect

from dionysus_app.class_ import NewClass
from dionysus_app.persistence.databases.sqlite_sqlalchemy import SQLiteSQLAlchemyDatabase

from dionysus_app.student import Student


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


class TestCreateChart:
    def test_create_chart(self, empty_sqlite_sqlalchemy_database):
        """
        Verify API works.

        NB No verification in API test, as API for verifying does not exist.
        TODO: Verify saved chart contents when load/edit features added.
        """
        test_database = empty_sqlite_sqlalchemy_database
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
        with test_database.session_scope() as test_session:
            assert test_session.execute(
                """SELECT chart.name FROM chart""").fetchone()[0] == test_chart_data_dict['chart_name']

            scores_data = []
            for score, students in test_chart_data_dict['score-students_dict'].items():
                # NB One chart in db -> chart.id = 1
                scores_data += [(1, student.id, score) for student in students]
            assert test_session.execute(
                """SELECT chart_id, student_id, value FROM score""").fetchall() == scores_data
            # Ensure chart id added to chart_data_dict:
            assert test_chart_data_dict['chart_id'] == 1


class TestSaveChartImage:
    def test_save_chart_image(self, tmpdir, empty_sqlite_sqlalchemy_database):
        """Save image and verify data."""
        test_database = empty_sqlite_sqlalchemy_database

        test_data_dict = {
            'class_id': 314,
            'class_name': "test_class_name",
            'chart_name': "test_chart_name",
            'chart_default_filename': "test_chart_default_filename",
            'chart_params': {"some": "chart", "default": "params"},
            'score-students_dict': {0: [Student(student_id=42, name="Brian")],
                                    },
            }
        # Create chart in db:
        test_database.create_chart(test_data_dict)
        # Create fake plot/image
        mock_plt = plt.figure(figsize=(19.20, 10.80))
        test_image = io.BytesIO()
        mock_plt.savefig(test_image, format='png', dpi=300)
        test_image.seek(0)  # Return pointer to start of binary stream.

        save_chart_path = test_database.save_chart_image(test_data_dict, mock_plt)
        # Path exists and image at path/db is expected data:
        assert save_chart_path.exists()
        assert save_chart_path.read_bytes() == test_image.read1()  # size arg can be omitted on 3.7+
        test_image.seek(0)  # Return pointer to start of test_image binary stream.

        # Compare db image
        with test_database.session_scope() as test_session:
            db_image = test_session.query(test_database.Chart).filter_by(id=test_data_dict['chart_id']).first().image
        # Images must both be saved as '.png' for comparison.
        test_image_path = Path(tmpdir, 'test_image.png')
        test_image_path.write_bytes(test_image.read1())
        test_image.seek(0)
        db_image_path = Path(tmpdir, 'db_image.png')
        db_image_path.write_bytes(db_image)
        try:
            assert not compare_images(db_image_path, test_image_path, 0.0001)  # Returns str on fail, None on success.
        except MemoryError:
            pass  # fails for 32 bit python on Windows.
        assert save_chart_path.read_bytes() == test_image.read()
