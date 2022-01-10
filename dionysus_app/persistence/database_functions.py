""" Script for database management functions. """

from dionysus_app.persistence.database import Database
from dionysus_app.persistence.databases.json import JSONDatabase
from dionysus_app.persistence.databases.sqlite import SQLiteDatabase
from dionysus_app.persistence.databases.sqlite_sqlalchemy import SQLiteSQLAlchemyDatabase

database_backends = {'JSON': JSONDatabase,
                     'SQLite': SQLiteDatabase,
                     'SQLiteSQLAlchemy': SQLiteSQLAlchemyDatabase,
                     }


def load_database() -> Database:
    """
    Instantiate/load Database object.

    :return: Database object
    """
    from dionysus_app.app_data.settings import dionysus_settings
    database_type = dionysus_settings['database']

    if database_type not in database_backends:
        raise ValueError("Selected database backend not available.")
    return database_backends[database_type]()
