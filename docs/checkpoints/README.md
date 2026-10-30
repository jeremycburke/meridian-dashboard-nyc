# Checkpoints

One note per phase checkpoint: the build's record of what was built, how it was checked, and when.
Name each note `P<phase>-<yyyy-mm-dd>.md` (`P5.5-2026-12-01.md` for Phase 5.5).
Put screenshots and rendered figures in `img/`, named after the note.

## Format

```markdown
# P<phase> checkpoint · <yyyy-mm-dd>

**Specs:** S0nn to S0nn
**Result:** continue | fix | change the plan

## Commands run
The exact commands, in order.

## Output
Row counts, printed cards, tables, screenshots (img/...).

## Compared against
Each independent source (ZoLa, ACRIS, DOB, HPD, a map, the source's own count) and whether it matched.

## What broke and what changed
Bugs found, specs or plan files corrected, with the commit.

## Decision
Why the phase passes, or what must happen before it does.
```

## Rules

- The repo is public. Never paste a key, the text of a review made for a real buyer profile, or anything from `profiles/` or `watchlist.yaml`.
- Record agent checkpoints as marks (right, wrong, unclear), counts and costs.
- Write what was observed, not what was expected.
