# 01 — Data sources: raw data and the pipeline stages

This file says where a pull lands on disk, what happens to it next, and the rules that keep it trustworthy.

## The folder layout

Everything under `data/` is ignored by git.
Nothing in it is ever committed.

```
data/
  raw/<dataset>/
    <YYYY-MM-DD>/              one pull: the files exactly as downloaded, plus _source.json
    manifest.json              every pull and every stage run for this dataset
  landing/<dataset>/
    <YYYY-MM-DD>.parquet       the pull, typed, as one table
  clean/<dataset>/
    <YYYY-MM-DD>.parquet       the current-state rows, after the dataset's filter and checks
    rejects_<YYYY-MM-DD>.csv   every row dropped or altered, with the reason
  warehouse.duckdb             the canonical tables (lots, sales, filings, violations, ...)
  export/nyc.duckdb            the read-only copy the API, the dashboard and the agent open
  tiles/                       map tiles (PMTiles) and their index
  runs/<UTC timestamp>.jsonl   one line per step: what ran, how long, rows in and out
```

The dataset's id from [`sources.md`](sources.md) names every folder.

## The stages

Each dataset runs the same four stages, in order.
Then four project-level steps run across all datasets.

| Stage | Reads | Writes | What it does |
|---|---|---|---|
| `pull` | the source | `raw/<dataset>/<date>/` | Downloads. Records the URL, the query, the byte count and a SHA-256 hash of each file. |
| `land` | newest raw pull | `landing/<dataset>/<date>.parquet` | Reads the files into one table. Lowercases column names. Pins column types. Puts geometry in EPSG:4326. Adds `_pull_date` and `_row_id`. Changes no values. |
| `clean` | newest landing | `clean/<dataset>/<date>.parquet`, rejects | Applies the "Keep" filter from `sources.md`. Fixes types and units. Checks keys. Every dropped or altered row goes to the rejects file with a reason. |
| `load` | newest clean | `warehouse.duckdb` | Maps the dataset's columns to a canonical table. Writes exactly the columns `SCHEMA.md` names, in order. |

| Project step | Reads | Writes | What it does |
|---|---|---|---|
| `derive` | warehouse | `lot_metrics` and other derived tables | Computes the per-lot numbers the reviews use: buildable area, open violation counts, distance to transit. |
| `export` | warehouse | `export/nyc.duckdb` | Copies the tables the API needs into a read-only file. |
| `tiles` | export | `tiles/` | Builds the map layers. |
| `detect` | the two newest clean files of each dataset | `site_queue` | Finds what is new since the last pull and queues sites for review. See [`../06-SITE-REVIEW-AGENT.md`](../06-SITE-REVIEW-AGENT.md). |

One command runs one stage of one dataset:

```bash
uv run python -m meridian_dashboard_nyc.datasets pluto pull
```

`all` in place of the dataset id runs that stage for every dataset in dependency order.
It stops at the first failure and names the dataset.

## Rules that hold at every stage

1. **Raw is never overwritten.** A pull writes a new dated folder. A failed pull leaves earlier pulls untouched.
2. **Downloads land atomically.** A pull writes into `<date>.partial/` and renames the folder only when every file is complete and hashed.
3. **Raw is pruned only after a good run.** `prune` keeps the two newest pulls of each dataset, with their landing and clean files, and removes the rest (decision D3). It is the last step of `make daily` and runs only when every step before it succeeded, so a failed run never removes the last good pull. It can also be run by hand.
4. **An unchanged input does nothing.** If a stage's input hash matches the last run, the stage writes `unchanged` to the manifest and exits in under a second.
5. **Every run is recorded.** Each stage appends one entry to the dataset's `manifest.json` and one line to `runs/`, whether it worked or failed.
6. **No stage reads a later stage.** `land` never opens `clean/`. `clean` never opens the warehouse.
7. **No source column name leaves `load`.** After `load`, code sees canonical names only. A column called `zonedist1` exists in the PLUTO module and nowhere else.
8. **The API never opens `warehouse.duckdb`.** It reads `export/nyc.duckdb`.

## What `_source.json` records

One file per pull, next to the downloaded files.

```json
{
  "dataset": "hpd_violations",
  "source": "socrata",
  "portal_id": "wvxf-dwi5",
  "url": "https://data.cityofnewyork.us/resource/wvxf-dwi5.csv",
  "query": {"$where": "violationstatus = 'Open'"},
  "portal_rows_updated_at": "2026-10-22T08:14:00Z",
  "started_utc": "2026-10-22T12:00:03Z",
  "finished_utc": "2026-10-22T12:09:41Z",
  "files": [{"name": "part-000.csv", "bytes": 1234567890, "sha256": "..."}],
  "rows": 2876572,
  "code_version": "git sha of the repo at pull time"
}
```

