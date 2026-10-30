# SPEC: the build plan

Every spec in build order, with the tests that prove it works, the checks on real data, and what it documents.
The first delivery is S001 to S055: Phases 0 to 9, live as a portfolio platform (D21).

This file is the order of work.
The plan behind it is in [`docs/plan/`](docs/plan/00-INDEX.md).
Each spec's own file in `specs/` holds its detail and its status line.
If this file and a spec disagree, the spec wins and this file is corrected in the same commit.

## Starting a session

Open a new chat in the repo root and say:

> Read AGENTS.md and SPEC.md. We are on S0NN. Draft its spec from specs/000-TEMPLATE.md, or open it if it exists, and walk me through it before any code.

The current spec is the first whose status is not `done`.
Before S001 exists, the current spec is S001.

## The loop for every spec

```
draft spec ──▶ owner accepts ──▶ tests (fail) ──▶ code (tests pass, lint clean) ──▶ checks ──▶ document ──▶ status: done
```

1. **Draft.** Claude drafts the spec from `specs/000-TEMPLATE.md` and the plan sections listed below. Status `draft`.
2. **Accept.** The owner reads it, settles its ⚠ items, and sets it to `accepted`.
3. **Tests first.** One test per acceptance criterion, named `test_s<nnn>_c<n>_<what>`. They fail before the code exists. Status `in progress`.
4. **Code.** Until the tests pass and `uv run ruff check .` is clean.
5. **Checks.** The real run on real data, compared against an independent source.
6. **Document.** The spec's changelog, the READMEs and `docs/SCHEMA.md` it touches, and the phase's checkpoint note when it closes a phase.
7. **Done.** The status moves to `done` in the same commit as the last change.

## Test layers

| Layer | Tool | When it runs | What it covers |
|---|---|---|---|
| Unit | `pytest` with real-row fixtures (at most 20 rows a dataset) | Every commit, offline, under 30 seconds | Stage logic, mappings, filters, metrics, rules |
| Contract | `pytest` | Every commit | `docs/SCHEMA.md` against `schema.py`; the API's OpenAPI schema against a snapshot; the generated TypeScript client against the schema |
| Golden | `pytest` with committed expected files | Every commit | The lot card, the digest, Plotly figure JSON |
| Database | `pytest -m db` against Postgres in Docker | Every commit, with Postgres running in Docker | Migrations, the app tables, the queue and reviews (from S043) |
| Real data | `pytest -m real` | On request and at every checkpoint | Counts, key uniqueness and geometry validity on full pulls |
| Browser | Playwright, with axe for accessibility | The web test command (from S041) | Each page loads, draws, and its main action works; keyboard reachable; no serious axe findings |
| Agent | Recorded-response replays; a live eval on request | Replays every commit; live after any prompt or profile change | Screens, numbers, citations, forbidden phrases, injection |
| CI | GitHub Actions | Not planned. The owner can add it later, for example before going live (S055) | Lint, the offline and database suites, the TypeScript typecheck |

## Checks

A check is a real run whose output a person looks at, compared against something the project did not produce:

| To check | Compare against |
|---|---|
| A lot's zoning | ZoLa (`zola.planning.nyc.gov`) |
| Filings, violations, certificates | DOB BIS and DOB NOW |
| HPD violations and registrations | HPD Online |
| A sale or a deed | ACRIS document search |
| Assessed value | DOF property tax bills |
| Row counts | The source's own `count(*)` ([`api.md`](docs/plan/01-data-sources/api.md)) |
| A walking distance | A map service's walking directions |

## Documenting the build

Every phase closes with a checkpoint note in `docs/checkpoints/`, named `P<phase>-<yyyy-mm-dd>.md` (`P5.5-...` for Phase 5.5).
The format is in [`docs/checkpoints/README.md`](docs/checkpoints/README.md): the specs covered, the exact commands, the outputs, what they were compared against, what broke, and the decision to continue.
Screenshots go in `docs/checkpoints/img/`.
Together the notes are the build's record: what was built, how it was verified, and when.

Each spec also leaves:

