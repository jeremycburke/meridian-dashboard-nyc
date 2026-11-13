# meridian-dashboard-nyc

meridian-dashboard-nyc evaluates New York City lots and buildings against the policies of real estate developers.
It is for investment companies that build new or buy whole properties, not for people who buy one condo or apartment.
A lot is a unit of real estate that the city taxes. Each lot has a borough, block and lot number (BBL).

This is v0, a simple prototype. It is in progress.

## What v0 does

v0 works like a claims department.
In a claims department, a claim comes in and an adjuster checks it against company policy.
Here, a site comes in, and the tool checks it against the policy of each of three developer types:

- **Safe and institutional:** large sites, prime locations, low risk.
- **Standard:** mid-size sites in four boroughs, medium risk.
- **Opportunistic:** smaller or distressed sites anywhere in the city, high risk.

For each site and each developer type, v0 gives one verdict: **Buy, Review or Pass**.
Code checks the policy's rules and the site's risk score, and gives a code verdict.
Then several AI agents give their own verdicts. Each agent looks up the site with the same read-only tools, and writes a short decision letter that cites the policy clauses and the evidence.
v0 compares how well each agent judges a site.
The same lot can get a Pass from one developer type and a Buy from another.

The verdicts use public data and example policies. They are not investment advice.

v0 evaluates each lot as it stands today. It uses ten public sources: five about the lot, its price and its condition, and five about its context, such as the walk to the subway and the shops, parks and cultural places within a 15-minute walk.
Every distance is a walking distance on the OpenStreetMap street network, never a straight line. All measures use US units.

[`docs/V0.md`](docs/V0.md) gives the full design.

## Built with

| Layer | Tools |
|---|---|
| Data | Python 3.12, `uv`, `httpx`, pandas |
| Analysis | Jupyter notebooks |
| Maps and walking | GeoPandas and `osmnx`, added with notebook `03` |
| Agent harness | The Anthropic Python SDK and Pydantic, starting with Claude Opus 5.5, added with notebook `05` |

## Repo layout

```
.
├── README.md               start here
├── ROADMAP.md              the work planned after v0
├── AGENTS.md  CLAUDE.md    the rules for coding agents
├── pyproject.toml          the packages, and the settings for pytest and ruff
├── uv.lock                 the exact version of every package
├── .env.example            the keys, with empty values (copy it to .env)
├── data/                   downloads, not in git (the pull command makes this folder)
│   └── raw/                one folder for each source, with the files exactly as downloaded
├── notebooks/              the analysis, numbered in the order to run it
├── profiles/               the example developer policies
├── src/meridian_dashboard_nyc/
│   ├── config.py           where the data lives, the start date, the keys from .env
│   ├── sources.py          the list of sources, with the portal id and filter for each
│   └── pull.py             downloads each source into data/raw/
├── tests/                  the pytest tests
└── docs/                   the v0 design, the decisions and the writing rules
```

Each source has its own folder in `data/raw/`.
A `_source.json` file next to each download records the source URL, the download time, the row count and the file hash.
The files in `data/raw/` do not change after the download.
Tables that combine sources go in `data/processed/`.

## Get started

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs Python 3.12 and every package for you.
2. Clone the repo and install the packages:

   ```bash
   git clone https://github.com/jeremycburke/meridian-dashboard-nyc.git
   cd meridian-dashboard-nyc
   uv sync
   ```

3. Copy `.env.example` to `.env`, then fill in the keys that you need. The tests and the download need no keys. With a Socrata app token in `SOCRATA_APP_TOKEN`, the open-data portals do not slow down the download.

   ```bash
   cp .env.example .env
   ```

4. Run the tests, the linter and the formatter:

   ```bash
   uv run pytest
   uv run ruff check .
   uv run ruff format .
   ```

5. Download every source into `data/raw/`:

   ```bash
   uv run python -m meridian_dashboard_nyc.pull
   ```

6. Open the notebooks in `notebooks/` in number order.

## Documentation

| File | What it describes |
|---|---|
| [`docs/V0.md`](docs/V0.md) | The v0 design. Start here. |
| [`docs/GLOSSARY.md`](docs/GLOSSARY.md) | Every term and measure, with one meaning each |
| [`docs/decisions.md`](docs/decisions.md) | Each decision in force, with its date and reason |
| [`ROADMAP.md`](ROADMAP.md) | The work planned after v0: the dashboard, history, more data and a daily refresh |
| [`AGENTS.md`](AGENTS.md) | The rules for coding agents |

## Data and credits

- Data from [NYC Open Data](https://opendata.cityofnewyork.us/), [NYS Open Data](https://data.ny.gov/) and the NYC Department of City Planning ([BYTES of the BIG APPLE](https://www.nyc.gov/site/planning/data-maps/open-data.page)). The tool describes these records as published and makes no claim beyond them.
- Walking network © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors, available under the Open Database License.

## License

This repo has no license yet. You can read the code, but you need permission to reuse it.
