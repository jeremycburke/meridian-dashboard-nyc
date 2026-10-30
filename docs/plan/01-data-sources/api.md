# 01 — Data sources: APIs

This file has two parts.
Part 1 is how we fetch data from the sources.
Part 2 is the API this project serves to its own dashboard and agent.

Every example in Part 1 was run on 2026-10-22 and returned what it says.

---

## Part 1 — Fetching from the sources

### 1.1 Socrata (NYC Open Data and NYS Open Data)

Both portals run on Socrata.
The same code reaches both; only the host changes.

| Host | Datasets |
|---|---|
| `data.cityofnewyork.us` | Everything in `sources.md` except the three marked NYS |
| `data.ny.gov` | `subway_stations`, `subway_entrances`, `liquor_licenses` |

Socrata offers five endpoints we use.

| Purpose | Endpoint | When we use it |
|---|---|---|
| Metadata | `GET https://<host>/api/views/<id>.json` | Before every pull: name, publisher, column list and types, `rowsUpdatedAt` |
| Query | `GET https://<host>/resource/<id>.csv?<SoQL>` | Filtered pulls, counts, paging |
| Bulk export | `GET https://<host>/api/views/<id>/rows.csv?accessType=DOWNLOAD` | Whole-dataset pulls with no filter |
| Geospatial export | `GET https://<host>/api/geospatial/<id>?method=export&format=GeoJSON` | Boundary datasets stored as maps |
| Catalog search | `GET https://api.us.socrata.com/api/catalog/v1?domains=data.cityofnewyork.us&q=<words>` | Finding a dataset's id |

#### The query language (SoQL)

Query parameters start with `$`.

| Parameter | Does | Example |
|---|---|---|
| `$select` | Picks columns, or computes | `$select=count(*)` |
| `$where` | Filters rows | `$where=violationstatus = 'Open'` |
| `$group` | Groups for a count | `$group=violationstatus` |
| `$order` | Sorts | `$order=:id` |
| `$limit` | Rows per page | `$limit=50000` |
| `$offset` | Skips rows | `$offset=100000` |

Three habits prevent most bugs.

1. **Quote strings, not numbers.** `year = '2027'` works on a text column. Check the column's type in the metadata first.
2. **Write dates as floating timestamps.** `created_date >= '2025-10-22T00:00:00'`.
3. **Page on a stable order.** Without `$order=:id`, two pages can overlap or skip rows.

#### Worked examples

Count the rows in PLUTO and read its version:

```text
https://data.cityofnewyork.us/resource/64uk-42ks.json?$select=version,count(*)&$group=version
→ [{"version":"26v2","count":"858284"}]
```

Count open and closed HPD violations:

```text
https://data.cityofnewyork.us/resource/wvxf-dwi5.json?$select=violationstatus,count(*)&$group=violationstatus
→ Close 8,457,092 · Open 2,876,572
```

Find the newest tax year in the property valuation roll:

```text
https://data.cityofnewyork.us/resource/8y4t-faws.json?$select=year,period,count(*)&$group=year,period&$order=year desc&$limit=6
→ 2027 period 1: 1,178,567 · 2027 period 3: 1,180,360 · 2026 ...
```

Pull 311 requests since the start date, one page at a time:

```text
https://data.cityofnewyork.us/resource/erm2-nwe9.csv
  ?$where=created_date >= '2025-01-01T00:00:00'
  &$order=:id
  &$limit=50000
  &$offset=0
```

Ask one lot's open charges (the one live lookup):

```text
https://data.cityofnewyork.us/resource/scjx-j6np.json?$where=bbl = '1000477501'
```

Check a column name in the metadata before writing any filter on it.
The examples above use names read on 2026-10-22.

#### The app token

Without a token, Socrata throttles requests by IP address.
A token is free. Register one on the NYC Open Data site.

- Store it as `SOCRATA_APP_TOKEN` in `.env`. Never in code, a commit or a log.
- Send it as the `X-App-Token` header on every request.
- On a `429` response, wait and retry with backoff. Never loop without a wait.
- Send a `User-Agent` that names the project and a contact address.

#### Picking the endpoint for a pull

| Situation | Endpoint |
|---|---|
| Whole dataset, under about 5 million rows | Bulk export |
| Filtered pull (open items, a date window) | Query, paged |
| A map-type asset (boundaries) | Geospatial export |
| One lot at review time | Query with `$where=bbl = '...'` |

### 1.2 DCP Bytes of the Big Apple

DCP publishes its main products as zip files.

Base URL: `https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/`

| Dataset | Path after the base | Checked 2026-10-22 |
|---|---|---|
| `mappluto` | `mappluto/nyc_mappluto_<version>_arc_shp.zip` | `26v2`: 200 OK, 302 MB |
| PLUTO as CSV | `pluto/nyc_pluto_<version>_csv.zip` | `26v2`: 200 OK, 72 MB |
| `pad` | `pad/pad_<release>.zip` | `26c`: 200 OK, 46 MB |
| `zoning_districts` | the zoning features geodatabase zip on the Bytes zoning page | resolve the URL at build time |

