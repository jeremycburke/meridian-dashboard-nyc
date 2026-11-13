"""Download NYC Open Data sources into data/raw/<source>/<date>/, one folder for each source.

uv run python -m meridian_dashboard_nyc.pull           every source
uv run python -m meridian_dashboard_nyc.pull pluto     one source
"""

import csv
import hashlib
import io
import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

import httpx

from meridian_dashboard_nyc import config
from meridian_dashboard_nyc.sources import SOURCES

PORTAL = "https://data.cityofnewyork.us"
USER_AGENT = "meridian-dashboard-nyc (https://github.com/jeremycburke/meridian-dashboard-nyc)"
PAGE_SIZE = 50_000


def client() -> httpx.Client:
    """Return a client for NYC Open Data, with the app token when .env has one."""
    headers = {"User-Agent": USER_AGENT}
    if config.SOCRATA_APP_TOKEN:
        headers["X-App-Token"] = config.SOCRATA_APP_TOKEN
    return httpx.Client(base_url=PORTAL, headers=headers, timeout=120)


def download(portal_id: str, where: str | None, dest: Path) -> int:
    """Write every matching row to dest as one CSV file, a page at a time. Return the row count."""
    # A stable order keeps pages from overlapping or skipping rows.
    params = {"$order": ":id", "$limit": PAGE_SIZE}
    if where:
        params["$where"] = where
    rows = 0
    with client() as http, dest.open("w", encoding="utf-8", newline="") as file:
        while True:
            params["$offset"] = rows
            response = http.get(f"/resource/{portal_id}.csv", params=params)
            response.raise_for_status()
            header, _, body = response.text.partition("\n")
            if rows == 0:
                file.write(header + "\n")
            file.write(body)
            # Count with the csv module, because a quoted field can hold a line break.
            page_rows = sum(1 for _ in csv.reader(io.StringIO(body)))
            rows += page_rows
            if page_rows < PAGE_SIZE:
                return rows


def pull(name: str) -> Path:
    """Download one source into data/raw/<name>/<today>/ and return the folder."""
    source = SOURCES[name]
    today = datetime.now(UTC).date().isoformat()
    folder = config.DATA / "raw" / name / today
    if folder.exists():
        print(f"{name}: already pulled today, {folder}")
        return folder

    # Download into a .partial folder, and rename it only when the pull is complete.
    partial = folder.with_name(f"{today}.partial")
    shutil.rmtree(partial, ignore_errors=True)
    partial.mkdir(parents=True)
    started = datetime.now(UTC)
    path = partial / f"{name}.csv"
    rows = download(source["portal_id"], source.get("where"), path)
    with path.open("rb") as file:
        sha256 = hashlib.file_digest(file, "sha256").hexdigest()

    record = {
        "source": name,
        "portal_id": source["portal_id"],
        "url": f"{PORTAL}/resource/{source['portal_id']}.csv",
        "where": source.get("where"),
        "started_utc": started.isoformat(timespec="seconds"),
        "finished_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "rows": rows,
        "file": {"name": path.name, "bytes": path.stat().st_size, "sha256": sha256},
    }
    (partial / "_source.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    partial.rename(folder)
    print(f"{name}: {rows:,} rows in {folder}")
    return folder


if __name__ == "__main__":
    for name in sys.argv[1:] or SOURCES:
        pull(name)
