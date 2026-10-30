# meridian-dashboard-nyc

Every current NYC dataset that describes a tax lot, in one place: on a map, in a lot card, measured for urban form, and watched every day for sites that just became interesting.

**Status:** Phase 0 is done. The project installs, lints and tests, and the build continues with S002. Progress is tracked spec by spec in [`SPEC.md`](SPEC.md), and each phase's checkpoint is written up in [`docs/checkpoints/`](docs/checkpoints/).

## What it does

1. **Lands the city's current record of every lot** into one DuckDB database. That covers 71 datasets from NYC Open Data, NYS Open Data and City Planning: PLUTO, zoning, sales and deeds, assessments, permits, violations, public notices and the neighborhood around each lot.
2. **Shows it** on a map and a dashboard, with one lot card per lot and comparable sales by neighborhood.
3. **Measures urban form.** Lot and building form, density and use mix, street-network form, and walking access, all measured along the OpenStreetMap walking network.
4. **Reviews new sites.** After each daily refresh, it finds lots that just changed (a demolition filing, a sale, a rezoning, a lien-sale listing), screens each against a buyer's stated criteria in SQL, and has Claude write a short review. The results land in an Inbox on the dashboard.

It describes the city as it stands today. It does not keep history beyond a fixed start date, and it never tells anyone to buy.

## Built with

| Layer | Tools |
|---|---|
| Data | Python 3.12, `uv`, DuckDB (spatial), Parquet, GeoPandas, `osmnx` |
| App database | Postgres |
| API | FastAPI, Pydantic |
| Dashboard | Next.js, React, TypeScript, deck.gl over MapLibre, PMTiles, TanStack Query, Zustand, Plotly |
| Agent | The Anthropic Python SDK, Claude Opus 5.5 |
| Hosting (from Phase 9) | A small VM for the pipeline, API and database; Vercel for the site; Cloudflare R2 for map tiles |

Why each tool was chosen: [`docs/plan/02-TECH-STACK.md`](docs/plan/02-TECH-STACK.md).

## Repo layout

```
.
├── README.md  AGENTS.md  CLAUDE.md  SPEC.md  BRAND.md
├── docs/
│   ├── plan/            the plan: data sources, stack, architecture, standards, processes, agent, phases, urban form
│   ├── decisions.md     every owner decision, dated
│   ├── SCHEMA.md        the canonical tables
│   └── checkpoints/     one write-up per phase checkpoint
├── specs/               one spec per unit of work, in build order
├── src/meridian_dashboard_nyc/
│   ├── config.py        paths, the event-log start date, the keys from .env
│   │                    each folder below arrives with the spec that first needs it
│   ├── sources/         HTTP clients
│   ├── datasets/        one package per dataset: pull, land, clean, load
│   ├── derive/          lot metrics and spatial joins
│   ├── network/         the walking network and walking distances
│   ├── form/            urban-form metrics, level by level
│   ├── export/          the read-only database the API reads
│   ├── detect/          what changed since the last pull
│   ├── appdb/           the app database
│   ├── agent/           the site-review agent
│   ├── digest/          the daily Inbox digest
│   ├── api/             the FastAPI app
│   └── tiles/           map tiles
├── profiles/            buyer profiles (only example.yaml is committed)
├── tests/
└── web/                 the Next.js dashboard (from S041)
```

## Getting started

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs Python 3.12 and every package for you.

```bash
git clone https://github.com/jeremycburke/meridian-dashboard-nyc.git
cd meridian-dashboard-nyc
cp .env.example .env      # then fill in the keys you need; the tests need none
uv sync                   # Python 3.12 and every package in uv.lock
uv run pytest             # the tests
uv run ruff check .       # lint
uv run ruff format .      # format
```

## How the work is done

- **Spec first.** No code without a spec in `specs/`, and no spec without tests that prove it ([`SPEC.md`](SPEC.md)).
- **Checkpoints on real data.** Every phase ends with a real run compared against an independent source: ZoLa, ACRIS, DOB, HPD, a map.
- **Decisions are the owner's.** Every one is logged in [`docs/decisions.md`](docs/decisions.md) with its reason.
- **Agents follow** [`AGENTS.md`](AGENTS.md).

Start reading at [`docs/plan/00-INDEX.md`](docs/plan/00-INDEX.md).

## Data and credits

- Data from [NYC Open Data](https://opendata.cityofnewyork.us/), [NYS Open Data](https://data.ny.gov/) and NYC Department of City Planning ([BYTES of the BIG APPLE](https://www.nyc.gov/site/planning/data-maps/open-data.page)). The project describes these records as published and makes no claim beyond them.
- Walking network © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors, available under the Open Database License.
- Map basemap from [Protomaps](https://protomaps.com/).

## License

No license has been granted yet. You are welcome to read the code; reusing it needs permission.
