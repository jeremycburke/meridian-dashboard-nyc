# Roadmap

v0 is the current work. [`docs/V0.md`](docs/V0.md) describes it.
This file lists the work planned after v0, in rough order.
Each item starts only when the owner chooses it.

## Next: the dashboard

A map and a dashboard on top of v0:

- A map of the sites, colored by the verdict for each developer type.
- A site page with the site card, the verdicts and the decision letters.
- A page that compares the agents.

The planned stack is Next.js and React, deck.gl over a MapLibre basemap, and Plotly for charts.
A read-only FastAPI service serves the data. The dashboard never opens a database itself (decision D19).

## History

- Sales since 2016, from the DOF annualized sales, and the change in price between a lot's sales.
- A backtest: score past sales, then check what happened to each lot afterward.
- Older PLUTO releases, so that a backtest sees each lot as it was at the time of the sale.

## More data

v0 uses 10 sources. The full catalog has 71 datasets from NYC Open Data, NYS Open Data and City Planning.

| Group | Examples |
|---|---|
| The lot | MapPLUTO lot shapes, the address directory, condo unit lots |
| Zoning | Zoning districts and overlays, landmark sites, inclusionary housing areas |
| Ownership and money | ACRIS deeds and owners, tax exemptions and abatements, the tax lien sale list |
| Building activity | DOB permits and certificates, the DCP housing database |
| Condition | HPD and DOB violations, building registrations, energy use |
| Public land and notices | City-owned property, land-use applications, City Record notices |
| Neighborhood | Schools, parks, civic facilities, storefronts, 311 requests |
| Hazard | Hurricane evacuation zones, stormwater flood maps |

## A daily refresh

- Pull the sources on a schedule.
- Find new sites each day, for example a demolition filing, a sale, a lien-sale listing or a rezoning.
- Review each new site against each policy, and post a daily digest to an Inbox page.

## Urban form, levels 4 and 6 to 9

[`docs/V0.md`](docs/V0.md) uses levels 1, 2, 3 and 5. The other levels are:

- Level 4: the form of the street network.
- Level 6: the v0 measures, summed up by city block.
- Level 7: detailed shape measures, with the `momepy` library.
- Level 8: descriptions of each area as numbers that a model can compare, with the `srai` library.
- Level 9: urban-fabric types, such as "dense row houses".

## Later

- Accounts, so that other companies can sign in and write their own policies.
- The daily digest by email.
- Subway frequency from the MTA timetables.
- Estimated exposure to Local Law 97, the city's limits on building emissions.
- A second city, with its own sources and database.

## How an item starts

Each item gets its own short design before any code, in the same way as [`docs/V0.md`](docs/V0.md).
Its decisions go into [`docs/decisions.md`](docs/decisions.md).