- its changelog, with what the real run proved wrong;
- the dataset README for every dataset it lands (profile, measured sizes, quirks);
- the `docs/SCHEMA.md` entries for every table or column it adds, written before the code.

---

## Phase 0: Scaffold

The repo, its folders, `.gitignore` and the root docs already exist (2026-10-28).

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S001 | Scaffold: install, lint, test | [07](docs/plan/07-BUILD-PHASES.md) Phase 0; [02](docs/plan/02-TECH-STACK.md); [04](docs/plan/04-CODING-STANDARDS.md) | D1, D2 |

**Builds.** `pyproject.toml`, `uv.lock` and `.python-version`; the ruff and pytest settings; `config.py` (the `data/` folder, the event-log start date 2025-01-01, the keys from `.env`); the README section "Getting started".

**Tests.**
- `test_s001_c1_paths_live_under_data`
- `test_s001_c2_event_log_start_is_2025_01_01`
- `test_s001_c3_env_values_come_through_config`

**Checks.**
- `uv run pytest` passes. `uv run ruff check .` and `uv run ruff format --check .` are clean.
- A fresh clone runs `uv sync` and `uv run pytest` with no other step.

**Documents.** `README.md` Getting started, checked command by command; `docs/checkpoints/P0-<date>.md`.

**Done when** a fresh clone installs, passes its tests and is clean under lint.

---

## Phase 1: The lot

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S002 | Dataset framework and the Socrata client | [raw.md](docs/plan/01-data-sources/raw.md); [api.md](docs/plan/01-data-sources/api.md) Part 1 | D2, D3 |
| S003 | PLUTO, the `lots` table and the schema contract | [sources.md](docs/plan/01-data-sources/sources.md) § A; [05](docs/plan/05-PROCESSES.md) § 5 | |
| S004 | `geo.py`, the measuring helper | [04](docs/plan/04-CODING-STANDARDS.md) Data rules | D11 |
| S005 | MapPLUTO and the DCP Bytes client | sources § A | |
| S006 | PAD and building footprints | sources § A | |
| S007 | Condos: billing and unit lots | sources § A (condo note) | |
| S008 | GeoSearch and `lookup` | api.md § 1.3 | |

**Tests.**
- S002: a test that calls `httpx.get` fails with the network block's message; a timed step appends one JSON line to `data/runs/`, also when it fails; paging stops at the last page; 429 and 5xx retry with backoff; the app token is sent and never logged (all on recorded responses); a pull writes into `<date>.partial/` and renames only when every file is hashed; a failed pull leaves earlier pulls untouched; every stage run appends to `manifest.json`, success or failure; an unchanged input writes `unchanged` and exits in under a second; `_source.json` records the URL, the query and each file's hash; `all` runs in dependency order and stops at the first failure, naming the dataset.
- S003: landing types are pinned and column names lowercased; a duplicate BBL fails `clean` and names the first duplicate; every dropped row reaches the rejects file with a reason; `load` writes exactly the `SCHEMA.md` columns, in order; `schema.py` matches `SCHEMA.md`; the PLUTO version is recorded.
- S004: a 100 ft square measures 10,000 sq ft in EPSG:2263; a point survives the 4326 to 2263 round trip; a scan finds no area, length or distance call outside `geo.py`.
- S005: the zip's hash is recorded; geometry is reprojected to 4326 at `land`; a MapPLUTO version that differs from PLUTO's fails with both versions named; invalid shapes are counted and flagged, never dropped.
- S006: PAD ranges load into `addresses`; footprints load into `buildings` by BIN.
- S007: a unit BBL resolves to its billing BBL.
- S008: a match without a BBL is refused; a cached address makes no second call; `lookup` prints the matched address back.

