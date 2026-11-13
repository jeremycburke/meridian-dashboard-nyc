# Decisions

The owner's decisions that are in force, one line each: date · number · decision · reason.
When a decision changes, its line is rewritten with the new date. Git keeps the earlier versions.

## Scope

- 2026-11-13 · D1 · Build v0 first: a simple prototype that evaluates lots and buildings as they stand today against company policies, the way a claims department checks a claim against policy. It uses about 10 sources and runs by hand in notebooks, with no model training and no history · A small tool to try out first. The historical record comes next.
- 2026-11-13 · D2 · v0 serves real estate investment companies that build new or buy whole properties. A site is a whole lot with its buildings. Sales are pulled for whole lots and buildings only. Condo and co-op lots stay in PLUTO, flagged and left out of every search · Individual buyers of condos and apartments are not the audience, and their sales do not compare with whole-property deals.
- 2026-11-13 · D3 · `ROADMAP.md` lists the work after v0. The detailed plans for that work stay out of the public repo · The repo shows working software first, not plans.

## Data

- 2026-10-28 · D4 · Event logs keep their open items and everything since one start date, 2025-01-01, set once in `config.py` · It keeps the data small. Moving the date back adds history.
- 2026-11-13 · D5 · US units throughout: feet, square feet, miles, minutes and US dollars. Every distance is a walking distance on the OpenStreetMap street network, never a straight line. Walking time uses 3 miles an hour, the speed widely reported for Google Maps · The audience works in US units. A straight line misstates access across rail yards, highways and water.
- 2026-10-28 · D6 · "Nearby" means a neighborhood, not a distance: the lot's own 2020 NTA, for comparable sales and for the neighborhood profile · Buyers think in neighborhoods, not in circles on a map.
- 2026-10-28 · D7 · Census data comes from the newest ACS 5-year release, by tract · ACS 1-year estimates are not published for tracts.
- 2026-11-13 · D8 · A market sale is a sale of $100,000 or more. Code flags every sale below that and keeps it · The rolling-sales price is the full price paid, and few whole lots or buildings in New York sell for less.
- 2026-11-13 · D9 · v0 uses four urban-form levels: 1 (lot and building basics), 2 (roof height only), 3 (density and use mix, by neighborhood) and 5 (walking access). Walking access counts the destinations within a 15-minute walk: grocery stores, schools, parks, pharmacies, shops and retail, cultural destinations and other points of interest. The use mix uses PLUTO's 11 land-use categories · These levels need only the v0 sources. A 15-minute walk is a common measure of local access.

## Policies and verdicts

- 2026-11-13 · D10 · Each site gets one verdict for each of three developer types: Buy, Review or Pass. The types are safe and institutional, standard, and opportunistic. Each type is a customer policy with its own rules and risk limits. Each site has one risk score, which all three types read. Each verdict names its developer type, and every output that shows verdicts states that they are not investment advice · Verdicts must lead to an action, and one site under three policies shows how the same lot suits different buyers.

## Agents

- 2026-11-13 · D11 · No rule limits an agent's verdict. Each agent gives its own verdict and decision letter, beside the code verdict, and v0 compares the agents on the same sites · v0 tests how well each agent judges a site, so a fixed limit would hide the differences between agents.
- 2026-11-13 · D12 · Agents use tools. v0 is an agent harness: a tool loop, with the same read-only tools and the same data for every agent · Tool use is the skill under test.
- 2026-10-28 · D13 · Start with `claude-opus-5-5`. Move a step to another model or a lower effort only when the comparison shows that it holds quality · Start from the best quality, and let measured results bring the cost down.

## Code and repo

- 2026-11-13 · D14 · The repo is `meridian-dashboard-nyc` and the package is `meridian_dashboard_nyc` · The dashboard comes soon after v0.
- 2026-10-29 · D15 · The code lives in `src/meridian_dashboard_nyc/`, with `uv_build` as the build backend · The standard layout for an installable package.
- 2026-10-29 · D16 · Keep the code simple: plain modules, module-level constants, and each library or tool added when the code first needs it. No Makefile, pre-commit hook or CI yet · A small project that works comes first.
- 2026-11-13 · D17 · Explore first, then build. New work starts in a notebook, as exploratory data analysis. Code moves into a module in `src/`, with tests, once the notebook shows that it works · The owner learns the data before the code takes its final shape.
- 2026-10-29 · D18 · All text follows [`WRITING_AND_COMMUNICATION_RULES.md`](WRITING_AND_COMMUNICATION_RULES.md) · One standard for docs, docstrings, commit messages and agent output.
- 2026-11-13 · D20 · The public history starts fresh with four v0 commits. After that, each piece of work gets its own branch, with commits as it grows, and merges into `main` after the owner reviews it. `main` is never force-pushed again · The public history shows how the project is built, not the cleanup before it.

## Dashboard

- 2026-10-28 · D19 · The dashboard uses Next.js and React, deck.gl over a MapLibre basemap, TanStack Query and Zustand, with filters in the URL and Plotly for charts. A read-only FastAPI service serves the data, and the dashboard never opens a database itself · deck.gl handles the volume of map data, and Plotly figures pass straight from Python to the browser.
