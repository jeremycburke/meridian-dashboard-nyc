# 01 — Data sources: the catalog

One row per dataset.
Every portal id, row count and URL was read from the live portals on 2026-10-22.

## How to read a row

| Column | Meaning |
|---|---|
| **Our id** | The dataset's name in this project. It names the folder, the Python module and the raw directory. |
| **Portal id** | The four-by-four code on NYC Open Data (`data.cityofnewyork.us/d/<id>`). "Bytes" means a DCP zip download. "NYS" means `data.ny.gov`. |
| **One row is** | The grain: what a single row describes. |
| **Rows** | The count on 2026-10-22, before any filter. |
| **Kind** | Register, event log or reference. See [`README.md`](README.md). |
| **Keep** | The filter that turns the full dataset into current state. "The start date" is the one start date every event log shares (below). |
| **Key** | The column that joins it to a lot or a building. |

Every event log shares one start date: **2025-01-01** (decision D2).
It is one setting in `config.py`, kept small for the first pass.
Moving it back adds history.

Three keys join almost everything.

- **BBL** is the ten-digit lot number: one borough digit, five block digits, four lot digits. `1000477501` is 120 Broadway.
- **BIN** is the seven-digit building number. One lot can hold several buildings.
- **Document id** is ACRIS's id for one recorded document. One deed can name several lots.

A condominium is one billing lot with many unit lots.
PLUTO carries the billing lot only.
`dtm_condo_units` maps each unit lot to its billing lot.
Write that mapping down in the lot module's README before the first sale is joined.

---

## A. The lot — Phase 1

What the lot is, how big it is, and what stands on it.

| Our id | Portal id | Publisher | One row is | Rows | Kind | Keep | Key |
|---|---|---|---|---|---|---|---|
| `pluto` | `64uk-42ks` | DCP | One tax lot | 858,284 | Register | Newest release (26v2 today) | BBL |
| `mappluto` | Bytes: `mappluto/nyc_mappluto_26v2_arc_shp.zip` (302 MB) | DCP | One tax lot with its shape | ~858,000 | Register | Newest release, same version as `pluto` | BBL |
| `pad` | Bytes: `pad/pad_26c.zip` (46 MB) | DCP | One address range on one lot and building | — | Reference | Newest release | BBL, BIN |
| `building_footprints` | `5zhs-2jue` | OTI | One building outline | 1,082,946 | Register | Newest pull | BIN, BBL |
| `dtm_condos` | `p8u6-a6it` | DOF | One condominium | 12,239 | Reference | Newest pull | billing BBL |
| `dtm_condo_units` | `eguu-7ie3` | DOF | One condo unit lot | 307,774 | Reference | Newest pull | unit BBL → billing BBL |

Notes.
- `pluto` is the attribute table on Open Data. It has no shapes. `mappluto` is the same release with shapes, from DCP's download site. The Open Data entry for MapPLUTO (`f888-ni5f`) is only a link.
- The `arc_shp` file is clipped to the shoreline. DCP also publishes an unclipped file. Use the clipped one for the map.
- `pluto` carries the FEMA flood flags (`firm07_flag`, `pfirm15_flag`). Group H uses them.
- Check that `pluto.version` equals the MapPLUTO file's version on every pull. A mismatch stops the land step.

## B. Zoning and land-use rules — Phase 2

What may be built on the lot.