`portal_rows_updated_at` comes from the portal's metadata endpoint ([`api.md`](api.md)).
If it has not moved since the last pull, `pull` can skip the download.

## Filter at pull, or filter at clean?

Filter at `clean` by default.
The filter can then change without a new download.

Filter at `pull` only when both are true:

- the full download is many times larger than the rows we keep, and
- the filter is unlikely to change.

Six datasets fit today: `hpd_violations` (open only), `service_requests_311` (since the start date), `city_record` (four sections), `property_valuation` (newest tax year), `dob_complaints` (since the start date) and `collisions` (since the start date).
The filter is written into `_source.json`, so a pull always says what it left out.
Moving the start date back (D2) makes the next pull of the date-filtered ones larger; the datasets filtered at `clean` need no new download.

ACRIS is the exception that needs a plan.
Its three tables join on `document_id`, and the API cannot join.
Pull all three in bulk on the first run.
Later runs pull only documents recorded since the last pull, then the legals and parties for those documents.
Write this as the ACRIS module's own spec before building it.

## Landing conventions

- **Column names:** lowercase, words joined by underscores. `ZoneDist1` becomes `zonedist1`.
- **Types:** pinned in the dataset's `landing_types.py` after the first profile. Type inference changes when a column's first rows change. Pinned types do not.
- **Geometry:** one column called `geometry`, stored as WKB in EPSG:4326 (longitude and latitude). MapPLUTO ships in EPSG:2263 (New York State Plane, Long Island, in feet). Reproject it at land.
- **Measuring:** areas and distances are computed in EPSG:2263, never in EPSG:4326. One helper does the reprojection, and a test fails on any measurement outside it.
- **Bookkeeping columns:** `_pull_date` (the raw folder's date) and `_row_id` (the row's position in the pull).

## The previous pull and "what's new"

`detect` compares the two newest clean files of a dataset on its key.
It writes three kinds of difference:

| Kind | Meaning | Example |
|---|---|---|
| `added` | Key in the new pull, not in the old | A new-building job filing appears |
| `removed` | Key in the old pull, not in the new | A lot disappears in a PLUTO merge |
| `changed` | Same key, a watched column differs | A ZAP project moves to public review |

Each dataset lists its watched columns in its module.
A change to an unwatched column is ignored.
This is the only use of the previous pull.

## Expected sizes

Measured on 2026-10-22 where the source states a size.
Write the measured size into each dataset's README at its first pull.

| Dataset | Size or rows | Note |
|---|---|---|
| `mappluto` | 302 MB zip | Shoreline-clipped shapefile |
| PLUTO CSV (`pluto/nyc_pluto_26v2_csv.zip`) | 72 MB zip | Same data as `64uk-42ks`; a faster first pull than the API |
| `pad` | 46 MB zip | |
| `acris_parties` | 46.7 million rows | The largest bulk download; expect several gigabytes |
| `acris_legals` | 22.8 million rows | |
| `acris_master` | 17.1 million rows | |
| `service_requests_311` | 22.9 million rows in full | Rows since the start date kept |
| `property_valuation` | 11.7 million rows in full | About 1.18 million kept |
| `hpd_violations` | 11.3 million rows in full | About 2.9 million kept |

Plan for tens of gigabytes of free disk before Phase 3.

## Test fixtures

Tests never touch `data/`.
Each dataset has a fixture under `tests/fixtures/<dataset>/`: at most 20 rows cut from a real landing file.
Cut fixtures after the first real pull, not from memory.
A fixture is committed. Real data never is.

## Where the old repo did this

Read these before writing the new versions.
Do not copy them; rebuild the idea in your own words.

| Idea | Old file |
|---|---|
| A dataset class with stages | `src/urban_metrics/datasets/base.py` |
| The manifest and its entries | `src/urban_metrics/datasets/manifest.py` |
| Readers for CSV, GeoJSON, zip, shapefile | `src/urban_metrics/datasets/readers.py` |
| Downloads, paging, hashing | `src/urban_metrics/ingest/http.py` |
| One dataset's pipeline, end to end | `src/urban_metrics/datasets/nyc/facilities/pipeline.py` |
| The change table between two releases | `src/urban_metrics/export/changes.py` |
