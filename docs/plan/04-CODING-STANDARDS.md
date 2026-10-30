# 04 — Coding standards

These rules apply to every file in the repo.
`ruff` and the tests enforce what they can.
Review enforces the rest.

## Principles

1. **Small, typed, documented functions.** A function does one thing. Its name says what. Its docstring says why.
2. **SQL for the heavy lifting.** DuckDB joins, filters and aggregates. Python orchestrates.
3. **Fail loudly, with a name.** An error says which dataset, which stage, which row. A silent skip is a bug.
4. **Flag, don't delete.** A doubtful row gets a flag column and stays. Deletion hides the problem.
5. **One place for each fact.** Paths live in `config.py`. Measuring lives in `geo.py`. A source's column names live in its dataset package.
6. **Explainable before shipped.** Do not merge code you cannot explain line by line. This applies twice to code copied from the old repo.

## Python

### Format and lint

- `ruff format` formats. `ruff check` lints. Run both with `uv run ruff format --check .` and `uv run ruff check .`.
- Line length 100.
- Imports sorted by ruff. No wildcard imports.

### Types

- Every function signature is fully typed, including the return.
- Use `pathlib.Path` for paths, never strings.
- Use Pydantic models for anything that crosses a boundary: config files, API responses, agent tool inputs and outputs, review results.
- Use `dataclass(frozen=True)` for small internal records.

### Docstrings

Every public module, class and function has one.
The first line is one sentence in the imperative: "Return the open violations on a lot."
Add a paragraph only when the reason is not obvious.

Metrics get one more rule.
The docstring says what the number measures and what it does **not** measure.

```python
def unused_floor_area_sqft(lots: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    """Return each lot's unused floor area in square feet: unused_floor_area_sqft@v1.

    It is the largest allowed FAR across uses, minus the built FAR, times the lot area.
    It does not account for bonuses, transfers of development rights, landmark limits,
    height limits or lot-coverage rules. A lot can show unused floor area it cannot use.
    """
```

### Naming

| Thing | Convention | Example |
|---|---|---|
| Module, function, variable | `snake_case` | `land_pull`, `open_violations` |
| Class | `PascalCase` | `Dataset`, `LotCard` |
| Constant | `UPPER_SNAKE` | `PORTAL_ID = "64uk-42ks"` |
| Dataset id | `snake_case`, from `sources.md` | `hpd_violations` |
| Canonical table | plural noun | `lots`, `filings` |
| Metric | `name_unit@vN` | `unused_floor_area_sqft@v1` |
| Units | suffix in the column name | `lot_area_sqft`, `distance_m`, `price_usd` |
| Dates | `_date` for a day, `_utc` for a timestamp | `sale_date`, `pulled_utc` |
| Booleans | `is_` or `has_` | `is_market_sale`, `has_open_vacate` |

### Errors

- Raise a specific exception with a message that names the thing: `ValueError(f"pluto: version {v} != mappluto version {m}")`.
- Never `except Exception: pass`. Catch only what you can handle.
- A stage that fails writes the error to the manifest, then re-raises.

### Logging and output

- Long steps go through `runlog.step("name")`, which prints elapsed time and writes a line to `data/runs/`.
- `print` only in command-line entry points.
- Never log a key, a token, an email body or a full API response.

### Config and secrets

- `config.py` is the only module that reads environment variables or builds paths under `data/`.
- Keys live in `.env`. Code reads them through `config.py`. Tests never need one.

### Network

- Only `sources/` opens network connections.
- Tests run with the network blocked. From S002, a test fixture fails any test that tries.
- Every request has a timeout. Every retry has a backoff.

## SQL

- DuckDB dialect. Lowercase keywords, one clause per line.
- Name every CTE for what it holds: `open_hpd`, not `t1`.
- A query longer than about 20 lines lives in its own `.sql` file next to the Python that runs it.
- **Never format user input into SQL.** Bind parameters with `?`.
- Select columns by name in anything that writes a table. `select *` is for exploration only.

```sql
with open_hpd as (
    select bbl, count(*) as n_open, count(*) filter (where class = 'C') as n_open_class_c
    from violations
    where agency = 'HPD'
    group by bbl
)
select l.bbl, coalesce(o.n_open, 0) as hpd_open, coalesce(o.n_open_class_c, 0) as hpd_open_class_c
from lots as l
left join open_hpd as o using (bbl)
```

## Data rules

- **Keys are checked at `clean`.** A duplicate key fails the stage and names the first duplicate.
- **Null is not zero.** A missing height is `NULL`, never `0`.
- **Geometry is stored in EPSG:4326 and measured in EPSG:2263.** Only `geo.py` converts. A test scans the code for area, length and distance calls outside it.
- **Distances are walking distances.** Every distance is measured along the OpenStreetMap walking network (D11); there are no straight-line approximations. The graph's edge lengths are computed in EPSG:2263 through `geo.py`. Every page that shows a walking distance credits "© OpenStreetMap contributors".
- **Every displayed number has a source.** Dataset id and pull date travel with it to the page and the inbox.

## Tests

- One test file per module: `tests/test_<module>.py`.
- Every acceptance criterion in a spec maps to at least one test, named after it: `test_s003_c2_duplicate_bbl_fails`.
- Fixtures are real rows: at most 20 per dataset, cut from a real landing file.
- Golden files for rendered output (a lot card, a digest). A change to a golden file is reviewed like code.
- The default suite runs offline in under 30 seconds. Tests that need real data carry `@pytest.mark.real` and run only on request.
- No test calls Claude. Agent tests replay recorded responses (see [`06-SITE-REVIEW-AGENT.md`](06-SITE-REVIEW-AGENT.md)).

## TypeScript (the dashboard)

- `strict: true` in `tsconfig.json`. No `any`.
- One route per page under `web/src/app/`. Shared pieces under `web/src/components/`.
- All API calls go through one client in `web/src/api/`, with one TanStack Query hook per endpoint. Its types are generated from the API's OpenAPI schema, so the front end and the server cannot drift.
- Nothing in `web/` opens DuckDB. Server components call FastAPI through the same client.
- Maps (deck.gl) and charts (Plotly) are client components, loaded in the browser only.
- The crawler rules in [`02-TECH-STACK.md`](02-TECH-STACK.md) hold on every page: filters are read only in client components, and filter controls are never links.
- Colors, spacing, type sizes and radii are CSS variables in `web/src/tokens.css`, from the Meridian XYZ token sheet (D10). Components never hard-code a color.
- deck.gl layers and Plotly figures read the same tokens through one helper, `web/src/tokens.ts`, never a literal.
- Plotly figures from Python carry data and layout, not colors. The dashboard applies the brand template when it draws them, so light and dark both work.
- Support light and dark themes through the same variables.
- Every interactive element is reachable by keyboard and has a label.
- Playwright tests cover each page: it loads, it draws, its main action works.

## Git

- `main` always passes `uv run pytest` and `uv run ruff check .`.
- Work on a branch named for its spec: `s003-pluto`.
- One spec per commit where possible. The message starts with the spec id: `S003: land PLUTO 26v2 and MapPLUTO`.
- Never commit `data/`, `.env`, notebooks with outputs, or a file over 5 MB.
- Never force-push `main`.

## Writing

All text follows [`../WRITING_AND_COMMUNICATION_RULES.md`](../WRITING_AND_COMMUNICATION_RULES.md).
That includes specs, READMEs, docstrings, commit messages, these plan files, and the digests and reviews that the agent writes.
