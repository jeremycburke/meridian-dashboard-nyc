# 03 — Architecture

This file shows how the pieces fit: the layers, the folders, the tables and the flow of data from a source to the inbox.

## The chain

Data moves in one direction.
No layer reads a layer after it.

```
 sources          datasets/            warehouse          derive         export           serve
 ───────          ─────────            ─────────          ──────         ──────           ─────
 NYC Open Data ─▶ pull ─▶ land ─▶ ──▶ canonical  ──▶  lot_metrics ──▶ nyc.duckdb ──┬──▶ API ──▶ dashboard
 DCP Bytes        clean ─▶ load        tables                         (read-only)  ├──▶ agent ──▶ inbox
 data.ny.gov                                                                       └──▶ tiles ──▶ map
                       │
                       └── two newest clean pulls ──▶ detect ──▶ site_queue ──▶ agent ──▶ reviews
```

Five rules hold the chain together.

1. **Source column names stop at `load`.** After that, code uses canonical names.
2. **The warehouse is written by `load` and `derive` only.**
3. **The API, the dashboard and the agent read the export, never the warehouse.**
4. **Numbers come from SQL.** The agent never computes a number. It reads one from a tool result.
5. **Current state only.** The previous pull exists to compute `detect`. Nothing else reads it.

## Folder layout

```
meridian-dashboard-nyc/
├── README.md                     what it is, how to run it, where the docs are
├── AGENTS.md                     how any coding agent works in this repo
├── CLAUDE.md                     imports AGENTS.md; Claude-specific notes
├── SPEC.md                       the build plan: every spec in order, with tests, checks, docs
├── BRAND.md                      the dashboard's design rules and tokens (D10)
├── pyproject.toml  uv.lock       (from S001)
├── .env.example                  every key, empty
├── .gitignore  .gitattributes
├── docs/
│   ├── plan/                     these files
│   ├── SCHEMA.md                 the canonical tables, column by column
│   ├── decisions.md              one line per owner decision, dated
│   └── checkpoints/              one write-up per phase checkpoint, with screenshots
├── specs/
│   ├── 000-TEMPLATE.md
│   └── 001-scaffold.md ...       one spec per row of SPEC.md
├── src/meridian_dashboard_nyc/
│   ├── config.py                 paths, settings (the event-log start date), reads .env
│   ├── runlog.py                 timed steps → data/runs/
│   ├── geo.py                    the measuring helper (EPSG:2263) and nothing else
│   ├── schema.py                 SCHEMA.md as code; checked by a test
│   ├── sources/                  HTTP clients: socrata.py, bytes.py, geosearch.py
│   ├── datasets/
│   │   ├── base.py               the Dataset class: pull, land, clean, load
│   │   ├── manifest.py
│   │   ├── registry.py           every dataset, in dependency order
│   │   ├── __main__.py           python -m meridian_dashboard_nyc.datasets <id> <stage>
│   │   ├── pluto/                one package per dataset:
│   │   │   ├── dataset.py        source, cadence, keep filter, watched columns
│   │   │   ├── landing_types.py  pinned column types
│   │   │   ├── load.py           source columns → canonical columns
│   │   │   └── README.md         what it is, quirks, measured sizes
│   │   └── ... (one per row of sources.md)
│   ├── derive/                   lot_metrics and other derived tables
│   ├── network/                  the walking graph and walking distances (D11)
│   ├── form/                     urban-form metrics, one module per level (D15)
│   ├── export/                   builds data/export/nyc.duckdb
│   ├── detect/                   compares pulls, writes site_queue
│   ├── api/                      FastAPI app, routes, response models
│   ├── agent/                    profiles, site card, tools, loop, review output
│   ├── appdb/                    the app database: connection, migrations, queries (D19)
│   ├── digest/                   the daily digest per profile, for the Inbox page
│   └── tiles/                    builds PMTiles
├── profiles/                     buyer profiles as YAML, imported into the app database; only example.yaml is committed
├── watchlist.example.yaml        the shape of watchlist.yaml, which stays out of git (D8)
├── web/                          Next.js + React + deck.gl dashboard (from S041)
├── tests/
│   ├── fixtures/<dataset>/       at most 20 real rows each
│   └── test_*.py
└── data/                         gitignored (see 01-data-sources/raw.md)
```

