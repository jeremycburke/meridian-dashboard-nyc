# AGENTS.md

How any coding agent works in this repo: Claude Code (through `CLAUDE.md`), or any other tool that reads `AGENTS.md`.

## What this is

An NYC parcel-data platform, current state only.
It lands every current NYC dataset that describes a lot into DuckDB, shows it on a map and a dashboard, computes urban-form metrics, and runs a site-review agent that reports new sites to an Inbox on the dashboard.
Explain each change before you make it.
The owner reviews every change before it merges.

## Before you change anything

1. Open [`SPEC.md`](SPEC.md). The current spec is the first one whose status is not `done`. Each spec file in `specs/` shows its status under its title.
2. Read that spec in `specs/` and the plan sections it cites.
3. No spec for the work? Stop. Draft one from `specs/000-TEMPLATE.md` and wait for the owner to accept it.

## Keep it simple

- Write plain code: short modules, module-level constants, plain functions, the most common library for each job.
- Add a library, a tool or a safeguard in the spec that first needs it, never earlier.
- Comment only where the reason is not obvious from the code.
- Handle an exception only when the code can do something about it.

## Where the truth lives

| File | Holds |
|---|---|
| [`SPEC.md`](SPEC.md) | The build order: every spec, its tests, its checks, what it documents |
| [`docs/plan/00-INDEX.md`](docs/plan/00-INDEX.md) | The plan's map, the deliveries and the decisions |
| [`docs/decisions.md`](docs/decisions.md) | One line per owner decision, dated |
| [`docs/SCHEMA.md`](docs/SCHEMA.md) | The canonical tables. A table or column not there does not exist |
| [`docs/plan/01-data-sources/`](docs/plan/01-data-sources/) | Every dataset, how it is stored, how it is fetched |
| [`BRAND.md`](BRAND.md) | The dashboard's design rules and tokens |
| [`docs/WRITING_AND_COMMUNICATION_RULES.md`](docs/WRITING_AND_COMMUNICATION_RULES.md) | How all text is written |

If a spec and the plan disagree, fix one of them in the same commit and say which in the spec's changelog.

## Binding rules

- **Spec, tests, code, checkpoint, status.** Tests are written before code and fail first. The spec's status line is the progress record.
- **⚠ items are the owner's decisions.** Stop and ask; never choose a default in code. When you ask, explain in plain words what each option means and what it costs, with an example, then recommend one.
- **Current state only.** Event logs keep open items, the newest deed per lot, the newest certificate per building, and everything since the start date in `config.py` (D2). The previous pull exists for `detect` and nothing else.
- **Source column names stop at `load`.** After that, canonical names only.
- **The API, the dashboard and the agent read `data/export/nyc.duckdb`, never the warehouse.** Whatever users or the agent write goes to the app database (Postgres), never the warehouse.
- **Next.js never opens DuckDB or Postgres.** It calls FastAPI.
- **Store in EPSG:4326; measure in EPSG:2263 through `geo.py`.** Every distance is a walking distance on the OpenStreetMap network. Never straight-line.
- **Flag, don't delete.** A doubtful row gets a flag column and stays.
- **Metrics are versioned and computed once** (`name_unit@v1`), with a docstring that says what they do not measure.
- **Numbers come from SQL.** The agent never computes a number it reports.
- **No output says "buy".** A site is graded only against a stated buyer profile. No universal score.
- **Tests run offline.** No test reaches the network or calls Claude. Agent tests replay recorded responses. From S002, a test fixture blocks the network.
- **Every phase ends with a checkpoint on real data,** written up in `docs/checkpoints/`.

## This repo is public

- No key in code, commits, logs, fixtures or checkpoint notes. Keys live in `.env`, which is never committed.
- Never commit `data/`, `.env`, real buyer profiles (`profiles/*.yaml` other than `example.yaml`) or `watchlist.yaml`.
- Checkpoint notes record how reviews were marked, never the text of reviews made for real profiles.
- Business details for later phases live in the owner's private notes, outside the repo. Do not copy them in.

## Commands

```bash
uv sync                   # install Python 3.12 and every package in uv.lock
uv run pytest             # the tests, offline
uv run ruff check .       # lint
uv run ruff format .      # format (add --check to only check)
```

Later specs add their commands here when the commands exist: S002 the dataset stages, S031 the daily refresh.

## Git

- Work on a branch named for the spec: `s003-pluto`.
- Commit messages start with the spec id: `S003: land PLUTO 26v2`.
- `main` always passes `uv run pytest` and `uv run ruff check .`. Never force-push `main`.
- Commit locally as you go. Push once a spec is done: the owner walks through the change file by file, it merges into `main`, and `main` is pushed.
- Commit or push only when the owner asks.

## Writing

- Read [`docs/WRITING_AND_COMMUNICATION_RULES.md`](docs/WRITING_AND_COMMUNICATION_RULES.md) before you write or edit text.
- Follow it for all text: docs, specs, docstrings, commit messages and messages to the owner.
- Interface copy also follows the voice rules in [`BRAND.md`](BRAND.md).