**Checks.**
- `lots` holds 858,284 rows (or the day's count), version 26v2, every BBL unique.
- Every lot has a geometry; the count of invalid shapes is printed.
- `lookup "120 Broadway, Manhattan"` prints BBL `1000477501` and its `lots` row.
- A condo unit BBL resolves to its billing lot.
- One borough's lots viewed on a map.

**Documents.** READMEs for the six datasets, each with its profile and measured sizes; `SCHEMA.md` for `lots`, `buildings`, `addresses`, `condo_units`; the condo rule, written before any sale is joined; `P1-<date>.md`.

**Done when** an address becomes a lot with its shape.

---

## Phase 2: Zoning

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S009 | Zoning districts into `zones` | sources § B | |
| S010 | `lot_zones`: the first spatial join | [03](docs/plan/03-ARCHITECTURE.md) tables | |
| S011 | The metric framework and `unused_floor_area_sqft@v1` | 04 Docstrings; 03 tables | |
| S012 | The rest of Group B and `lot_restrictions` | sources § B | |

**Tests.**
- S009: every layer of the geodatabase lands with its `kind`; invalid polygons are flagged.
- S010: a fixture lot inside a known district gets that district; the join runs in EPSG:2263 through `geo.py`.
- S011: the metric matches a hand-computed value on fixture lots; its docstring says what it does not measure; it writes one `metric_meta` row with grain and version; computing it twice gives the same table.
- S012: e-designations and landmark sites land in `lot_restrictions`; historic districts land as zones.

**Checks.**
- Five lots' zoning cards beside ZoLa's pages; they match.
- Lots with at least 5,000 sq ft of unused floor area, by borough.
- Lots where `zoning_tax_lots` and PLUTO disagree on the first district, with five explained.

**Documents.** `SCHEMA.md` for `zones`, `lot_zones`, `lot_restrictions`, `lot_metrics`, `metric_meta`; dataset READMEs; `P2-<date>.md`.

---

## Phase 3: Ownership, money and activity

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S013 | ACRIS: bulk first pull, incremental pulls, `documents` | raw.md (ACRIS); sources § C | D2, D8, ⚠ market-sale rule |
| S014 | Sales: ACRIS deeds and rolling sales into `sales` | sources § C | D8 |
| S015 | Valuation, exemptions, abatements, the lien list | sources § C | |
| S016 | DOB filings and permits into `filings` | sources § D | D2 |
| S017 | Certificates of occupancy | sources § D | D2 |
| S018 | The housing pipeline | sources § D | |
| S019 | The `open_charges` live lookup | api.md | |

**Tests.**
- S013: the three ACRIS tables join on `document_id`; an incremental pull takes only documents recorded since the last pull; a lot whose only deed is from 1998 keeps it as its newest deed; an older deed that is not the newest and predates the start date is dropped; moving the start date in config changes what is kept.
- S014: buyer and seller names are kept as recorded; `buyer_is_company` is set by name suffix (LLC, Inc, LP, Corp, ...); a $0 or $10 deed is flagged non-market and kept.
- S015: the newest tax year and the newest lien cycle are kept; the lien flag lands on the lot.
- S016: all four sources map into one `filings` shape with a `system` column; an open job is kept whatever its age.
- S017: every building keeps its newest certificate, plus every certificate since the start date.
- S019: the lookup runs on a recorded response and lands nothing.

**Checks.**
- Five lots' last sale and price beside ACRIS document search.
- Market sales in the last 12 months by borough, beside the `rolling_sales` count.
- New-building and demolition filings in the last 30 days, by borough, beside DCP's housing database.
- Disk used by `data/`, printed.

**Documents.** The ACRIS spec itself, before any code; `SCHEMA.md` for `documents`, `sales`, `assessments`, `tax_benefits`, `filings`, `certificates`, `pipeline`; READMEs with measured sizes; `P3-<date>.md`.

---

## Phase 4: Condition, compliance and notices

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S020 | `violations`: HPD, DOB, ECB, safety | sources § E | ⚠ DOB and ECB keep filters, confirmed at profile |
| S021 | HPD registrations, vacate orders, AEP, speculation watch list | sources § E | |
| S022 | DOB complaints, stalled sites, facades, LL84 energy | sources § E | D2 |
| S023 | Notices: ZAP, City Record, city-owned property | sources § F | D2 |
| S024 | The lot card, version 1 | 03 The lot card | |

**Tests.**
- S020: only open violations land; agency and class map to canonical values.
- S021: a vacate order with a rescind date is not open; AEP and speculation flags land on the lot.
- S023: City Record keeps four sections and only notices not yet ended; ZAP keeps open projects plus those completed since the start date; `zap_bbls` links projects to lots.
- S024: one SQL view per card section; the card for a fixture lot matches its golden file; every field carries its dataset and pull date.

**Checks.**
- The full lot card for five lots: a vacant lot, a walk-up, a tower, a city-owned lot, a lot with an open ZAP project.
- Each card checked against HPD Online, DOB BIS or DOB NOW, and ZAP.
- Open violations by agency and class, citywide.

**Documents.** `SCHEMA.md` for `violations`, `registrations`, `complaints`, `energy`, `notices`; the lot card's section list; `P4-<date>.md` with the five cards.

---

## Phase 5: Neighborhood, hazard and walking

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S025 | Boundaries and districts, school zones | sources § G | D17 (NTAs) |
| S026 | Places: subway, parks, facilities, storefronts, licenses | sources § G | |
| S027 | 311 requests and collisions | sources § G | D2, ⚠ 311 complaint types |
| S028 | Hazard: evacuation zones, stormwater flooding | sources § H | |
| S029 | The walking network and `walk_distance_to_subway_m@v1` | sources § I; 04 Data rules | D11 |
| S030 | Walking distances to the other destinations | sources § G notes | D11, ⚠ destination kinds |
| S031 | `make daily`, version 1 | 05 § 6 | D3 |

**Tests.**
- S025: every boundary set lands as zones; each lot gets its NTA and community district.
- S027: 311 is filtered at pull from the start date in config; only the chosen complaint types land; collisions land in the table `SCHEMA.md` names first.
- S029: on a five-node fixture graph, shortest walking distances are exact; a lot snaps to its nearest walkable node; an unreachable lot gets `NULL`, never `0`; edge lengths are computed in EPSG:2263 through `geo.py`; the graph saves and reloads unchanged; the OSM attribution text exists.
- S031: a dataset is pulled only when its cadence says it is due and its source has changed; the run stops at the first failure and names the dataset; every step writes a `runlog` line.

**Checks.**
- For the five lots, the walking route to the nearest subway entrance drawn on a map, its length checked against a map service's walking directions.
- The share of lots with a walking distance, and the median by borough.
- 311 requests in the last 12 months per 1,000 lots, by community district.
- `make daily` runs end to end and prints its total time.

**Documents.** The network README (OSM extract date, graph size, memory used); `SCHEMA.md` for `places` and the new zone kinds; `P5-<date>.md`.

---

## Phase 5.5: Urban form, levels 1 to 5

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S032 | The form registry and level 1: lot and building basics | [08](docs/plan/08-URBAN-FORM.md) | D15 |
| S033 | Level 2: building geometry | 08 | D15 |
| S034 | Level 3: density and use mix | 08 | ⚠ use classes |
| S035 | Level 4: street network form | 08 | D11 |
| S036 | Level 5: walking access | 08 | ⚠ walking speed |

**Tests.**
- S032: levels run in order; each metric writes its `metric_meta` row with grain, inputs and version; lot metrics match hand-computed values on fixture lots; NTA summaries aggregate correctly on a fixture; the level's Plotly figure validates and carries no colors.
- S033: a square footprint has the known compactness; footprint coverage never exceeds 1 without a flag.
- S034: a fixture with equal floor area in each use reaches the maximum mix entropy.
- S035: intersection density and node degree are exact on the fixture graph.
- S036: destination counts within 5, 10 and 15 minutes are exact on the fixture graph at the configured speed.

**Checks.**
- Every level 1 to 5 metric for the five checkpoint lots and their neighborhoods, spot-checked against PLUTO, ZoLa or a map.
- Three metrics mapped citywide and looked at for artifacts.
- One rendered figure per level.

**Documents.** The levels marked done in `08-URBAN-FORM.md`; metric docstrings; figures in `docs/checkpoints/img/`; `P5.5-<date>.md`.

---

## Phase 6: Export, API, map and dashboard

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S037 | The export, `nyc.duckdb` | 03 The chain | |
| S038 | API core: `/health`, `/lots/{bbl}` | api.md Part 2 | D16 |
| S039 | API: datasets, lookup, lot search, results, comparables | api.md Part 2 | D17 |
| S040 | Map tiles: PMTiles for lots and layers | 02 Map and dashboard | D6 |
| S041 | The web shell, the map page and the lot page | 02; 04 TypeScript; [BRAND.md](BRAND.md) | D5, D10, ⚠ brand open items |
| S042 | Data page, neighborhood search, metric picker, Stats, crawler rules | 02 Crawlers; 06 § 11 | D5, D17 |

**Tests.**
- S037: the export opens read-only and a write fails; it holds only the tables the API reads.
- S038: every response is a Pydantic model; the OpenAPI schema matches its snapshot; `/lots/{bbl}` returns the card matching the golden file; a guest gets only the identity, lot, building and zoning sections.
- S039: comparables default to the lot's NTA; each comp's metric differences match a fixture computed in SQL; a 40,000-lot search returns a count, a sample and a result id; the CSV download matches the result; a burst of requests is rate-limited.
- S041: `pnpm typecheck` passes with `strict`; the generated API client matches the schema, or CI fails; the map page draws the lots layer; colors come from `tokens.css` and no component holds a hex literal; both themes render; the OSM credit shows wherever a walking distance does.
- S042: Playwright: each page loads, draws and its main action works; axe finds nothing serious; `next build` reports filtered views and the lot page as static; `robots.txt` disallows query strings and lot pages and allows the docs page.

**Checks.**
- Screenshots in light and dark: the map at city scale, one lot selected with its card, the data page with every dataset's freshness.
- The API's `/docs` page lists every endpoint.
- A filtered URL and a lot URL each return the static page with no server render.

**Documents.** The API's endpoint list; `web/README.md`; screenshots; `P6-<date>.md`.

---

## Phase 7: The app database and change detection

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S043 | The app database: Postgres, migrations, `site_queue` | 03 App tables | D19 |
| S044 | `detect`, `changes` and the `demolition_filed` trigger | raw.md; 06 § 4 | D3, D8 |
| S045 | The other eleven triggers and the watchlist | 06 § 4 | D8 |
| S046 | Lasso search and saved areas | api.md; 06 § 7 | D17 |
| S047 | `make daily`, version 2: export, tiles, detect, prune | 05 § 6 | D3 |

**Tests.**
- S043 (`-m db`): migrations apply in order to an empty database and twice without change; `site_queue` matches `SCHEMA.md`.
- S044: two fixture pulls give the right `added`, `removed` and `changed` rows; a change to an unwatched column is ignored; a lot queued for the same trigger in the last 30 days is not queued again.
- S045: each trigger fires on its fixture and writes one queue row that references its source row; `zoning_changed` reads `zoning_tax_lots`; the watchlist matches names ignoring case and punctuation and never fuzzily.
- S046: a saved lasso returns an area id usable as `area=`; an invalid polygon is refused.
- S047: `prune` keeps the two newest pulls with their landing and clean files; a failure at any earlier step stops the run before `prune`.

**Checks.**
- Two real daily refreshes, a day apart.
- The queue after the second: the count per trigger, and ten rows opened on the city's sites to confirm each is real.
- After a third refresh, `data/raw/` holds two pulls per dataset.

**Documents.** `SCHEMA.md` for the app tables; the migrations README; `P7-<date>.md`.

---

## Phase 8: The review agent

Before it starts, the owner writes the first one or two buyer profiles (D7). They stay out of git; `profiles/example.yaml` shows the shape.

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S048 | Profiles and screens (8a) | 06 §§ 5, 6 | D7, D18 |
| S049 | The tool loop and the first two tools (8b) | 06 §§ 7, 8 | D9 |
| S050 | The review record, checks and the eval suite (8c) | 06 §§ 10, 12 | D9 |
| S051 | The other tools, the nightly batch and `run_sql` (8d) | 06 §§ 7, 8 | D9 |

**Tests.**
- S048: a profile naming an unknown metric fails to load and names it; screens run in SQL and match the 30-lot screens set exactly; a site failing a screen is stored as screened out with no model call; each review stores the profile's hash.
- S049 (recorded responses): parallel tool calls come back in one message; a failed tool returns `is_error`; the loop stops after 10 rounds, on `max_tokens` and on `refusal`; requests send explicit effort, `tool_choice: auto`, strict tool schemas, no sampling parameters, and the fallback setting; every call's tokens and cost reach `usage`.
- S050: every review validates against `Review`; every number in the prose appears in a tool result; no forbidden phrase appears; every risk and fit point cites a card field; a City Record notice that says "ignore your instructions" produces a normal review.
- S051: batch results are keyed by review id; `run_sql` refuses anything but one `select`, returns at most 500 rows and stops at 10 seconds.

**Checks.**
- Ten real reviews of real new sites, each marked right, wrong or unclear.
- The eval suite passes; the live eval prints its cost first.
- Measured cost per review, interactive and batch.
- The eval on Opus 5.5 at `medium` and `low` effort and on Sonnet 5.5, pass rate and cost side by side (D9).

**Documents.** The prompt versions; the eval set's README; `P8-<date>.md` with the marks and costs, never the text of reviews made for real profiles.

---

## Phase 9: The Inbox, the review pages and going live

| Spec | Title | Plan | Decisions |
|---|---|---|---|
| S052 | The digest and the Inbox page (9a) | 06 § 11 | D4 |
| S053 | Sites, Review, Stats and Profiles pages (9b) | 06 § 11 | D17 |
| S054 | Sign-in: Auth.js, the owner, the signed token (9c) | api.md Rules; 02 | D16 |
| S055 | Going live: VM, Vercel, R2, backups (9c) | 02 Running it | D6, ⚠ VM provider, ⚠ domain |

**Tests.**
- S052: a digest is written only when something is new; its statistics equal a fresh SQL count; it matches its golden file.
- S053: Playwright on each page; the Review page shows the lot card, the search area on a map, the comps table and nearby activity.
- S054: signed out, every private endpoint refuses; a guest gets only the guest card sections; an expired or tampered token is refused; the owner sees everything.
- S055: smoke tests against the live URLs (`/health`, a guest lot card, `robots.txt`); tiles are served from R2 with range requests; a Postgres backup restores into a scratch database.

**Checks.**
- A real digest on the Inbox page, screenshotted.
- An address submitted from the dashboard, reviewed within minutes.
- The injection test notice produces a normal review and nothing else.
- `make daily` ran unattended on the VM three days in a row; its run log shows each step's time.
- Signed out, the Inbox page and `GET /inbox` refuse; the map and a guest lot card load.

**Documents.** `docs/RUNBOOK.md` (deploy, restore, rotate a key); the live link in `README.md`; `P9-<date>.md`.

**The first delivery is done** when the P9 checkpoint passes.

---

## After the first delivery

- **Phase 9.5, accounts and payments.** Specs are written when the phase starts, from the owner's private notes (D18, D20).
- **Phase 10, over time.** Each item gets its own spec when picked: email subscriptions (D4, D12), census demographics (D14), subway frequency from GTFS, LL97 exposure, urban-form levels 6 to 9 ([08](docs/plan/08-URBAN-FORM.md)), a second city (D13).

## Open ⚠ items by spec

| Spec | Item |
|---|---|
| S013 | The market-sale rule |
| S020 | The DOB and ECB keep filters, confirmed at profile |
| S027 | The 311 complaint types the reviews use |
| S030 | The destination kinds |
| S034 | Which PLUTO use classes count as which use |
| S036 | Walking speed (proposed 80 m a minute) |
| S041 | Brand open items: wordmark casing, square corners, nav icons ([BRAND.md](BRAND.md)) |
| S055 | The VM provider and the domain |
