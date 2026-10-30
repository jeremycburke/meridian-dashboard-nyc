# meridian-dashboard-nyc — the plan

*Start at the repo root: [`README.md`](../../README.md), [`AGENTS.md`](../../AGENTS.md), and [`SPEC.md`](../../SPEC.md), the build plan with every spec's tests and checks.*

*Written 2026-10-22. These files are the plan for rebuilding the urban-metrics project as a new repo. Rewrite them in place as decisions are made; record each decision in `docs/decisions.md`.*

## What this project is

A rebuild of `meridian-urban-metrics-and-capital` for New York City, holding the city as it stands today.

It does three things.

1. **Lands every current NYC dataset that describes a lot** into one DuckDB database: the newest PLUTO, zoning, sales, assessments, permits, violations, notices, and the neighborhood around each lot.
2. **Shows it** on a map and a dashboard, one lot card per lot.
3. **Reviews new sites.** After each daily refresh, an agent finds lots that just became interesting, grades each against a buyer's stated criteria, and reports to an inbox on the dashboard.

## The old repo

The old repo is the reference: every phase names the old files to read first.
Nothing here imports from it.
Copy code from it only when you can explain the code line by line.

## What is in, what is out

| In | Out |
|---|---|
| The newest PLUTO release and its lot shapes | Earlier PLUTO releases, lot lineage, history views |
| Current registers; event logs as open items plus everything since 2025-01-01 | Event history before 2025 (added later by moving the start date back) |
| 71 datasets from NYC and NYS Open Data and DCP, plus the OpenStreetMap walking network | Federal economic series, Overture Maps, SEC filings |
| One read-only API, a map, a dashboard | The causal studies, project outcomes, verify/search/design engines |
| The site-review agent and its daily digest, on a dashboard Inbox page | Entity resolution of owners into sponsors; email, sent or received (later, as a subscription) |
| Guest browsing now; accounts and payments in a later phase (Phase 9.5) | |
| NYC only | Other cities (possible later, each with its own dataset packages and its own database) |

## Read in this order

| # | File | What it settles |
|---|---|---|
| 1 | `00-INDEX.md` | This map and the open decisions |
| 2 | [`01-data-sources/README.md`](01-data-sources/README.md) | What "current" means; the kinds of dataset; what is left out |
| 3 | [`01-data-sources/sources.md`](01-data-sources/sources.md) | All 71 datasets: ids, grain, rows, filter, key, phase |
| 4 | [`01-data-sources/raw.md`](01-data-sources/raw.md) | Where pulls land; the stages; the rules; sizes |
| 5 | [`01-data-sources/api.md`](01-data-sources/api.md) | How to fetch from each source; the API this project serves |
| 6 | [`02-TECH-STACK.md`](02-TECH-STACK.md) | Every tool and why |
| 7 | [`03-ARCHITECTURE.md`](03-ARCHITECTURE.md) | The chain, the folders, the tables, the lot card |
| 8 | [`04-CODING-STANDARDS.md`](04-CODING-STANDARDS.md) | Python, SQL, data, tests, TypeScript, git, writing |
| 9 | [`05-PROCESSES.md`](05-PROCESSES.md) | Specs, checkpoints, decisions, adding a dataset, the daily refresh, working with Claude |
| 10 | [`06-SITE-REVIEW-AGENT.md`](06-SITE-REVIEW-AGENT.md) | Triggers, buyer profiles, the review pipeline, Claude settings, the inbox, evals |
| 11 | [`07-BUILD-PHASES.md`](07-BUILD-PHASES.md) | Phases 0–10 (and 5.5, 9.5), each with its checkpoint |
| 12 | [`08-URBAN-FORM.md`](08-URBAN-FORM.md) | Urban-form metrics from simple to complex, and how a level is added |

## How to use these files while building

1. Pick the next phase in `07-BUILD-PHASES.md`.
2. Settle the open decisions it names.
3. Write its spec from `specs/000-TEMPLATE.md`, citing the plan sections it implements.
4. Build it: the tests first, then the code.
5. Run the checkpoint on real data. Look at the output. Then move on.

## Deliveries

Decision D21.

1. **First delivery: the portfolio platform.** Phases 0–9, with 5.5 and the full agent: the data back end, the dashboard, the urban-form analytics and the reporting on site changes, live with guest browsing and you as the only account. It shows the work as a portfolio piece and is ready for consulting use.
2. **When consulting calls for it:** Phase 9.5, accounts and payments, planned in the owner's private notes. D20 waits until then.
3. **Over time:** Phase 10 features and urban-form levels 6–9, one at a time.

## Open decisions

Each is the owner's call.
The proposed default holds only once you accept it in `docs/decisions.md`.
Claude stops and asks at any of these; it never picks one in code.