| Our id | Portal id | Publisher | One row is | Rows | Kind | Keep | Key |
|---|---|---|---|---|---|---|---|
| `zoning_districts` | Bytes: `nycgiszoningfeatures_fgdb.zip` | DCP | One district, overlay, special district or limited-height polygon | — | Reference | Newest release | spatial |
| `zoning_tax_lots` | `fdkv-4t4z` | DCP | One lot's zoning labels | 857,951 | Register | Newest pull | BBL |
| `mih_areas` | `m79g-k9r4` | DCP | One Mandatory Inclusionary Housing area | 275 | Reference | Newest pull | spatial |
| `inclusionary_housing_areas` | `e9rz-c67w` | DCP | One Inclusionary Housing designated area | 55 | Reference | Newest pull | spatial |
| `transit_zones` | `6ztr-wgff`, `vhqf-adkz` | DCP | One transit zone (parking rules) | 5, 1 | Reference | Newest pull | spatial |
| `e_designations` | `hxm3-23vy` | DCP | One environmental restriction on a lot | 13,956 | Register | Newest pull | BBL |
| `landmark_sites` | `buis-pvji` | LPC | One individual landmark site | 1,532 | Register | Newest pull | BBL, spatial |
| `historic_districts` | `skyk-mpzq` | LPC | One historic district | 141 | Reference | Newest pull | spatial |
| `lpc_buildings` | `gpmc-yuvp` | LPC | One building in a landmark or district | 38,105 | Register | Newest pull | BIN, BBL |

Notes.
- `zoning_districts` replaces the Open Data entry `mm69-vrje`, which is a 2013 attachment.
- PLUTO already carries each lot's zoning district and its maximum FAR by use. FAR is floor area ratio: the floor area a lot may hold, as a multiple of its lot area. These datasets add the overlays, special districts and restrictions that PLUTO summarizes or leaves out.
- `transit_zones` matters because parking requirements differ inside them. `vhqf-adkz` is the newer Greater Transit Zone. Confirm which one current rules use before any metric reads it.

## C. Ownership and money — Phase 3

Who owns the lot, what it sold for, what it is assessed at, and what it owes.

| Our id | Portal id | Publisher | One row is | Rows | Kind | Keep | Key |
|---|---|---|---|---|---|---|---|
| `acris_master` | `bnx9-e6tj` | DOF | One recorded document | 17,117,230 | Event log | Documents recorded since the start date, plus the newest deed on every lot | document id |
| `acris_legals` | `8h5j-fqxa` | DOF | One lot named on one document | 22,797,599 | Event log | Rows whose document is kept | document id → BBL |
| `acris_parties` | `636b-3b5g` | DOF | One party on one document | 46,695,140 | Event log | Rows whose document is kept | document id |
| `acris_document_codes` | `7isb-wh4c` | DOF | One document type code | 126 | Reference | Newest pull | `doc_type` |
| `acris_property_types` | `94g4-w6xz` | DOF | One property type code | 49 | Reference | Newest pull | code |
| `rolling_sales` | `usep-8jbt` | DOF | One sale in the last 12 months | 82,576 | Event log | Whole file (it is already a 12-month window) | borough-block-lot |
| `property_valuation` | `8y4t-faws` | DOF | One lot's market and assessed value for one tax year and roll | 11,685,588 | Register | Newest `year` and its newest `period` (2027 today, about 1.18 million rows) | `parid` → BBL |
| `property_exemptions` | `muvi-b6kx` | DOF | One exemption on one lot | 3,574,260 | Register | Newest `year` | `parid` → BBL |
| `property_abatements` | `rgyu-ii48` | DOF | One abatement on one lot | 3,246,890 | Register | Newest `taxyr` | `parid` → BBL |
| `tax_lien_sale_list` | `9rz4-mjek` | DOF | One lot on a lien sale list | 264,142 | Event log | Newest `cycle` and `month` | borough-block-lot |
| `property_charges_balance` | `scjx-j6np` | DOF | One charge on one lot | 136,838,310 | Event log | **Not landed.** Asked per lot at review time. | BBL |

Notes.
- ACRIS is three linked tables. Master holds the document, legals hold the lots it names, parties hold the buyer and seller. Join on `document_id`.
- Deed prices in ACRIS are reliable from 2003. A $0 or $10 deed is not a sale. Flag non-market deeds; never delete them.
- `rolling_sales` is DOF's cleaned list of sales. It is the fastest route to comparable sales. ACRIS is the route to ownership and debt.
- `property_charges_balance` is too large to download in bulk. It is the project's one live lookup: the review asks the API for one lot's rows.
- `speculation_watch_list` (Group E) also carries a sale price and a cap rate per deed.

