# 05 — Processes

How work moves from an idea to running code, how you stay in control of it, and how the data stays current.

## 1. The build loop

Every piece of code goes through five steps.

```
spec ──▶ tests ──▶ code ──▶ checkpoint ──▶ status = done
```

1. **Spec.** A file in `specs/` says what will exist, what is out of scope, and how to tell it works. No code is written without a spec that names it.
2. **Tests.** Each acceptance criterion gets a test before the code. The tests fail first.
3. **Code.** Written until the tests pass and `uv run ruff check .` is clean.
4. **Checkpoint.** A real run on real data, with its output shown and reviewed. See section 2.
5. **Status.** The spec's status line moves to `done` in the same commit as the last code change.

A spec's status line is the only progress record:
`draft → accepted → in progress → done`.
Each spec file shows its status under its title.

### Who does what

| Work | Who |
|---|---|
| Specs | Claude drafts them from these plan files. The owner accepts or changes them. |
| Tests and code | Claude writes them against an accepted spec. The owner reviews them. |
| Open decisions (⚠) | The owner |

Before a merge, Claude walks the owner through the change file by file.

## 2. Checkpoints

A checkpoint is a stop where you see the work itself, not a description of it.

At every checkpoint:

1. Run the phase's commands on real data.
2. Show the real output: row counts, a printed lot card, a screenshot, a digest on the Inbox page.
3. Compare it against something independent: the city's own website for that lot, a count published by the source, a map.
4. Decide: continue, fix, or change the plan.
5. Write it up in `docs/checkpoints/` ([`SPEC.md`](../../SPEC.md) § Documenting the build).

No phase starts until the previous phase's checkpoint passed.
Each phase's checkpoint is written in [`07-BUILD-PHASES.md`](07-BUILD-PHASES.md).

Independent checks worth using:

| To check | Compare against |
|---|---|
| A lot's zoning | ZoLa (`zola.planning.nyc.gov`) |
| A building's filings, violations and certificates | DOB BIS and DOB NOW public portals |
| HPD violations and registrations | HPD Online |
| A sale or a deed | ACRIS document search |
| Assessed value | DOF property tax bills |
| Row counts | The `count(*)` query in [`01-data-sources/api.md`](01-data-sources/api.md) |

## 3. Specs

Copy `specs/000-TEMPLATE.md` for each new spec.
Number specs in build order: `001-scaffold.md`, `002-dataset-framework.md`, `003-pluto.md`.

```markdown
# S000 — <Title>

**Status:** draft | accepted | in progress | done
**Plan sections:** docs/plan/<file> § <section>
**Depends on:** S<nnn>
**Open decisions:** none | the ⚠ items below

## Goal
One paragraph: what exists when this is done that does not exist now.

## Scope
**In:** modules, tables, commands, pages this spec produces.
**Out:** what is deferred, and to which spec.

## Inputs
Datasets (by id from sources.md), tables, earlier specs.

## Deliverables
- `path/to/module.py`: functions and signatures
- `tests/test_x.py`: the tests that prove the criteria

## Acceptance criteria
Numbered, binary, testable.
1. ...

## Checkpoint
The real run, and what you will look at.

## Open decisions (⚠ = owner decides; stop and ask)
- ...

## Changelog
- YYYY-MM-DD: created.
```

If a spec and these plan files disagree, fix one of them in the same commit and say which in the spec's changelog.

## 4. Decisions

`docs/decisions.md` holds one line per decision: date, number, decision, reason.

```markdown
- 2026-10-28 · D1 · Repo `meridian-dashboard-nyc`, package `meridian_dashboard_nyc` · Package matches the distribution name, so the build backend needs no module-name override.
```

An open decision is marked ⚠ in the spec that meets it.
Claude stops at a ⚠ and asks.
It never resolves one by choosing a default in code.

The open decisions at the start are listed in [`00-INDEX.md`](00-INDEX.md).

## 5. Adding a dataset

The same nine steps for every dataset, in order.

