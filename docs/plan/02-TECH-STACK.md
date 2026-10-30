# 02 — Tech stack

Each choice below names what it is for and why it was picked.
Most choices match the old repo on purpose.
The old repo is then a working example of every tool you will use.

Where this project departs from the old one, the row says so.

## Language and tooling

| Tool | Version | For | Why |
|---|---|---|---|
| Python | 3.12 | All data and server code | The old repo's version. Every library below supports it. |
| `uv` | latest | Python install, virtual environment, dependencies, running commands | One tool instead of four. `uv.lock` makes installs repeatable. |
| `ruff` | latest | Linting and formatting | One fast tool instead of black, isort and flake8. |
| `pytest` | 8+ | Tests | Standard. Fixtures and parametrize cover everything here. |
| `python-dotenv` | 1.2+ | Reads the keys in `.env` into the environment | The most common way for Python code to read keys from a file. Only `config.py` uses it. |
| `lefthook` | from S041 | Runs the checks before each commit | It arrives through npm with the dashboard, so one tool runs the Python and the TypeScript checks. |
| Node.js + `pnpm` | Node 22, pnpm 10 | The dashboard's front end | Matches the old `web/`. |
| Git + GitHub | — | Version control | One spec per commit where possible. |

## Data

| Tool | For | Why |
|---|---|---|
| **DuckDB** (+ `spatial` extension) | The warehouse, the export, every heavy query | One file, no server. Reads Parquet and CSV directly. Fast on tens of millions of rows. |
| **Parquet** via `pyarrow` | Landing and clean files on disk | Typed, compressed, columnar. DuckDB reads it without loading it. |
| **GeoPandas + Shapely** | Reading shapefiles and geodatabases, reprojection | Standard for geometry in Python. Used at the edges, not for big joins. |
| `pyogrio` | Fast shapefile and geodatabase reading | GeoPandas's fast reader. |
| `pyproj` | Coordinate reference systems | Under GeoPandas; used directly by the measuring helper. |
| `osmnx` + `networkx` | The walking network and walking distances (D11) | `osmnx` builds the five boroughs' walking graph from OpenStreetMap; one multi-source shortest-path run per destination kind reaches every lot. |
| `httpx` | Downloads and API calls | Sync and async in one client, timeouts and retries built in. |
| `pydantic` | Typed records: configs, API responses, review output | One definition gives validation, JSON and a schema the agent can use. |
| `pandas` | Small tables at the edges | Only where a library expects it. DuckDB SQL does the heavy work. |

**Rule of thumb:** SQL in DuckDB for anything over a few thousand rows. Pandas for display and small glue.

## Server

| Tool | For | Why |
|---|---|---|
| **FastAPI** | The API: read-only over the export; writes only to the app database | Typed routes from Pydantic models, automatic OpenAPI docs at `/docs`. |
| **Postgres** + `psycopg` | The app database: accounts, profiles, the review queue, reviews, digests, usage (D19) | The standard store for a multi-user app. Only the Python side connects; Next.js never does. Schema changes are numbered SQL migrations. |
| `uvicorn` | Runs FastAPI | Standard. |
| `typer` | The command line (`python -m meridian_dashboard_nyc ...`) | Typed commands with help text for free. **Departure:** the old repo used `argparse`. |

## Map and dashboard

| Tool | For | Why |
|---|---|---|
| **Next.js** (App Router) + **React** + **TypeScript** | The dashboard app under `web/` | Routing and layouts for the pages. Map and chart pages are client components. Server code calls the FastAPI app only and never opens DuckDB. **Departure:** the old repo used Vite with vanilla TypeScript. |
| **deck.gl** | Every data layer on the map | Draws hundreds of thousands of features on the GPU: lots from PMTiles, large point sets from the API as Arrow. Check its current PMTiles loader at build time. |
| **MapLibre GL JS** | The basemap under deck.gl | Open source, vector tiles, no vendor key. |
| **PMTiles** + **tippecanoe** | Map layers as single files | One file per layer, served statically. tippecanoe builds them from GeoJSON. On Windows, run it in WSL or Docker. |
| **Protomaps** | The basemap | A self-hosted basemap in one PMTiles file. |
| **TanStack Query** | API data in the browser | Caches and refreshes responses; one hook per endpoint. |
| **Zustand** | UI state | Map view, selected lot, layer toggles. Filters live in the URL instead, so a view can be shared as a link. |
| **Plotly** (`plotly` in Python, `plotly.js` in the browser) | Every chart | A figure is JSON, so Python analyses and the agent can produce one and a test can validate it. Loaded only on chart pages, in the browser. **Departure:** the old repo used Vega-Lite. |
| **Playwright** | Browser tests | Proves pages draw and buttons work. |

