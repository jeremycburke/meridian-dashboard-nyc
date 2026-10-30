# 01 — Data sources: overview

This folder says what data the project uses, how each pull is stored, and how each source is reached.
It has three files after this one.

| File | Question it answers |
|---|---|
| [`sources.md`](sources.md) | What is each dataset, who publishes it, and which rows do we keep? |
| [`raw.md`](raw.md) | Where does a pull land on disk, and what are the rules for it? |
| [`api.md`](api.md) | How do we fetch each source: which endpoint, which query, which key? |

Every dataset ID, row count and URL in these files was checked against the live portals on 2026-10-22.
Row counts change daily. Treat them as orders of magnitude, not targets.

## The one rule: current state only

The old repo kept 24 releases of PLUTO, from 2002 to 2026, and built history on top of them.
This project keeps none of that.
It holds the city as it stands today.

"Current" means something different for each kind of dataset.
Every dataset in `sources.md` is tagged with one of three kinds.

| Kind | What one row is | What "current" means | Examples |
|---|---|---|---|
| **Register** | A thing as it is now | The newest release only | PLUTO, building footprints, facilities, HPD registrations |
| **Event log** | Something that happened on a date | Items still open, plus everything since the start date | Deeds, permits, violations, 311 complaints |
| **Reference** | A code list or a boundary | The newest release only | ACRIS document codes, district boundaries, zoning districts |

A register is easy: download the newest release and replace the last one.

An event log needs a rule.
A deed from 1987 is history.
But the last deed on a lot, whatever its date, says who owns it now.
So each event log keeps two things:

1. **The current state, whatever its age.** An open violation from 2009 is still a fact about the building today.
   So is the newest deed on a lot (who owns it) and the newest certificate of occupancy on a building (what it legally is).
2. **Everything since the start date.** Closed items since 2025-01-01 give context: recent sales, recent permits, recent complaints.

The start date is decision D2 in [`../00-INDEX.md`](../00-INDEX.md).
It is one setting in `config.py`, shared by every event log, and kept small for the first pass.
Moving it back adds history; [`raw.md`](raw.md) says what that costs at the next pull.
The per-dataset filters are in `sources.md`.

## Keeping the previous pull

The site-review agent needs to know what is new.
"New" means "in today's pull but not in the last one."
So the project keeps exactly two pulls of each dataset: the current one and the one before it.
That is the only history in the project.
It exists to compute a difference, not to study the past.

The daily refresh removes older pulls itself, after each run where every step succeeded (decision D3).
`raw.md` covers how this works on disk.

## Where the data comes from

Most sources are on NYC Open Data, which runs on a platform called Socrata.
A few are not.

| Portal | What we take from it | How we reach it |
|---|---|---|
| NYC Open Data (`data.cityofnewyork.us`) | Almost everything: PLUTO attributes, ACRIS, DOB, HPD, DOF, districts, notices | Socrata API (SODA) |
| NYS Open Data (`data.ny.gov`) | MTA subway stations and entrances; State Liquor Authority licenses | Socrata API, same as above |
| DCP Bytes of the Big Apple (`s-media.nyc.gov/.../bytes/`) | MapPLUTO lot shapes, the Property Address Directory (PAD), zoning district shapes | Zip file download |
| NYC GeoSearch (`geosearch.planninglabs.nyc`) | Address to lot number (BBL) and building number (BIN) | HTTP API, no key |
| Protomaps | The basemap under the map | One file per city extract |
| Census API (optional, later) | Population and income by tract | HTTP API, key |

## Inventory at a glance

`sources.md` lists 71 datasets in eight groups, plus four outside services.
Each is assigned to a build phase in [`../07-BUILD-PHASES.md`](../07-BUILD-PHASES.md).

| Group | Datasets | Phase | Why a buyer cares |
|---|---|---|---|
| A. The lot | 6 | 1 | What the lot is, how big, what stands on it |
| B. Zoning and land-use rules | 9 | 2 | What may be built there |
| C. Ownership and money | 11 | 3 | Who owns it, what it sold for, what it is assessed at, what it owes |
| D. Building activity | 8 | 3 | What is being built or torn down |
| E. Condition and compliance | 13 | 4 | What is wrong with the building today |
| F. Public land and notices | 4 | 4 | City land, land-use applications, hearings, auctions |
| G. Neighborhood and access | 18 | 5 | Transit, schools, parks, shops, complaints |
| H. Hazard | 2 | 5 | Flood and storm exposure |
| I. Outside services | 5 | 1, 5, 6, 10 | Addresses, the walking network, basemap, optional census and transit schedules |

## What is deliberately left out

These sources were in the old repo.
They are out of scope here because they are history, not current state.

- PLUTO vintages before the newest one.
- The zoning envelope across vintages, lot lineage, and lot genealogy.
- Project outcomes (entry price, exit price, multiple) and the spine that built them.
- The Greenpoint-Williamsburg rezoning study and all causal work.
- SEC EDGAR loan contracts and CMBS data.
- Federal economic series (BLS, BEA, FRED) and Overture Maps.

Any of these can return later through the add-a-dataset process in [`../05-PROCESSES.md`](../05-PROCESSES.md).