**Old repo departures.**
- `ingest/` and `datasets/` were two systems in the old repo. Here there is one: `datasets/`.
- No `territory/`, no `causal/`, no `outcomes/`, no `history/`, no `engine/`. A second city would get its own database, not a column (D13).
- `sources/` is new. It keeps HTTP code out of the dataset packages, so a dataset package never opens a network connection itself.

## The canonical tables

`docs/SCHEMA.md` will hold the column lists.
It is written phase by phase, after each dataset's first profile.
This section fixes only each table's grain and key, so the phases agree on the shape.

A table or column not in `SCHEMA.md` does not exist.
Adding one is a written change to `SCHEMA.md` first, then code.

### Current-state tables (written by `load`)

| Table | One row is | Key | Fed by | Phase |
|---|---|---|---|---|
| `lots` | One tax lot | `bbl` | `pluto`, `mappluto` | 1 |
| `buildings` | One building | `bin` | `building_footprints` | 1 |
| `addresses` | One address range | `bbl`, `bin`, range | `pad` | 1 |
| `condo_units` | One unit lot | `unit_bbl` → `billing_bbl` | `dtm_condo_units`, `dtm_condos` | 1 |
| `zones` | One polygon of any kind (zoning district, overlay, special district, MIH area, landmark district, school zone, community district, ...) | `kind`, `zone_id` | Groups B, G, H | 2, 5 |
| `lot_restrictions` | One restriction on one lot (e-designation, landmark) | `bbl`, `kind`, `ref` | `e_designations`, `landmark_sites`, `lpc_buildings` | 2 |
| `documents` | One recorded document on one lot | `document_id`, `bbl` | `acris_*` | 3 |
| `sales` | One sale of one lot | `bbl`, `sale_date`, `source_ref` | `rolling_sales`, ACRIS deeds | 3 |
| `assessments` | One lot's value for the current tax year | `bbl` | `property_valuation` | 3 |
| `tax_benefits` | One exemption or abatement on one lot | `bbl`, `kind`, `code` | `property_exemptions`, `property_abatements` | 3 |
| `filings` | One DOB job, from either system | `system`, `job_id` | four DOB filing and permit datasets | 3 |
| `certificates` | One certificate of occupancy | `system`, `certificate_id` | two DOB certificate datasets | 3 |
| `pipeline` | One housing project with net units | `job_id` | `housing_database`, `affordable_housing` | 3 |
| `violations` | One open violation, any agency | `agency`, `violation_id` | HPD and DOB violation datasets | 4 |
| `complaints` | One complaint in the window | `source`, `complaint_id` | `dob_complaints`, `service_requests_311` | 4, 5 |
| `registrations` | One registered building and its contacts | `registration_id` | HPD registration datasets | 4 |
| `energy` | One building's newest energy report | `bbl`, `bin` | `ll84_energy` | 4 |
| `notices` | One open public notice or land-use project | `source`, `notice_id` | `zap_*`, `city_record` | 4 |
| `places` | One point people go to | `kind`, `place_id` | facilities, subway entrances, storefronts, licenses | 5 |

Five kinds of "flag" sit on these tables as columns, never as deleted rows: a non-market deed, a lot on the lien sale list, an AEP building, a speculative sale, a company buyer.

### Derived tables (written by `derive`, `form` and `detect`)

| Table | One row is | Key | Written by |
|---|---|---|---|
| `lot_zones` | One lot inside one zone | `bbl`, `kind`, `zone_id` | `derive` (spatial join in EPSG:2263) |
| `lot_metrics` | One lot's computed numbers | `bbl` | `derive` |
| `area_metrics` | One area's computed numbers (NTA now; block and cell later) | `grain`, `area_id` | `form` |
| `metric_meta` | One metric's definition, grain and inputs | `name`, `version` | `derive`, `form` |
| `changes` | One difference between two pulls | `dataset`, `key`, `kind`, `column` | `detect` |

