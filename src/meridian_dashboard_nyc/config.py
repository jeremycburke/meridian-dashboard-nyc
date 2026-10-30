"""Where the data lives, when the event logs start, and the keys from .env."""

import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parents[2]
DATA = ROOT / "data"

EVENT_LOG_START_DATE = date(2025, 1, 1)

load_dotenv(ROOT / ".env")
SOCRATA_APP_TOKEN = os.getenv("SOCRATA_APP_TOKEN")
