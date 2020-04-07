import os

from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

# Import to get around circular import caused by type checking. Type as string.
if TYPE_CHECKING:
    from dionysus_app.persistence.database import Database  # Line skipped from coverage.

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Global root directory.

DEFAULT_DATABASE_BACKEND = 'JSON'

DATABASE: Optional['Database'] = None
REGISTRY: Optional[List] = None

DEFAULT_CHART_SAVE_FOLDER: Optional[Path] = None  # Path object.
