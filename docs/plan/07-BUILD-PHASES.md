# 07 — Build phases

Thirteen phases, in order: 0–10, plus 5.5 and 9.5.
The first delivery is Phases 0–9 with 5.5: the platform live as a portfolio piece (D21, [`00-INDEX.md`](00-INDEX.md) § Deliveries).
Phase 9.5 follows when consulting calls for it; Phase 10 over time.
Each ends with a checkpoint that shows real output ([`05-PROCESSES.md`](05-PROCESSES.md) § 2).
No phase starts until the one before it passes.

Each phase lists:

- **Goal:** what exists afterwards.
- **Builds:** the first instance of each pattern.
- **Then:** later instances of the same patterns.
- **Read first:** the old repo's version, to read before writing the new one.
- **Checkpoint:** the real run and what to look at.

Sizes are relative: S is a session or two, M is a few, L is a week or more of sessions.

---

## Phase 0 — Scaffold (S)

**Goal.** An empty project that installs, lints and tests.

**Already done (2026-10-28).** The git repo on GitHub, `.gitignore`, the folder layout, the root docs (`README.md`, `AGENTS.md`, `CLAUDE.md`, `SPEC.md`, `BRAND.md`), `specs/000-TEMPLATE.md` and `docs/decisions.md`.

**Builds.**
- `pyproject.toml`, `uv.lock` and `.python-version`, made with `uv init` and `uv add`.
- `src/meridian_dashboard_nyc/config.py`: the `data/` folder, the event-log start date (D2), and the keys from `.env`.
- `tests/test_config.py`: the first three tests.

**Read first.** Old `pyproject.toml`, `src/urban_metrics/config.py`.

**Checkpoint.**
- `uv run pytest` passes, and `uv run ruff check .` is clean.
- A fresh clone runs `uv sync` and `uv run pytest` with no other step.

---

## Phase 1 — The lot (L)

**Goal.** Every lot in the city, with its shape, in the warehouse. An address turns into a lot.

**Builds.**
- `runlog.py`: a context manager that times a step and appends one JSON line to `data/runs/`.
- A network-blocking test fixture in `tests/conftest.py`, before the first code that goes online.
- `sources/socrata.py`: metadata, paged query, bulk export, app token, retries.
- `datasets/base.py`: the `Dataset` class with `pull` and `land`, the manifest, the atomic `.partial` folder.
- `datasets/pluto/`: the first dataset, all four stages.
- `geo.py`: the measuring helper and its test.
- `docs/SCHEMA.md`: the `lots` table, column by column, after profiling PLUTO.
- `schema.py` and the test that checks it matches `SCHEMA.md`.

**Then.** `mappluto` (Bytes download), `pad`, `building_footprints`, `dtm_condos`, `dtm_condo_units`; `sources/bytes.py`; `sources/geosearch.py`.

**Read first.** Old `runlog.py`, the `no_network` fixture in `tests/test_narrator.py`, `datasets/base.py`, `datasets/manifest.py`, `ingest/http.py`, `datasets/nyc/pluto/pipeline.py`, `ingest/nyc/README.md` (condo handling).