The visual style is the Meridian XYZ brand (decision D10), from `brand-guidelines.md` in the `meridianxyz_website` repo.
Its § 11.1 token sheet becomes `web/src/tokens.css`; its § 4.5 ramps color the map layers and the charts.
Geist and Geist Mono are self-hosted, as the guidelines require.
Colors, spacing and type sizes live as CSS variables in that one file ([`04-CODING-STANDARDS.md`](04-CODING-STANDARDS.md)).

Decision D5 settled this stack.

### Crawlers and hosting cost

The map and lot pages are public from Phase 9 (D6), so crawlers will find them.
Filter state in the URL could give them millions of distinct pages to render.
Four rules keep a crawler's visit cheap.

1. **No server render per URL.** Filters are read from the URL only in client components, so every filtered view is the same static page from the CDN. A lot page is one static shell that loads its card in the browser; the Phase 6 spec picks a URL shape that keeps it static.
2. **Nothing to follow.** Filter controls update the URL through the router. They are never `<a href>` links.
3. **Crawlers told no.** `app/robots.ts` disallows any URL with a query string, and the lot pages. Filtered views and lot pages carry `noindex` and a canonical link to the bare page. The docs page is the exception: static, indexed, and linked from every locked feature.
4. **A ceiling on the bill.** On Vercel, turn on bot protection and set a spend limit. The VM and R2 bill flat or near it, so crawlers can slow them but not raise the bill.

## The agent

| Tool | For | Why |
|---|---|---|
| **Anthropic Python SDK** (`anthropic` 1.x) | Calling Claude | The official SDK. Version 1.x is built on `httpx2`, not `httpx`; import its types from the SDK, not from `httpx`. |
| **Claude Opus 5.5** (`claude-opus-5-5`) | Reviews | Every step, until the evals show a cheaper model or a lower effort holds quality (decision D9). |
| Message Batches API | The nightly digest's write-ups | Half price for work that can wait. |
| Prompt caching | The fixed part of every request | The system prompt, tool list and table descriptions repeat on every call. Caching them cuts cost and time. |

Details, including which Claude features to use and avoid, are in [`06-SITE-REVIEW-AGENT.md`](06-SITE-REVIEW-AGENT.md).

## Email

None in v1 (decision D4).
Reviews and the daily digest go to the dashboard's Inbox page.
Email comes later, as a subscription that sends the same digest to a personal address.
These options fit when it does.

| Option | Sends | Receives | Note |
|---|---|---|---|
| Postmark | Yes | Yes, by webhook | Simple inbound parsing. Good deliverability. |
| Resend | Yes | Yes, by webhook | Modern API, Python SDK. |
| SendGrid | Yes | Yes (Inbound Parse webhook) | Widely used. Heavier setup. |
| Gmail or Microsoft 365 API | Yes | Yes, by polling or push | Uses the mailbox you already have. OAuth setup is the cost. |

Sending works from a laptop.
Receiving needs a public HTTPS address for the provider's webhook, which the VM provides from Phase 9 (D6).

## Running it

Decision D6.

| Need | Phases 0–8 | From Phase 9 |
|---|---|---|
| Where it runs | Your laptop | The pipeline and FastAPI on one small cloud VM. The Next.js site on Vercel. Map tiles on Cloudflare R2, which charges no egress fees. |
| Schedule | Windows Task Scheduler, or cron in WSL, calling one `make daily` command | The same command on the VM's cron |
| Who can see it | You, on localhost | Guests browse the map, a basic lot card and neighborhood stats. Phase 9 opens sign-in for you; Accounts for others come in Phase 9.5 (D18). A user's profiles, inbox and reviews are visible only to that user and to you. |
| Secrets | `.env` at the repo root, gitignored, read by `config.py` with `python-dotenv` | The host's secret store |
| Logs | `data/runs/*.jsonl` plus the API's stdout | Same, shipped to a log service if needed |

## Keys the project needs

| Variable | For | Phase |
|---|---|---|
| `SOCRATA_APP_TOKEN` | NYC and NYS Open Data, without throttling | 1 |
| `ANTHROPIC_API_KEY` | The agent | 8 |
| `AUTH_SECRET`; Google and GitHub client ids and secrets | Sign-in (D16) | 9 |
| `DATABASE_URL` | The app database (D19) | 7 |
| `TILES_BUCKET_KEY_ID`, `TILES_BUCKET_SECRET` | Uploading map tiles to R2 | 9 |
| `CENSUS_API_KEY` | Optional census data | 10 |

`.env.example` names every variable with an empty value.
`.env` holds the real values and is never committed.

## `pyproject.toml`

The real file is [`pyproject.toml`](../../pyproject.toml) at the repo root.
S001 made it with `uv init --bare --package` and `uv add`.
Each spec adds a library with `uv add` when its code first needs it, so the file lists only what the code uses.
The tables above name the libraries the plan expects.

`uv.lock` pins every version.
Upgrade on purpose, one library at a time, and run the tests after each upgrade.
