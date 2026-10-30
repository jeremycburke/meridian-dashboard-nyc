# S000 — <Title>

**Status:** draft | accepted | in progress | done
**Phase:** <n>
**Plan sections:** docs/plan/<file> § <section>
**Depends on:** S<nnn>
**Decisions:** D<n> · Open: none | the ⚠ items below

## Goal

One paragraph: what exists when this is done that does not exist now.

## Scope

**In:** the modules, tables, commands and pages this spec produces.
**Out:** what is deferred, and to which spec.

## Inputs

Datasets (by id from `docs/plan/01-data-sources/sources.md`), tables, earlier specs.

## Deliverables

- `src/meridian_dashboard_nyc/<path>.py`: the functions and their signatures
- `tests/test_<module>.py`: the tests below
- `docs/SCHEMA.md`: the tables or columns added, written before the code

## Acceptance criteria

Numbered, binary, testable. Each one maps to a test.

1. ...
2. ...

## Tests

| Criterion | Test |
|---|---|
| 1 | `test_s000_c1_<what>` |
| 2 | `test_s000_c2_<what>` |

## Checks

The real run on real data, what you will look at, and what it is compared against.

- ...

## Documents

- The READMEs this spec writes or updates
- The checkpoint note, if this spec closes a phase: `docs/checkpoints/P<n>-<yyyy-mm-dd>.md`

## Open decisions (⚠ = owner decides; stop and ask)

- ...

## Changelog

- YYYY-MM-DD: created.