Release names follow two patterns.
PLUTO uses year and version: `26v1`, `26v2`.
PAD uses year and letter: `26a`, `26b`, `26c`.

**Find the current MapPLUTO from PLUTO itself.**
Read `version` from `64uk-42ks` and build the MapPLUTO file name from it.
The two then match by construction.

These zips have no metadata endpoint.
Send a `HEAD` request and compare `Content-Length` and `Last-Modified` with the last pull.

### 1.3 NYC GeoSearch

GeoSearch turns an address into a lot number and a building number.
It needs no key.

| Endpoint | Use |
|---|---|
| `GET https://geosearch.planninglabs.nyc/v2/search?text=<address>&size=1` | Address to BBL and BIN |
| `GET https://geosearch.planninglabs.nyc/v2/autocomplete?text=<partial>` | The dashboard's search box |
| `GET https://geosearch.planninglabs.nyc/v2/reverse?point.lat=<lat>&point.lon=<lon>` | A map click to an address |

Example:

```text
https://geosearch.planninglabs.nyc/v2/search?text=120 broadway manhattan&size=1
→ label "120 BROADWAY, New York, NY, USA"
→ properties.addendum.pad = {"bbl": "1000477501", "bin": "1001026", "version": "26c"}
```

Rules.

- Cache every answer in a local table keyed by the normalized address. Never ask twice.
- Accept a match only when it carries a BBL. A street-level match is not a lot.
- A notice or a pasted listing may contain an address. Geocode it, then show the matched address back to the reader so a wrong match is visible.

### 1.4 Optional services (Phase 10)

| Service | Endpoint | Key | Use |
|---|---|---|---|
| Census ACS | `https://api.census.gov/data/<year>/acs/acs5?get=...&for=tract:*&in=state:36` | `CENSUS_API_KEY` | Population, income, rent by tract |
| MTA GTFS static | MTA developer data page | none | Train frequency at each station |
| NYC Geoclient v2 | NYC API portal | subscription key | A second geocoder, if GeoSearch falls short |

---

## Part 2 — The API this project serves

The dashboard and the agent read data through one small read-only API.
It is a FastAPI app over `data/export/nyc.duckdb`.
It never opens the warehouse.
[`../03-ARCHITECTURE.md`](../03-ARCHITECTURE.md) shows where it sits.

### Endpoints

| Method and path | Returns | Used by |
|---|---|---|
| `GET /health` | Export date and dataset freshness | Monitoring |
| `GET /datasets` | Each dataset's last pull, row count and whether it is overdue | Dashboard data page |
| `GET /lookup?address=` | Matched address, BBL, BIN | Search box, agent |
| `GET /lots/{bbl}` | The lot card for one lot: the sections the caller's tier allows (guests get identity, lot, building and zoning) | Lot page, agent |
| `GET /lots?<filters>` | A result id, a count and a 50-row sample. `area=` takes a neighborhood code or a saved lasso id | Dashboard table, agent |
| `GET /lots/{bbl}/comparables?area=&months=` | Comparable sales in the area (default: the lot's neighborhood), each with its metrics and their difference from the lot | Lot page, Review page, agent |
| `POST /areas` | Saves a lasso polygon drawn on the map; returns its area id | Dashboard map |
| `GET /results/{id}` | One page of a saved result, or a CSV download | Dashboard table |
| `GET /sites?since=&trigger=&profile=` | Queued new sites and why each was queued | Dashboard sites page |
| `GET /reviews` and `GET /reviews/{id}` | Finished reviews | Dashboard reviews page and inbox |
| `POST /reviews` | Queues a review of one BBL against one buyer profile, optionally with a search area | Dashboard button |
| `GET /profiles`, `POST /profiles`, `PUT /profiles/{id}` | The caller's own buyer profiles; creating and editing them within the tier's limits | Dashboard, agent |
| `GET /me` | The caller's account, role and usage | Dashboard |
| `GET /inbox?profile=&since=` | Each day's digest per profile, newest first | Dashboard inbox |

### Rules

1. **Read-only data.** The export file is opened read-only. Writes go only to the app database (D19): review requests, saved areas and profiles. Never to data tables.
2. **Large results are summaries.** A query that matches 40,000 lots returns a count, a sample and a result id. The full set is a download.
3. **Every number carries its source.** A lot card field says which dataset and which pull date it came from.
4. **Typed responses.** Every response is a Pydantic model. The models are the contract the dashboard and the agent's tools share.
5. **Every endpoint checks the caller's role itself** (D16, D18): guest, account or owner, read from the signed token Next.js sends. A user sees only their own profiles, inbox and reviews; the owner sees all. Hiding a page in the dashboard is not enough. Public endpoints are rate-limited per client (D6).
