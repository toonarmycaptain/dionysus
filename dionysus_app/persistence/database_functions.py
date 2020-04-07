""" Script for database management functions. """


from dionysus_app.persistence.database import Database
from dionysus_app.persistence.databases.json import JSONDatabase


database_backends = {'JSON': JSONDatabase,
                     }


def load_database() -> Database:
    from dionysus_app.app_data.settings import dionysus_settings
    database_type = dionysus_settings['database']

    if database_type not in database_backends:
        raise ValueError("Selected database backend not available.")
    return database_backends[database_type]()