## D. Building activity — Phase 3

What is being built, altered or torn down.
New-building and demolition filings are the main signal of a new site.

| Our id | Portal id | Publisher | One row is | Rows | Kind | Keep | Key |
|---|---|---|---|---|---|---|---|
| `dob_now_job_filings` | `w9ak-ipjd` | DOB | One job filing in DOB NOW | 973,482 | Event log | Open jobs, plus jobs filed since the start date | job filing number, BBL, BIN |
| `dob_now_permits` | `rbx6-tga4` | DOB | One approved work permit in DOB NOW | 1,018,441 | Event log | Unexpired permits, plus permits issued since the start date | job filing number, BBL |
| `dob_job_filings` | `ic3t-wcy2` | DOB | One job filing in the older BIS system | 2,716,299 | Event log | Open jobs, plus jobs filed since the start date | job number, BBL |
| `dob_permits` | `ipu4-2q9a` | DOB | One permit in the older BIS system | 3,991,021 | Event log | Unexpired permits, plus permits issued since the start date | job number, BBL |
| `dob_now_certificates` | `pkdm-hqz6` | DOB | One certificate of occupancy in DOB NOW | 83,282 | Event log | The newest certificate on every building, plus certificates issued since the start date | BBL, BIN |
| `dob_certificates` | `bs8b-p36w` | DOB | One certificate of occupancy in BIS | 143,258 | Event log | The newest certificate on every building, plus certificates issued since the start date | BBL, BIN |
| `housing_database` | `br6q-ssj3` | DCP | One housing job with net units and status | 111,909 | Register | Newest pull | job number, BBL |
| `affordable_housing` | `hg8x-zxpr` | HPD | One building in an affordable housing project | 9,551 | Register | Newest pull | BBL, BIN |

Notes.
- DOB runs two systems. BIS is the older one; DOB NOW replaced it for most filings. A full picture needs both. Unify them into one `filings` table and one `permits` table, each with a `system` column.
- `housing_database` is DCP's cleaned view of the same filings. It states net new units, which the raw filings do not. Use it to check the unified table.

## E. Condition and compliance — Phase 4

What is wrong with the building today, and who answers for it.

| Our id | Portal id | Publisher | One row is | Rows | Kind | Keep | Key |
|---|---|---|---|---|---|---|---|
| `hpd_violations` | `wvxf-dwi5` | HPD | One housing code violation | 11,333,664 | Event log | `violationstatus = 'Open'` (2,876,572 today) | BBL, BIN |
| `hpd_registrations` | `tesw-yqqr` | HPD | One registered multiple dwelling | 203,887 | Register | Newest pull | BBL, BIN, registration id |
| `hpd_registration_contacts` | `feu5-w2e2` | HPD | One owner, agent or manager on a registration | 810,494 | Register | Newest pull | registration id |
| `hpd_vacate_orders` | `tb8q-a3ar` | HPD | One vacate order | 8,941 | Event log | Orders with no rescind date | BBL, BIN |
| `hpd_aep_buildings` | `hcir-3275` | HPD | One building in the Alternative Enforcement Program | 4,387 | Register | Newest pull | BBL, BIN |
| `speculation_watch_list` | `adax-9mit` | HPD | One recent sale HPD flags as speculative | 797 | Register | Newest pull | BBL |
| `dob_violations` | `3h2n-5cm9` | DOB | One DOB violation | 2,477,418 | Event log | No disposition date (confirm at profile) | BBL, BIN |
| `dob_ecb_violations` | `6bgk-3dad` | DOB | One ECB violation with its penalty | 1,841,577 | Event log | Active status or a balance due (confirm at profile) | BBL, BIN |
| `dob_safety_violations` | `855j-jady` | DOB | One safety violation (elevators, boilers, facades) | 1,118,944 | Event log | `violation_status` open | BBL, BIN |
| `dob_complaints` | `eabe-havv` | DOB | One complaint to DOB | 3,145,939 | Event log | Entered since the start date | BIN |
| `dob_stalled_sites` | `i296-73x5` | DOB | One stalled-site complaint on one run date | 1,457,536 | Register | Newest `dobrundate` only | BIN |
| `facade_filings` | `xubg-57si` | DOB | One facade inspection filing | 87,483 | Register | Newest cycle per building | BBL, BIN |
| `ll84_energy` | `5zyy-y8am` | DOB | One building's energy and water use for one year | 103,259 | Register | Newest `report_year` per property | BBL, BIN |

