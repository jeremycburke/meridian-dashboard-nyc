# Glossary

The words and measures that this project uses, with one meaning each.
Look up a word here before you use it in code, in a policy or in a decision letter.
If a word is not here and the work needs it, add it here first.

## Project terms

| Term | Meaning |
|---|---|
| Site | One tax lot with its buildings, identified by its BBL. A condo unit or a co-op apartment is never a site (D2). |
| Developer type | One type of buyer: safe and institutional, standard, or opportunistic (D10). |
| Policy | What one developer type is willing to do: its clauses and its two risk limits. Each policy is one YAML file in [`profiles/`](../profiles/). |
| Clause | One numbered rule in a policy, for example "3.1: the lot area is 10,000 sq ft or more". |
| Deal-breaker | A clause that fails when the site has a named problem, for example a landmark designation. |
| Risk factor | One named problem that adds points to the risk score, for example an open vacate order. [`risk_factors.yaml`](../profiles/risk_factors.yaml) lists them. |
| Risk score | The sum of the points for the risk factors that a site has, with a maximum of 100. All three developer types read the same score. |
| Risk limits | The two highest risk scores at which a policy still gives Buy and Review. |
| Verdict | Buy, Review or Pass, for one site under one policy. |
| Buy | In the code verdict: every clause passes, and the risk score is at or below the Buy limit. |
| Review | In the code verdict: a clause has no data, or the risk score is above the Buy limit and at or below the Review limit. A person must look at the site. |
| Pass | In the code verdict: a clause fails, or the risk score is above the Review limit. |
| Code verdict | The verdict that code gives from the clauses and the risk score, with no model. |
| Agent | One model with its settings, for example Claude Opus 5.5 at medium effort. An agent's verdict is its own judgment, and no rule limits it (D11). |
| Tool | A read-only function that an agent calls to get facts, for example `get_site_card`. |
| Harness | The code that runs the tool loop. It sends the task, runs each tool that the agent asks for, and sends the results back (D12). |
| Site card | The facts about one site, in fixed sections, each with its source and pull date. |
| Decision letter | An agent's short write-up of its verdict, with the clauses and the evidence. |
| Answer key | The verdicts that count as right when an agent is graded. Not decided yet. |

## Property and data terms

| Term | Meaning |
|---|---|
| Tax lot | A unit of real estate that the city taxes. |
| BBL | Borough, block and lot: the ten-digit number of a tax lot. One borough digit, five block digits, four lot digits. `1000477501` is 120 Broadway. |
| BIN | The seven-digit number of a building. One lot can hold several buildings. |
| Building class | The Department of Finance code for what stands on a lot, for example `A1` for a one-family house. Classes that start with `R` are condos. `C6`, `C8`, `D0` and `D4` are co-ops. |
| Condo lot | A lot divided into units that are owned and sold one at a time. PLUTO shows only the condo's billing lot. |
| Co-op building | A building that a cooperative corporation owns. Its apartments sell as shares in the corporation. |
| FAR | Floor area ratio: floor area as a multiple of lot area. A 5,000 sq ft lot with an FAR of 2 can hold 10,000 sq ft of floor area. |
| Maximum FAR | The largest FAR that the zoning allows for one use: homes, commerce or community facilities. |
| Built FAR | The FAR of the buildings on the lot today. |
| Unused floor area | The floor area that the zoning allows but that no building uses yet. |
| Buildable square feet | The largest of the maximum FARs, times the lot area. |
| Zoning district | The area where one set of zoning rules applies, for example `R6` or `C4-4A`. |
| E-designation | A city restriction on a lot for hazardous materials, noise or air quality. Building work on the lot needs extra review. |
| Landmark | A building or site that the Landmarks Preservation Commission (LPC) protects. A change to it needs LPC approval. |
| Historic district | An area that LPC protects. A change to a building in it needs LPC approval. |
| MIH area | A Mandatory Inclusionary Housing area. New homes there must include affordable homes. |
| Transit zone | An area near transit where the zoning asks for less parking. |
| FEMA flood zone | The area with a 1% chance of a flood each year, on the 2015 preliminary flood map of the Federal Emergency Management Agency. |
| Vacate order | An order from the Department of Housing Preservation and Development (HPD) that people must leave a building, or part of one, because it is not safe. It stays open until HPD rescinds it. |
| Job filing | An application to the Department of Buildings (DOB) for building work. v0 uses new buildings, full demolitions and major rebuilds. |
| Market sale | A sale of $100,000 or more. Code flags every sale below that, and keeps it (D8). |
| Market value | The Department of Finance (DOF) estimate of a lot's value, for property tax. It can be far from a sale price. |
| NTA | A 2020 Neighborhood Tabulation Area: one of 262 neighborhoods that City Planning builds from census tracts. v0 uses the NTA as "the neighborhood" (D6). |
| Census tract | A small area for which the Census Bureau publishes statistics. |
| ACS | The American Community Survey: Census Bureau estimates of income, rent and population. v0 uses the 5-year estimates (D7). |
| PLUTO | City Planning's table of every tax lot, with its zoning, size, buildings and owner. |
| Rolling sales | The Department of Finance list of the sales in the last 12 months. |
| ZoLa | City Planning's zoning map website, `zola.planning.nyc.gov`. |