Every metric has a versioned name, such as `unused_floor_area_sqft@v1`.
Its definition lives in one function with a docstring that says what it measures and what it does not.
It is computed once into `lot_metrics`.
Nothing recomputes it elsewhere.

### App tables (Postgres, decision D19)

Everything a user or the agent writes lives here, never in the warehouse.
Only the Python side (the API, `detect`, the agent, `digest`) connects; Next.js never does.

| Table | One row is | Key | Written by |
|---|---|---|---|
| `users` | One account and its role | `user_id` | API, on first sign-in |
| `profiles` | One buyer profile, owned by one user | `profile_id` | API (yours imported from `profiles/*.yaml`) |
| `site_queue` | One site waiting for review | `bbl`, `trigger`, `detected_on` | `detect`, `POST /reviews` |
| `reviews` | One finished review | `review_id` | the agent |
| `digests` | One day's digest for one profile | `profile_id`, `digest_date` | `digest` |
| `search_areas` | One saved lasso polygon | `area_id` | `POST /areas` |
| `usage` | One model call's tokens and cost, charged to a user | `call_id` | the agent |

## The lot card

The lot card is the project's central object.
It is everything the record says about one lot today, in fixed sections.
The lot page draws it.
The agent reads it.
The digest quotes it.

| Section | Contents | Tables |
|---|---|---|
| Identity | Address, BBL, borough, community district, owner name as recorded | `lots`, `addresses` |
| The lot | Lot area, frontage, depth, land use, building class | `lots` |
| The building | Floors, units, gross area, year built, footprint, height | `lots`, `buildings` |
| Zoning | Districts, overlays, special districts, max FAR by use, built FAR, unused floor area, MIH, transit zone | `lots`, `lot_zones`, `lot_metrics` |
| Restrictions | Landmark, historic district, e-designation | `lot_restrictions`, `lot_zones` |
| Ownership and money | Last sale, price per square foot, assessed and market value, tax benefits, lien list | `sales`, `documents`, `assessments`, `tax_benefits` |
| Activity | Open filings, recent permits, certificates, pipeline units | `filings`, `certificates`, `pipeline` |
| Condition | Open violations by agency and class, vacate orders, AEP, stalled site, facade status | `violations`, `registrations` |
| Energy | EUI, ENERGY STAR score, estimated LL97 exposure | `energy`, `lot_metrics` |
| Notices | Open land-use projects and hearings on or near the lot | `notices` |
| Neighborhood | Walking distance to the nearest subway entrance, school, grocery store and other destinations; school zones, parks, storefront vacancy, 311 rate | `lot_zones`, `places`, `lot_metrics` |
| Hazard | FEMA flags, evacuation zone, stormwater flooding | `lots`, `lot_zones` |

Guests see Identity, The lot, The building and Zoning. The other sections need an account (D18).
Every field carries its source dataset and pull date.
The card is built by one SQL view per section.
A test renders the card for a fixture lot and compares it to a committed expected file.

## How the old repo maps to the new one

Read the old module before writing its new counterpart.
Explain it in your own words first.

| New | Old | What changes |
|---|---|---|
| `datasets/base.py` | `datasets/base.py` | Four stages instead of eight; no territory |
| `sources/socrata.py` | `ingest/http.py` | HTTP split out of datasets |
| `datasets/pluto/` | `datasets/nyc/pluto/` and `ingest/nyc/pluto.py` | One release, not 24 |
| `datasets/acris_*` | `ingest/nyc/acris.py` | Since the start date plus the newest deed per lot, not 1966 onward |
| `export/` | `export/mapdb.py` | Same idea: a read-only copy for the API |
| `detect/` | `export/changes.py` | Changes feed a review queue, not a news strip |
| `api/` | `api/` | Fewer endpoints; lot card first |
| `agent/` | `narrator/` | Reviews sites against a profile; one provider |
| `web/` | `web/` | Next.js and React instead of Vite and vanilla TS; the old views show what each page does |
| `tiles/` | `map/tiles.py`, `map/tiles_wrapper.py` | Same tools |
