import importlib
from datetime import date
from pathlib import Path

from meridian_dashboard_nyc import config

REPO = Path(__file__).parents[1]


def test_s001_c1_paths_live_under_data():
    assert config.DATA == REPO / "data"


def test_s001_c2_event_log_start_is_2025_01_01():
    assert date(2025, 1, 1) == config.EVENT_LOG_START_DATE


def test_s001_c3_env_values_come_through_config(monkeypatch):
    monkeypatch.setenv("SOCRATA_APP_TOKEN", "test-token")
    importlib.reload(config)
    assert config.SOCRATA_APP_TOKEN == "test-token"
