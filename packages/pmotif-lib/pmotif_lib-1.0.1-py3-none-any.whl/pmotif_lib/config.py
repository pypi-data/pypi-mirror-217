"""Configuration constants."""
import os
from pathlib import Path

DATASET_DIRECTORY = Path(os.getenv("DATASET_DIRECTORY"))
EXPERIMENT_OUT = Path(os.getenv("EXPERIMENT_OUT"))
GTRIESCANNER_EXECUTABLE = Path(os.getenv("GTRIESCANNER_EXECUTABLE"))

WORKERS = int(os.getenv("WORKERS", default="1"))
