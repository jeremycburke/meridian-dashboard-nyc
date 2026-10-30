# 08 — Urban form: metrics from simple to complex

This file is decision D15.
It lists the urban-form metrics in the order they are built, from simple to complex.
Each level is one spec and one checkpoint.
A level starts only after the one before it has been checked on real data.

Levels 1–5 are Phase 5.5, at two grains: the lot and the neighborhood (2020 NTA).
Levels 6–9 come later, one at a time, as new datasets and techniques earn their place.

## How a level is added

The same steps for every level, so complexity can grow without new plumbing.

1. **Spec.** Written from `specs/000-TEMPLATE.md`, naming the level and its ⚠ items.
2. **Module.** One file under `src/meridian_dashboard_nyc/form/`, registered in order.
3. **Metrics.** Each one versioned (`lot_coverage@v1`), with a docstring that says what it measures and what it does not, and a row in `metric_meta` giving its grain, inputs and version.
4. **Computed once.** Lot grain into `lot_metrics`; area grains (NTA now; block and cell later) into `area_metrics`. Nothing recomputes a metric elsewhere.
5. **Measured by the rules.** Areas and lengths in EPSG:2263 through `geo.py`; walking through `network/` (D11).
6. **One figure.** A Plotly figure per level from Python: data and layout, no colors (D5, D10).
7. **Shown without new page code.** The dashboard lists metrics from `metric_meta`, so a new level appears on the map and the Stats page by itself.
8. **Usable by profiles.** Once a metric exists, a buyer profile may screen on it or show it, and comps carry it (D17).

## The ladder

| Level | Family | Metrics (examples) | Inputs | Grain | Phase |
|---|---|---|---|---|---|
| 1 | Lot and building basics | Lot coverage, built FAR, building age, floors, units per acre, floor area by use | `pluto`, `mappluto` | Lot, NTA | 5.5 |
| 2 | Building geometry | Footprint coverage, roof height, footprints per lot, footprint compactness and elongation | `building_footprints`, `mappluto` | Lot, NTA | 5.5 |
| 3 | Density and use mix | Units and floor area per acre; the floor-area split by use; land-use mix entropy | `pluto` | Lot, NTA | 5.5 |
| 4 | Street network form | Intersection density, mean street-segment length, average node degree, street orientation order | OSM walking network | NTA | 5.5 |
| 5 | Walking access | Destinations of each kind within a 5, 10 and 15-minute walk; floor area by use within a 10-minute walk | `network/`, `places`, `pluto` | Lot, NTA | 5.5 |
| 6 | Block grain | Levels 1–5 summarized by tax block | Levels 1–5 | Block | Later |
| 7 | Morphometrics (`momepy`) | A morphological tessellation; building, cell and street metrics on it, aggregated to lot and NTA | `building_footprints`, OSM walking network | Cell, lot, NTA | Later |
| 8 | Region embeddings (`srai`) | Feature counts on H3 cells and NTAs (`CountEmbedder`) first; learned embeddings (Hex2Vec, and GTFS2Vec once GTFS lands) after | OSM tags, GTFS | H3, NTA | Later |
| 9 | Urban-fabric typology | Level 7 metrics clustered into fabric types, following the Urban Taxonomy method | Level 7 | Cell, lot, NTA | Later |

Levels 1 and 3 are SQL over PLUTO.
Level 2 adds geometry.
Levels 4 and 5 need the walking network from Phase 5.
Level 7 is the first that needs a new library and a new spatial unit.
Levels 8 and 9 bring in outside methods.

## The two outside sources

| Source | What it is | Fit here | Level |
|---|---|---|---|
| [Urban Taxonomy](https://urbantaxonomy.org/docs.html) (Charles University) | A published hierarchical classification of European urban fabric: each building and morphotope labeled at seven levels, from 76 morphometric columns | Europe only. For NYC, rerun the method (its code is linked as `uscuni/himoc`) rather than use the data. Its labels describe European fabric and may not map onto NYC's grid. The docs page states no license; check it before reuse. | 9 |
| [srai](https://github.com/kraina-ai/srai) (Kraina, Apache-2.0, `pip install srai`) | Geospatial ML at region level: H3, S2 and Voronoi regions; OSM, Overture and GTFS loaders; count and learned embeddings | Regions, not parcels: results join to NTAs or H3 cells. `CountEmbedder` is simple; the torch embedders are not. Under heavy development, with breaking changes between minor versions, so pin the version. | 8 |

Both were read on 2026-10-28.

## Open items for the level specs (⚠)

- Walking speed for the 5, 10 and 15-minute walks. Proposed: 80 m a minute, about 4.8 km/h.
- The destination kinds (D11).
- Which PLUTO use classes count as which use in the mix.

## Where the old repo did this

The old repo planned the same layer as "Phase B, the urban-form layer", after its product checkpoint.
Read its draft specs S029–S035 and research question Q47 (`docs/meridian/13-RESEARCH-QUESTIONS.md`) before writing the level 1 spec.
