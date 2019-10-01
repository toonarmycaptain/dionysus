import os

from pathlib import Path
from typing import List, Optional, Iterable

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Global root directory.

REGISTRY: List[str] = []

DEFAULT_CHART_SAVE_FOLDER: Path = Path('.')  # Path object.