1. **Catalog row.** Add the dataset to [`01-data-sources/sources.md`](01-data-sources/sources.md): id, portal id, grain, kind, keep filter, key.
2. **Metadata check.** Read the portal's metadata endpoint. Record the column list, `rowsUpdatedAt` and the row count.
3. **Pull and land.** Scaffold the package from the template. Run `pull` and `land`.
4. **Profile.** Write the profile into the dataset's README: rows, columns, types, nulls per column, key uniqueness, date range, geometry validity.
5. **Decide.** Confirm the keep filter. Decide the target table. If a canonical column or table is new, write the change into `docs/SCHEMA.md` first.
6. **Fixture and tests.** Cut a fixture of at most 20 rows from the landing file. Write the tests: column names and order, key uniqueness, the filter, the mapping.
7. **Clean and load.** Write `clean` and `load` until the tests pass.
8. **README.** Add measured sizes, quirks, and anything that surprised you.
9. **Register.** Add the dataset to `registry.py` with its cadence and watched columns.

The step that is skipped most often is 4.
Skipping it is how a 2013 attachment ends up loaded as current zoning.

## 6. The daily refresh

One command keeps everything current: `make daily`.
It runs these steps in order and stops at the first failure.

| Step | What it does |
|---|---|
| 1. `pull` | Pulls every dataset whose cadence says it is due and whose source has changed |
| 2. `land`, `clean`, `load` | Only for datasets that pulled something new |
| 3. `derive` | Recomputes `lot_metrics` |
| 4. `export` | Rebuilds `data/export/nyc.duckdb` |
| 5. `tiles` | Rebuilds layers whose data changed |
| 6. `detect` | Compares the two newest pulls; adds new sites to `site_queue` |
| 7. `review` | The agent reviews queued sites against each buyer profile, within each user's limits (D18) |
| 8. `digest` | Writes each profile's daily digest of finished reviews to the inbox |
| 9. `prune` | Keeps the two newest pulls of each dataset and removes the rest. Reached only when steps 1–8 succeeded |

Cadences:

| Cadence | Datasets |
|---|---|
| Daily | DOB filings, permits and certificates; HPD and DOB violations; ZAP; City Record; 311 |
| Weekly | ACRIS; DOB complaints; stalled sites; HPD registrations and vacate orders |
| Monthly | Rolling sales; footprints; facilities; storefronts; licenses; restaurants; collisions |
| By release | PLUTO and MapPLUTO, PAD, zoning, valuation roll, exemptions, abatements, lien list, LL84, districts, boundaries |

`GET /datasets` and the dashboard's data page show each dataset's last pull and flag any that are overdue.

## 7. Reviewing the agent

The agent's output is reviewed like code.

- **Weekly:** read ten reviews. Mark each one right, wrong or unclear, with a note.
- **Every wrong review** becomes an eval case: the lot, the profile, and what the review should have said.
- **Every prompt or profile change** runs the eval set before it merges.

[`06-SITE-REVIEW-AGENT.md`](06-SITE-REVIEW-AGENT.md) § 12 describes the eval set.

## 8. Working with Claude Code

### Model choice

Your standing policy from the old repo applies here.

| Model | Work |
|---|---|
| Fable | Design: specs, schema decisions, hard debugging, surfacing open decisions |
| Opus | Building against an accepted spec; first instances; code review |
| Sonnet | Repeating an established pattern; doc syncs; status updates |
| Haiku | Quick lookups; no repo changes |

### `AGENTS.md` and `CLAUDE.md`

The working rules for any coding agent live in [`AGENTS.md`](../../AGENTS.md) at the repo root.
[`CLAUDE.md`](../../CLAUDE.md) imports it and adds what applies only to Claude.
Edit them as the project grows; they and these plan files must agree.

## 9. Keeping the project healthy

- **Rebuildable.** The warehouse rebuilds from clean files. The export rebuilds from the warehouse. Back up `data/raw/` and nothing else needs a backup.
- **Pruning.** `make daily` ends with `prune`, which keeps the two newest pulls per dataset. A failed day stops before it, so the last good pull is never removed.
- **Source changes.** A source that renames or retypes a column fails `land` on its pinned types. Fix the dataset module and note the change in its README.
- **Upgrades.** One library at a time, tests after each.