| Id | Decision | Proposed default | Needed by |
|---|---|---|---|
| D1 | Repo and package names | **Decided 2026-10-28:** repo `meridian-dashboard-nyc`, package `meridian_dashboard_nyc` | Phase 0 |
| D2 | Look-back window for each event log | **Decided 2026-10-28:** open items, the newest deed per lot and the newest certificate per building, plus everything since one fixed start date, 2025-01-01. One setting; move it back to add history (per-dataset filters in `sources.md`) | Phase 3 |
| D3 | How many pulls of each dataset to keep | **Decided 2026-10-28:** the two newest; `prune` removes the rest as the last step of `make daily`, only after every step succeeded | Phase 7 |
| D4 | Email provider | **Decided 2026-10-28:** no email in v1. Reviews and the daily digest go to an Inbox page on the dashboard; email comes later as a subscription, and the provider is chosen then | Phase 9 |
| D5 | Dashboard approach | **Decided 2026-10-28:** Next.js + React + deck.gl over a MapLibre basemap; TanStack Query, Zustand and filters in the URL; Plotly for every chart. Crawler rules in `02-TECH-STACK.md` | Phase 6 |
| D6 | Where it runs and what schedules it | **Decided 2026-10-28:** your laptop and Task Scheduler through Phase 8. From Phase 9: pipeline and FastAPI on one small VM (cron), Next.js on Vercel, tiles on Cloudflare R2. Map and lot pages public; Inbox, Sites, Review and Profiles behind sign-in (access tiers refined by D18) | Phase 9 |
| D7 | The first buyer profiles and their screens | **Decided 2026-10-28:** you write one or two before Phase 8, once the lot card and metrics exist | Phase 8 |
| D8 | Which events count as a new site | **Decided 2026-10-28:** the twelve triggers in `06-SITE-REVIEW-AGENT.md` § 4: the ten proposed, plus `zoning_changed` and `watched_buyer_bought`. Every sale shows its buyer and seller as recorded; company buyers are flagged | Phase 7 |
| D9 | Which Claude model runs each step | **Decided 2026-10-28:** `claude-opus-5-5` throughout; after Phase 8c the eval also runs on Opus at `low` effort and on Sonnet 5.5, and a step switches only when it holds quality | Phase 8 |
| D10 | Visual style of the dashboard and email | **Decided 2026-10-28:** the Meridian XYZ brand guidelines (`meridianxyz_website/brand-guidelines.md`): the § 11.1 token sheet in `web/src/tokens.css`, the § 4.5 ramps for maps and charts | Phase 6 |
| D11 | Walking distance on the street network | **Decided 2026-10-28:** walking distance on an `osmnx` (OpenStreetMap) network from every lot to each destination kind (transit, schools, grocery stores, ...; the list is set in the network spec). No straight-line approximations. Built in Phase 5 | Phase 5 |
| D12 | Who may receive email from the agent | **Deferred with D4:** no email in v1; settled when email subscriptions are added | Later |
| D13 | A `territory` column on every table | **Decided 2026-10-28:** none. One database per city: a second city gets its own dataset packages, warehouse and export file; cross-city queries attach both | Phase 1 |
| D14 | Census estimates | **Decided 2026-10-28:** the newest ACS 5-year release, by tract | Phase 10 |
| D15 | Urban-form analysis: what it measures and which phase builds it | **Decided 2026-10-28:** the ladder in `08-URBAN-FORM.md`. Levels 1–5 (lot and building basics, geometry, density and mix, street network form, walking access) at lot and NTA grain in a new Phase 5.5; block grain, momepy, srai and an Urban Taxonomy-style typology later | Phase 5.5 |
| D16 | Sign-in provider | **Decided 2026-10-28:** Auth.js with Google and GitHub sign-in; guests browse without signing in. Next.js gives FastAPI a short-lived signed token; FastAPI checks it and the caller's tier | Phase 9 |
| D17 | What "nearby" means for comparable sales and nearby activity | **Decided 2026-10-28:** a neighborhood, not a distance. Default: the lot's own 2020 NTA; the dashboard adds chosen neighborhoods and a lasso. Comps show their metrics beside the subject lot's | Phase 6, 8 |
| D18 | Access tiers for accounts | **Decided 2026-10-28.** Guests browse the map, a basic lot card and neighborhood stats; accounts unlock deeper views and their own profiles and Inbox. The details are in the owner's private notes | Phase 9.5 |
| D19 | App database | **Decided 2026-10-28:** Postgres, in Docker on your laptop from Phase 7 and on the VM from Phase 9. Holds accounts, profiles, the review queue, reviews, digests, saved areas, usage and stored keys. Only the Python side connects | Phase 7 |
| D20 | Payments | **Deferred 2026-10-28** until Phase 9.5, after the first delivery. Details in the owner's private notes | Phase 9.5 |
| D21 | What the first delivery is | **Decided 2026-10-28:** Phases 0–9 with 5.5 and the full agent, live as a portfolio platform; Phase 9.5 when consulting calls for it; Phase 10 over time | — |
| D22 | How much tooling the scaffold has | **Decided 2026-10-29:** simple code; each library or tool arrives in the spec that first needs it. No Makefile, pre-commit hook or CI in S001 | Phase 0 |
| D23 | Where the Python code lives | **Decided 2026-10-29:** `src/meridian_dashboard_nyc/`, with `uv_build` | Phase 0 |
| D24 | How all text is written | **Decided 2026-10-29:** `docs/WRITING_AND_COMMUNICATION_RULES.md` | Phase 0 |
| D25 | When work is pushed | **Decided 2026-10-29:** commit locally while a spec is open; push `main` once the spec is done and reviewed | Phase 0 |

