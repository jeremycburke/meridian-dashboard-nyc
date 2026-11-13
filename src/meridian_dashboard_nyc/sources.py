"""The NYC Open Data sources this project pulls, one entry for each.

Each source lands in its own folder, data/raw/<name>/<date>/. Nothing here combines them.
A source with a "where" filter pulls only the rows that match it.
"""

from meridian_dashboard_nyc.config import EVENT_LOG_START_DATE

START = EVENT_LOG_START_DATE.isoformat()

SOURCES = {
    # The lot: one row for each tax lot, with its zoning, size and buildings.
    "pluto": {"portal_id": "64uk-42ks"},
    # Building activity: new buildings, demolitions and major rebuilds, filed since START.
    "dob_now_job_filings": {
        "portal_id": "w9ak-ipjd",
        "where": (
            "job_type in ('New Building', 'Full Demolition', "
            "'ALT-CO - New Building with Existing Elements to Remain') "
            f"AND filing_date >= '{START}'"
        ),
    },
    # Sales: the Department of Finance list of sales in the last 12 months.
    # Whole lots and buildings only: no condo units and no co-op apartments.
    "rolling_sales": {
        "portal_id": "usep-8jbt",
        "where": (
            "building_class_category not like '%CONDO%' "
            "AND building_class_category not like '%COOP%'"
        ),
    },
    # Distress: open HPD orders to vacate a whole building or part of one.
    "hpd_vacate_orders": {"portal_id": "tb8q-a3ar", "where": "actual_rescind_date IS NULL"},
}