**Checkpoint.**
- `lots` holds 858,284 rows (or today's count), version 26v2, every BBL unique.
- Every lot has a geometry; the count of invalid shapes is printed.
- `lookup "120 Broadway, Manhattan"` prints BBL `1000477501` and its row from `lots`.
- A condo unit BBL resolves to its billing lot.
- Open one borough's lots in QGIS or a quick map and look at it.

---

## Phase 2 — Zoning (M)

**Goal.** Each lot knows its zoning, overlays, special districts and restrictions, and its unused floor area.

**Builds.**
- `datasets/zoning_districts/`: a geodatabase with several layers into one `zones` table.
- `derive/lot_zones.py`: the first spatial join, in EPSG:2263 through `geo.py`.
- `derive/metrics.py`: the first metric, `unused_floor_area_sqft@v1`, with its docstring and `metric_meta` row.

**Then.** `zoning_tax_lots`, `mih_areas`, `inclusionary_housing_areas`, `transit_zones`, `e_designations`, `landmark_sites`, `historic_districts`, `lpc_buildings`.

**Read first.** Old `datasets/nyc/zoning_districts/`, `ingest/nyc/zoning.py`, `metrics/form.py` (`far_utilization`).

**Checkpoint.**
- Five lots you pick: their zoning card printed beside ZoLa's page for each. They match.
- Count of lots with at least 5,000 sq ft unused floor area, by borough.
- Count of lots where `zoning_tax_lots` and PLUTO disagree on the first district, with five examples explained.

---

## Phase 3 — Ownership, money and activity (L)

**Goal.** Each lot knows its last sale, its assessed value, its tax benefits, and what is being filed or built on it.

**Builds.**
- The ACRIS spec first: the bulk first pull, then the incremental pull by recorded date ([`01-data-sources/raw.md`](01-data-sources/raw.md)).
- `datasets/acris_master/` and the `documents` and `sales` tables, with the market-sale flag.
- The unified `filings` table from the first DOB dataset.

**Then.** `acris_legals`, `acris_parties`, the two code tables, `rolling_sales`, `property_valuation`, `property_exemptions`, `property_abatements`, `tax_lien_sale_list`, the other three DOB filing and permit datasets, both certificate datasets, `housing_database`, `affordable_housing`; the `open_charges` live lookup.

**Read first.** Old `ingest/nyc/acris.py`, `ingest/nyc/permits.py`, `ingest/nyc/dob_now.py`, `docs/research/profiles/nyc/acris-master.md`.

**Checkpoint.**
- Five lots: last sale and price beside the ACRIS document search for each.
- Market sales in the last 12 months by borough, beside the count from `rolling_sales`.
- New-building and demolition filings in the last 30 days, by borough, beside DCP's housing database.
- Disk used by `data/` printed.

---

## Phase 4 — Condition, compliance and notices (M)

**Goal.** Each lot knows what is wrong with its buildings and what public process touches it.

**Builds.** The unified `violations` table from `hpd_violations`, then the first notice source, `zap_projects`.

**Then.** Every other Group E and F dataset in `sources.md`.

**Read first.** Old `datasets/nyc/zap_projects/`, `datasets/nyc/city_record/`, `datasets/notices.py`, spec S052's changelog (what the real pull proved wrong).

**Checkpoint.**
- The full lot card printed for five lots: one vacant lot, one walk-up, one tower, one city-owned lot, one lot with an open ZAP project.
- Each card checked against HPD Online, DOB BIS or DOB NOW, and ZAP.
- Open violations by agency and class, citywide.

---

## Phase 5 — Neighborhood and hazard (L)

**Goal.** Each lot knows its districts, school zones, walking distance to transit and other destinations, nearby places and hazards.

**Builds.** `subway_entrances`; `network/`: the OpenStreetMap walking graph for the five boroughs and the metric `walk_distance_to_subway_m@v1` (D11).

**Then.** Every other Group G and H dataset; walking-distance metrics for the other destination kinds, once the spec names them.

**Read first.** Old `datasets/nyc/districts_admin/`, `datasets/nyc/facilities/`, `metrics/amenity.py`.

**Checkpoint.**
- The five lots' neighborhood sections, with the walking route to the nearest subway entrance drawn on a map for each, and its length checked against a map service's walking directions.
- 311 requests in the last 12 months per 1,000 lots, by community district.
- `make daily` runs end to end on every dataset so far and prints its total time.

---

## Phase 5.5 — Urban form, levels 1–5 (L)

**Goal.** Each lot and each neighborhood carries the first five levels of urban-form metrics in [`08-URBAN-FORM.md`](08-URBAN-FORM.md), ready for the dashboard in Phase 6.

**Decide first.** The ⚠ items in `08-URBAN-FORM.md`: walking speed, use classes.

**Builds.** `form/`: the registry and level 1 (lot and building basics), with its Plotly figure.

**Then.** Levels 2–5, one spec each, in order.

**Read first.** `08-URBAN-FORM.md`; the old repo's draft specs S029–S035 and research question Q47.

**Checkpoint.**
- Every level 1–5 metric printed for the five checkpoint lots and their neighborhoods, spot-checked against PLUTO, ZoLa or a map.
- One Plotly figure per level, rendered.
- `metric_meta` lists every metric with its grain and version.

---

## Phase 6 — Export, API, map and dashboard (L)

**Goal.** You open the dashboard, search an address, and see the lot on a map with its card.

**Builds.**
- `export/`: the read-only `nyc.duckdb`.
- `api/`: `GET /health` and `GET /lots/{bbl}`, with their Pydantic models.
- `web/`: the shell, `tokens.css`, the map page with the lots layer, the lot page.

**Then.** The other endpoints in [`01-data-sources/api.md`](01-data-sources/api.md) Part 2; the other layers; the data page; neighborhood search on the map (D17); a metric picker on the map and the Stats page that lists `metric_meta`.

**Decide first.** D5 (dashboard approach) and D10 (visual style).

**Read first.** Old `export/mapdb.py`, `api/app.py`, `api/models.py`, `map/tiles.py`, `web/src/` (shell and map views). The brand: `brand-guidelines.md` §§ 4.5 and 11 in the `meridianxyz_website` repo.

**Checkpoint.**
- Screenshots: the map at city scale, one lot selected with its card, the data page with every dataset's freshness.
- The API's `/docs` page lists every endpoint.
- Playwright tests pass.
- A filtered URL and a lot URL each return the static page with no server render; `robots.txt` disallows both.

---

## Phase 7 — Change detection and the site queue (M)

**Goal.** After each refresh, the project knows what is new and queues it.

**Builds.** `appdb/`: Postgres in Docker, its first migration and `site_queue` (D19). Then `detect/` for one dataset (DOB filings): `changes`, then the `demolition_filed` trigger into `site_queue`.

**Then.** The other triggers in [`06-SITE-REVIEW-AGENT.md`](06-SITE-REVIEW-AGENT.md) § 4; `prune` as the last step of `make daily` (D3); lasso search and saved areas (`POST /areas`, D17), which need the app database.

**Decide first.** D3 (pulls kept) and D8 (triggers).

**Read first.** Old `export/changes.py`, `ingest/refresh.py`, spec S053.

**Checkpoint.**
- Two real daily refreshes, a day apart.
- The queue after the second: count per trigger, and ten rows you open on the city's sites to confirm each trigger is real.
- After a third refresh, `data/raw/` still holds two pulls per dataset.

---

## Phase 8 — The review agent (L)

**Goal.** Each queued site gets a stored review against each interested profile.

**Before it starts.** Write the first one or two buyer profiles (D7).

**Builds.**
- 8a: profile loading (YAML into the app database), the screens in SQL, screened-out reviews. No model.
- 8b: the manual tool loop and the first two tools, tested on recorded responses.
- 8c: the `Review` model, the structured final call, the eval suite.

**Then.** The other tools; 8d, the nightly batch path and the `run_sql` tool.

**Read first.** Old `narrator/` (loop, providers, tools), spec S050 (why text-to-SQL, how the risk is held).

**Checkpoint.**
- Ten real reviews of real new sites, read by you, each marked right, wrong or unclear.
- The eval suite passes; the live eval's cost is printed.
- Measured cost per review, interactive and batch.
- The eval on Opus 5.5 at `medium` and `low` effort and on Sonnet 5.5: pass rate and cost side by side, for the D9 review.

---

## Phase 9 — The inbox, the review pages and going live (L)

**Goal.** Each morning's digest is in the inbox; the dashboard shows the queue and the reviews; the site is live, with the private pages behind sign-in.

**Uses.** D6 (hosting) and D16 (Auth.js with Google and GitHub), both decided.

**Builds.** 9a: the digest and the Inbox page, plain text first.

**Then.** 9b: the Sites, Review, Stats and Profiles pages. 9c: the move to the VM, Vercel and R2 (D6); sign-in for you as owner (D16). Sign-up for everyone else waits for Phase 9.5.

**Checkpoint.**
- A real digest on the Inbox page, screenshotted.
- An address submitted from the dashboard, reviewed within minutes.
- The injection test notice produces a normal review and nothing else.
- The scheduled `make daily` ran unattended on the VM for three days in a row; its run log shows each step's time.
- Signed out, the Inbox page and `GET /inbox` both refuse; the map and a guest lot card load.

---

## Phase 9.5 — Accounts and payments (later)

**Goal.** Other people can sign up and use the platform with their own profiles and Inbox (D18, D20).

Planned in the owner's private notes. Its specs are written when it starts, after the first delivery (D21).

---

## Phase 10 — Optional depth

Pick from these only after Phase 9 has run for a few weeks.

- Email subscriptions: the daily digest sent to a personal address (D4, D12).
- Census tract demographics.
- Subway frequency from GTFS.
- Estimated Local Law 97 exposure, as a versioned metric with its own spec.
- Urban form levels 6–9 ([`08-URBAN-FORM.md`](08-URBAN-FORM.md)), one level at a time.
- A second city, with its own dataset packages and database (D13).

---

## Summary

| Phase | Size | Ends with |
|---|---|---|
| 0 Scaffold | S | Green tests and lint |
| 1 The lot | L | 858k lots; an address becomes a lot |
| 2 Zoning | M | Zoning cards match ZoLa |
| 3 Ownership, money, activity | L | Sales and filings match ACRIS and DOB |
| 4 Condition and notices | M | Five full lot cards, checked |
| 5 Neighborhood and hazard | L | `make daily` end to end; walking distances for every lot |
| 5.5 Urban form | L | Five levels of form metrics for every lot and neighborhood |
| 6 Export, API, dashboard | L | The dashboard on screen |
| 7 Change detection | M | A real queue of new sites |
| 8 Review agent | L | Ten real reviews read by you |
| 9 Inbox, pages, live | L | A digest on the Inbox page of the live site |
| 9.5 Accounts and payments | — | Planned privately |
| 10 Optional | — | — |
