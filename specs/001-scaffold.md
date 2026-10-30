# S001 — Scaffold: install, lint, test

**Status:** done
**Phase:** 0
**Plan sections:** docs/plan/07-BUILD-PHASES.md § Phase 0; docs/plan/02-TECH-STACK.md § Language and tooling
**Depends on:** none
**Decisions:** D1, D2 · Open: none (⚠1 settled 2026-10-29)

## Goal

A fresh clone installs with `uv sync` and passes `uv run pytest` and `uv run ruff check .`.
One small module, `config.py`, holds where the data lives, when the event logs start, and the keys from `.env`.
The project is a minimal Python project: a `pyproject.toml`, a lock file, one package and one tests folder.

## Scope

**In:**

- `pyproject.toml`, `uv.lock` and `.python-version`, made with `uv init --bare --package`, `uv python pin 3.12` and `uv add`.
- `config.py`.
- `tests/test_config.py`.
- `README.md` § Getting started.

**Out, and when it comes back:**

| Left out | Comes back |
|---|---|
| A Makefile | Not planned. Commands are `uv run ...`. When Node arrives (S041), `package.json` scripts name the long ones. S031 picks the command for the daily refresh and replaces `make daily` in the plan |
| A pre-commit hook | S041, with lefthook through npm |
| GitHub CI | Not planned. The owner can add it later, for example before the site goes live (S055) |
| `runlog.py` | S002, with the first step to time |
| The network-blocking test fixture | S002, with the first code that goes online |
| `make specs` | Dropped. Each spec file shows its status under its title |
| DuckDB, GeoPandas and the other libraries | Each one arrives with `uv add` in the spec that first uses it |
| The 12 empty subpackages | Each one comes back with the spec that fills it |

## Inputs

No datasets.
The old repo's `src/urban_metrics/config.py`, read and never imported.

## Deliverables

- `pyproject.toml`:
  - Python 3.12.
  - The build backend `uv_build`, written by `uv init --package`. It finds `src/meridian_dashboard_nyc` from the project name (D1).
  - One dependency, `python-dotenv`.
  - `pytest` and `ruff` in the dev group (`uv add --dev`).
  - ruff: line length 100, and the rules `E`, `F`, `W`, `I`, `B`, `SIM`, `UP` and `C90` with a maximum complexity of 10.
  - pytest: `testpaths = ["tests"]`.
- `uv.lock` and `.python-version`.
- `src/meridian_dashboard_nyc/config.py`:
  - `ROOT`: the repo folder, from the location of this file.
  - `DATA`: `ROOT / "data"`.
  - `EVENT_LOG_START_DATE`: `date(2025, 1, 1)` (D2).
  - `load_dotenv()`, then `SOCRATA_APP_TOKEN = os.getenv("SOCRATA_APP_TOKEN")`. Later specs add their keys in the same way.
- `tests/test_config.py`: the three tests below.
- `README.md` § Getting started.

## Acceptance criteria

1. `config.DATA` is the `data` folder at the repo root.
2. `config.EVENT_LOG_START_DATE` is the date 2025-01-01.
3. A value set for `SOCRATA_APP_TOKEN` in the environment reaches `config.SOCRATA_APP_TOKEN`.

## Tests

| Criterion | Test |
|---|---|
| 1 | `test_s001_c1_paths_live_under_data` |
| 2 | `test_s001_c2_event_log_start_is_2025_01_01` |
| 3 | `test_s001_c3_env_values_come_through_config` |

Test 3 sets the variable with the pytest `monkeypatch` fixture, then reloads `config` with `importlib.reload`.
The reload is necessary because a module reads the environment once, when Python first imports it.

## Checks

- `uv run pytest` passes.
- `uv run ruff check .` and `uv run ruff format --check .` are clean.
- A fresh clone in a temporary folder runs `uv sync` and `uv run pytest` with no other step.
- `git status` does not show `.env`.

## Documents

- `README.md` § Getting started: each command run in order on the fresh clone.
- `AGENTS.md` and `CLAUDE.md`: the commands, a rule to keep code simple, and the writing rules in `docs/WRITING_AND_COMMUNICATION_RULES.md`.
- The plan files that describe the heavier scaffold, corrected in the same commit:
  - `SPEC.md`: the S001 section.
  - `docs/plan/07-BUILD-PHASES.md`: Phase 0.
  - `docs/plan/02-TECH-STACK.md`: the make and pre-commit rows, the `pyproject.toml` sketch, how `.env` is read.
  - `docs/plan/03-ARCHITECTURE.md`: the Makefile line in the folder tree.
  - `docs/plan/04-CODING-STANDARDS.md`: shorter Python rules.
- `docs/decisions.md` and the decision table in `docs/plan/00-INDEX.md`: D22, simple code with each tool added when first needed. D23, the code stays in `src/` (⚠1). D24, the writing rules. D25, one push for each finished spec.
- `docs/checkpoints/P0-<yyyy-mm-dd>.md`: a short note. This spec closes Phase 0.

## Open decisions (⚠ = owner decides; stop and ask)

- ⚠1 **Where the Python code lives.** The owner settled it on 2026-10-29. The code stays in `src/meridian_dashboard_nyc/`, with a build backend in `pyproject.toml`. The 12 empty subfolders go. Each one comes back with the spec that fills it.

## Changelog

- 2026-10-29: created. At the request of the owner, the first draft became a minimal scaffold: no Makefile, pre-commit hook, CI, run log, network block or status script in S001.
- 2026-10-29: the owner settled ⚠1 and kept `src/`. So `pyproject.toml` gets the `uv_build` backend, and pytest needs no `pythonpath`.
- 2026-10-29: the owner accepted the spec. Tests started.
- 2026-10-29: done. A fresh clone passed every check. The output is in `docs/checkpoints/P0-2026-10-29.md`.