## Measures

Each measure that a policy clause or a risk factor uses.
The names follow the conventions in [`AGENTS.md`](../AGENTS.md): the unit is in the name, and a yes-or-no measure starts with `is_` or `has_`.

| Measure | Unit | Definition | Source | Does not measure |
|---|---|---|---|---|
| `borough` | Code | `MN`, `BX`, `BK`, `QN` or `SI` | PLUTO `borough` | — |
| `lot_area_sqft` | sq ft | The area of the lot | PLUTO `lotarea` | Easements, or the part of the lot that can hold a building |
| `unused_floor_area_sqft` | sq ft | (The largest of `residfar`, `commfar` and `facilfar`, minus `builtfar`) times `lotarea`. Never below 0 | PLUTO | Zoning bonuses, transferred development rights, height and lot-coverage limits, landmark limits, or whether the use with the largest FAR suits the buyer |
| `price_usd` | US dollars | The first that exists: the asking price that you enter, the last market sale in the last 12 months, or the market value | Your input, rolling sales, property valuation | The price a buyer would pay today |
| `walk_to_subway_min` | Minutes | The walking time at 3 miles an hour along the OpenStreetMap walking network, from the lot's center point to the nearest subway entrance | PLUTO `latitude` and `longitude`, OpenStreetMap, MTA | Waiting time, train frequency, stairs and elevators, or where the trains go |
| `is_landmark_or_historic_district` | Yes or no | Yes when PLUTO names a landmark or a historic district for the lot | PLUTO `landmark`, `histdist` | Sites that LPC is only considering for designation |
| `is_in_2015_flood_zone` | Yes or no | Yes when PLUTO `pfirm15_flag` is 1 | PLUTO `pfirm15_flag` | Rainfall flooding, the 0.2% flood zone, or future sea-level rise |
| `has_open_vacate_order` | Yes or no | Yes when HPD has a vacate order on the lot with no rescind date | HPD vacate orders | DOB vacate orders, or whether the order covers the whole building |
| `residential_units` | Count | The homes on the lot | PLUTO `unitsres` | Whether anyone lives in them, or whether their rents are regulated. v0 counts every home as occupied |
| `has_e_designation` | Yes or no | Yes when PLUTO lists an E-designation number for the lot | PLUTO `edesignum` | The kind of restriction: hazardous materials, noise or air |
| `has_market_sale_last_12_months` | Yes or no | Yes when rolling sales hold a market sale of the lot in the last 12 months | Rolling sales | Sales older than 12 months |
| `is_price_per_sqft_above_neighborhood_median` | Yes or no | Yes when the site's price per buildable square foot is above the median for the market sales of the same building class category in the same NTA, in the last 12 months | Rolling sales, PLUTO | Condition, tenants, or any other reason behind a price |

## Proposed rules for missing data

These rules are proposals. The owner has not confirmed them yet.

1. A risk factor whose measure has no data adds no points. The site card says that the data is missing.
2. The neighborhood median needs at least 5 market sales. With fewer, `is_price_per_sqft_above_neighborhood_median` has no data.
3. Price per square foot uses buildable square feet, so that a vacant lot and a built lot compare on the same basis.