Notes.
- `dob_stalled_sites` repeats every site on every run date. Keeping the newest run date gives the current list.
- `ll84_energy` covers buildings over 25,000 square feet. It gives energy use per square foot and an ENERGY STAR score. The Local Law 97 fine estimate is a calculation on top of it. That calculation is a metric with its own spec, not a column copied from the source.
- Contact names in `hpd_registration_contacts` and `facade_filings` are public. Show them as published. Never merge two names into one owner by guesswork.

## F. Public land and notices — Phase 4

City-owned land, land-use applications, hearings and auctions.

| Our id | Portal id | Publisher | One row is | Rows | Kind | Keep | Key |
|---|---|---|---|---|---|---|---|
| `city_owned_property` | `fn4k-qyk2` | DCP | One city-owned or leased property | 17,298 | Register | Newest pull | BBL |
| `zap_projects` | `hgx4-8ukb` | DCP | One land-use application | 32,964 | Event log | Open projects (filed, noticed, in public review), plus projects completed since the start date | project id |
| `zap_bbls` | `2iga-a6mk` | DCP | One lot named by one application | 132,090 | Event log | Rows whose project is kept | project id → BBL |
| `city_record` | `dg92-zbpx` | DCAS | One City Record notice | 1,112,805 | Event log | Four sections only (hearings and meetings, agency rules, property disposition, court notices), notices not yet ended | notice id; addresses in text |

Notes.
- City Record is mostly personnel changes. Pull with a section filter, never the bulk file. The old repo measured about 12,500 useful rows out of 1.1 million.
- A City Record notice names a place in free text. Matching it to a lot needs the geocoder in Group I.

## G. Neighborhood and access — Phase 5

What is near the lot: transit, schools, parks, shops, and what neighbors complain about.

| Our id | Portal id | Publisher | One row is | Rows | Kind | Keep | Key |
|---|---|---|---|---|---|---|---|
| `boroughs` | `yeji-bk3q` | DCP | One borough | 5 | Reference | Newest pull | spatial |
| `community_districts` | `5crt-au7u` | DCP | One community district | 71 | Reference | Newest pull | spatial |
| `ntas` | `9nt8-h7nd` | DCP | One 2020 neighborhood tabulation area | 262 | Reference | Newest pull | spatial |
| `council_districts` | `872g-cjhh` | DCP | One council district | 51 | Reference | Newest pull | spatial |
| `police_precincts` | `y76i-bdw7` | DCP | One precinct | 78 | Reference | Newest pull | spatial |
| `school_districts` | `8ugf-3d8u` | DCP | One school district | 33 | Reference | Newest pull | spatial |
| `school_zones` | `cmjf-yawu`, `t26j-jbq7`, `ruu9-egea` | DOE | One elementary, middle or high school zone | 770, 279, 80 | Reference | Newest pull | spatial |
| `subway_stations` | NYS `39hk-dx4f` | MTA | One station on one line | 496 | Reference | Newest pull | spatial |
| `subway_entrances` | NYS `i9wp-a4ja` | MTA | One entrance or exit | 2,120 | Reference | Newest pull | spatial |
| `bike_routes` | `mzxg-pwib` | DOT | One bike route segment | 29,695 | Reference | Newest pull | spatial |
| `parks` | `enfh-gkve` | DPR | One park property | 2,061 | Register | Newest pull | spatial |
| `facilities` | `ji82-xba5` | DCP | One civic facility (school, clinic, library, firehouse) | 34,446 | Register | Newest pull | BBL, spatial |
| `storefronts` | `92iy-9c3n` | DOF | One ground-floor storefront and whether it is vacant | 481,097 | Register | Newest `reporting_year` | BBL |
| `restaurants` | `43nn-pn8j` | DOHMH | One restaurant inspection | 295,356 | Event log | Newest inspection per restaurant | BBL |
| `business_licenses` | `w7w3-xahh` | DCWP | One issued license | 72,452 | Register | Active licenses | spatial |
| `liquor_licenses` | NYS `9s3h-dpkz` | SLA | One active liquor license | 60,066 | Register | Newest pull | spatial |
| `service_requests_311` | `erm2-nwe9` | OTI | One 311 request | 22,879,856 | Event log | Created since the start date | BBL, spatial |
| `collisions` | `h9gi-nx95` | NYPD | One motor vehicle crash | 2,269,187 | Event log | Crashes since the start date | spatial |

