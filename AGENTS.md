# AGENTS.md

How any coding agent works in this repo: Claude Code (through `CLAUDE.md`), or any other tool that reads `AGENTS.md`.

## What this is

v0, a simple prototype that evaluates NYC lots and buildings as they stand today, for real estate investment companies.
It checks each site against the policies of three developer types, and gives one verdict for each type: Buy, Review or Pass.
It is also an agent harness: it compares how well different agents, with the same tools, give those verdicts.
It runs by hand, in notebooks. [`docs/V0.md`](docs/V0.md) is the design.

The work planned after v0 is in [`ROADMAP.md`](ROADMAP.md).
Do not build it unless the owner asks.

Explain each change before you make it.
The owner reviews every change before it merges.

## Before you change anything

1. Read [`docs/V0.md`](docs/V0.md).
2. If the work is not in `docs/V0.md`, stop and ask the owner.
3. Keep each source in its own folder in `data/raw/`.
4. Explore first (D17). New work starts in a notebook. Move code into a module in `src/`, with tests, only after the notebook shows that it works.

## Keep it simple

- Write plain code: short modules, module-level constants, plain functions, the most common library for each job.
- Add a library, a tool or a safeguard in the notebook or module that first needs it, never earlier.
- Comment only where the reason is not obvious from the code.
- Handle an exception only when the code can do something about it.
- Never change a file in `data/raw/`. Combine sources in a notebook, and write combined tables to `data/processed/`.

## Data and code conventions

- Put the unit in a column name: `lot_area_sqft`, `walk_min`, `distance_ft`, `price_usd`.
- Start a boolean name with `is_` or `has_`: `is_market_sale`, `has_open_vacate_order`.
- End a date name with `_date` for a day and `_utc` for a time: `sale_date`, `pulled_utc`.
- Null is not zero. A missing value stays empty, never `0`.
- An error names the dataset and the step, for example `rolling_sales: sale_price is not a number`.
- Every number carries its source dataset and pull date.
- The docstring of a risk factor or a measure says what it measures and what it does not measure.

## Where the truth lives

| File | Holds |
|---|---|
| [`docs/V0.md`](docs/V0.md) | The v0 design: verdicts, developer types, risk factors, sources, notebooks |
| [`docs/GLOSSARY.md`](docs/GLOSSARY.md) | Every term and measure, with one meaning each, and what each measure does not measure |
| [`sources.py`](src/meridian_dashboard_nyc/sources.py) | The data sources that `pull` downloads, with the portal id and filter for each |
| [`profiles/`](profiles/) | The three example policies and the risk factors, which the code reads |
| [`docs/decisions.md`](docs/decisions.md) | One line per owner decision, dated |
| [`docs/WRITING_AND_COMMUNICATION_RULES.md`](docs/WRITING_AND_COMMUNICATION_RULES.md) | How all text is written |
| [`ROADMAP.md`](ROADMAP.md) | The work planned after v0 |

## Binding rules

- **⚠ items are the owner's decisions.** Stop and ask. Never choose a default in code. When you ask, explain in plain words what each option means and what it costs, with an example, then recommend one.
- **Current state only.** v0 evaluates lots as they stand today. Event logs keep open items and everything since the start date in `config.py` (D4).
- **Sites are whole lots and buildings** (D2). Never offer a condo unit or a co-op apartment as a site. Flag condo and co-op lots, and leave them out of every search.
- **US units** (D5). Feet, square feet, miles, minutes and US dollars. Walking time uses 3 miles an hour.
- **Store in EPSG:4326, measure in EPSG:2263,** which is in US feet. Every distance is a walking distance on the OpenStreetMap network. Never straight-line.
- **Flag, do not delete.** A doubtful row gets a flag column and stays.
- **Numbers come from code.** Code computes every fact that an agent receives. The comparison checks each number in a decision letter against those facts.
- **Agents give their own verdicts** (D11). Do not add a rule that limits or overrides an agent's verdict. Record it beside the code verdict.
- **Every agent gets the same tools and the same data** (D12). Tools are read-only.
- **Every verdict names its developer type** (D10). A verdict is Buy, Review or Pass under one policy, never for every buyer. Each output that shows verdicts states that they use public data and example policies, and are not investment advice.
- **Tests run offline.** No test reaches the network or calls Claude.

## This repo is public

- No key in code, commits, logs, fixtures or notebook outputs. Keys live in `.env`, which is never committed.
- Never commit `data/`, `.env`, real customer policies (`profiles/*.yaml` other than `example_*.yaml` and `risk_factors.yaml`) or `watchlist.yaml`.
- Never commit the text of a decision letter made for a real customer policy.
- Business details for later phases live in the owner's private notes, outside the repo. Do not copy them in.

## Commands

```bash
uv sync                   # install Python 3.12 and every package in uv.lock
uv run pytest             # the tests, offline
uv run ruff check .       # lint
uv run ruff format .      # format (add --check to only check)
uv run python -m meridian_dashboard_nyc.pull           # download every source into data/raw/
uv run python -m meridian_dashboard_nyc.pull pluto     # download one source
```

## Git

- Work on a branch named for the work, for example `v0-policies`.
- Commit messages start with `v0:`, for example `v0: add the three developer policies`.
- `main` always passes `uv run pytest` and `uv run ruff check .`. Never force-push `main`.
- Commit locally as you go. The owner walks through each change file by file. Then it merges into `main`, and `main` is pushed.
- Commit or push only when the owner asks.

## Writing

- Read [`docs/WRITING_AND_COMMUNICATION_RULES.md`](docs/WRITING_AND_COMMUNICATION_RULES.md) before you write or edit text.
- Follow it for all text: docs, docstrings, notebooks, commit messages, decision letters and messages to the owner.
- Use each term with its meaning in [`docs/GLOSSARY.md`](docs/GLOSSARY.md). Add a new term there before you use it.
