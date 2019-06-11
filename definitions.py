import os

from pathlib import Path
from typing import List, Optional

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Global root directory.

REGISTRY: Optional[List] = None

DEFAULT_CHART_SAVE_FOLDER: Path = None  # Path object.