Notes.
- `service_requests_311` is the largest dataset kept. Pull it with a date filter through the API. Choose the complaint types the reviews use before the first full pull.
- Every distance is a walking distance on the OpenStreetMap street network (decision D11), from each lot to the nearest destination of each kind. There are no straight-line distances. The destination kinds (transit, schools, grocery stores, ...) are chosen in the walking-network spec.

## H. Hazard — Phase 5

| Our id | Portal id | Publisher | One row is | Rows | Kind | Keep | Key |
|---|---|---|---|---|---|---|---|
| `hurricane_evacuation_zones` | `epne-qv9x` | DCP | One evacuation zone | 8 | Reference | Newest pull | spatial |
| `stormwater_flood_maps` | `9i7c-xyvv` | DEP | One flood scenario layer | file | Reference | Newest file | spatial |

PLUTO's FEMA flags (Group A) cover the 2007 flood map and the 2015 preliminary map.
These two datasets add storm surge and rainfall flooding.

## I. Services outside NYC Open Data

These are services the code calls, not datasets it lands.

| Service | What it does | Key needed | Phase |
|---|---|---|---|
| NYC GeoSearch, `https://geosearch.planninglabs.nyc/v2/search` | Turns an address into BBL and BIN. Checked 2026-10-22: "120 Broadway" returns BBL `1000477501`, BIN `1001026`, PAD 26c. | No | 1 |
| Protomaps basemap | The street map drawn under the lots | No | 6 |
| Census ACS API | Population, income and rent by tract, from the newest ACS 5-year release (decision D14) | Yes (`CENSUS_API_KEY`) | 10, optional |
| OpenStreetMap, through `osmnx` | The walkable street network of the five boroughs, for walking distances (D11). Saved like a register pull under `raw/osm_walk_network/<date>/` and refreshed monthly. Licensed ODbL: every page that shows a walking distance credits "© OpenStreetMap contributors". | No | 5 |
| MTA GTFS static feed | Subway and bus schedules, for headways | No | 10, optional |

---

## Totals

| Group | Datasets | Phase |
|---|---|---|
| A. The lot | 6 | 1 |
| B. Zoning and land-use rules | 9 | 2 |
| C. Ownership and money | 11 (one lookup only) | 3 |
| D. Building activity | 8 | 3 |
| E. Condition and compliance | 13 | 4 |
| F. Public land and notices | 4 | 4 |
| G. Neighborhood and access | 18 | 5 |
| H. Hazard | 2 | 5 |
| **Total** | **71** | |

## Adding a dataset

A dataset joins this catalog through the add-a-dataset process in [`../05-PROCESSES.md`](../05-PROCESSES.md).
Its row here is written first, before any code.