## Carried over from the old repo

These rules from the old `CLAUDE.md` still hold.

- Spec before code; tests before code; the spec's status line is the progress record.
- A table or column not in `SCHEMA.md` does not exist.
- Owner decisions are marked ⚠ and never resolved in code.
- Flag, don't delete.
- BBL is the join key; condo handling is written down before the first sale is joined.
- Store in EPSG:4326; measure in the local projection through one helper.
- Metrics are versioned and computed once.
- The map, the API and the agent read the export, never the warehouse.
- No output says "do the deal"; scores exist only inside a stated buyer profile.
- No key in code, commits, logs or fixtures.
- Every phase ends with real output reviewed by you.

## Changelog

- 2026-10-22: created. Dataset ids, row counts and download URLs checked against NYC Open Data, NYS Open Data, DCP Bytes and NYC GeoSearch on this date.
- 2026-10-28: D1 decided. Package renamed `meridian_dashboard` → `meridian_dashboard_nyc` in every plan file.
- 2026-10-28: D2 decided: one start date, 2025-01-01, for every event log. Keep filters rewritten in `sources.md`, `README.md`, `raw.md`, `api.md`. D14 (ACS 5-year by tract) added and decided.
- 2026-10-28: D3 decided: `make daily` ends with `prune`, keeping two pulls per dataset. `raw.md` rule 3, `README.md`, `05-PROCESSES.md` and Phase 7 updated.
- 2026-10-28: D4 decided: no email in v1; the digest goes to a dashboard Inbox page. D12 deferred with it. Email folder, inbound webhook and email keys removed; Phase 9 rewritten; email subscriptions added to Phase 10.
- 2026-10-28: D5 decided: Next.js + React + deck.gl, TanStack Query + Zustand + URL filters, Plotly replacing Vega-Lite. Crawler rules added to `02-TECH-STACK.md`. D15 (urban-form analysis) opened.
- 2026-10-28: D6 decided: laptop through Phase 8; VM + Vercel + R2 from Phase 9; public lots, sign-in for the rest. Phase 9 grows to L with the deploy and sign-in. D16 (sign-in provider) opened.
- 2026-10-28: D7 decided as proposed. "Buyer profile" defined in `06-SITE-REVIEW-AGENT.md` § 3 as a user's investment thesis, not an owner in the data.
- 2026-10-28: D8 decided: twelve triggers (`zoning_changed` and `watched_buyer_bought` added); buyer names on every sale; `buyer_is_company` flag; `watchlist.yaml` added to the layout.
- 2026-10-28: D9 decided as proposed; the Phase 8 checkpoint now compares models and effort on the eval.
- 2026-10-28: D10 decided: Meridian XYZ brand guidelines; token and chart-color rules added to `04-CODING-STANDARDS.md`.
- 2026-10-28: D11 decided: walking distances on the OpenStreetMap network, built in Phase 5 (now L); straight-line distances removed everywhere; `network/` added to the layout; OSM added as an outside service.
- 2026-10-28: D17 added and decided: comps and nearby activity search by neighborhood (default the lot's NTA), chosen neighborhoods or a lasso; `POST /areas`, `GET /lots/{bbl}/comparables` and `search_areas` added.
- 2026-10-28: D13 decided: no city column; one database per city.
- 2026-10-28: D15 decided: `08-URBAN-FORM.md` added with the nine-level ladder; Phase 5.5 added; `form/`, `area_metrics` added; levels 6–9 added to Phase 10.
- 2026-10-28: D16, D18 and D19 decided; D20 (payments) opened. Account tiers added; Postgres app database from Phase 7; Phase 9.5 (accounts and payments) added; Phase 5b renamed 5.5.
- 2026-10-28: D20 deferred to Phase 9.5. D21 decided: the first delivery is Phases 0–9 with the full agent; "Deliveries" section added.
- 2026-10-28: pricing, trial and own-key details moved to the owner's private notes before the repo went public.
- 2026-10-29: root docs (`README.md`, `AGENTS.md`, `CLAUDE.md`, `SPEC.md`, `BRAND.md`), the spec template and the folder layout added; lasso search moved to Phase 7, where the app database arrives.
- 2026-10-29: each phase in `07-BUILD-PHASES.md` now has one build list, and the Who column left `SPEC.md`. All text follows `docs/WRITING_AND_COMMUNICATION_RULES.md`.
