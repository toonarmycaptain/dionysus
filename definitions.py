"""
definitions.py - source for vars used throughout application.None

ROOT_DIR - path to directory containing app_main/definitions
DEFAULT_DATABASE_BACKEND - the default database backend
DATABASE - the database object.
DEFAULT_CHART_SAVE_DIR - default user save folder for generated charts.

For state-holding object eg DATABASE, must import definitions, then use
dot access to use the object:
    import definitions
    definitions.DATABASE.do_stuff()
"""
import os

from pathlib import Path
from typing import Optional, TYPE_CHECKING

# Import to get around circular import caused by type checking. Type as string.
if TYPE_CHECKING:
    from dionysus_app.persistence.database import Database  # Line skipped from coverage.

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Global root directory.

DEFAULT_DATABASE_BACKEND = 'SQLite'
# Ignore typehint error: DATABASE object needs to be initialised with a value
DATABASE: 'Database' = None  # type: ignore


DEFAULT_CHART_SAVE_DIR: Optional[Path] = None  # Path object.
