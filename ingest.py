"""Local one-time data ingest for the NOSHIP Trade Tracker.

Run this on YOUR machine (where `.env` holds your private API keys). It pulls
trade data for a single country through a single port over a span of years and
writes it into a committed SQLite database (`data/trade.db`). The public
Streamlit dashboard then reads only from that file and never touches an API or
your key.

Examples:
  # Default: Israel, last 13 years, Port of New Orleans, Census source, HS6
  python ingest.py

  # A different country / span
  python ingest.py --country Sudan --years-back 7

  # A country not in the built-in name->code map
  python ingest.py --country "South Korea" --country-code 5800

  # Use a different HS specificity level
  python ingest.py --hs-level HS2
"""

from datetime import date
import click

from src.models import TradeDirection
from src.sources import census
from src import database

# US Census Bureau "Schedule C" country codes. TODO: What a weird selection of countries. Should we pick some more useful ones?
COUNTRY_NAME_TO_CODE: dict[str, str] = {
  "israel": "5081",
  "brazil": "3510",
  "china": "5700",
  "germany": "4280",
  "japan": "5880",
  "mexico": "2010",
  "canada": "1220",
  "united kingdom": "4120",
  "france": "4279",
  "india": "5330",
}

# Customs district code -> human-readable port name.
DISTRICT_TO_PORT_NAME: dict[str, str] = {
  "2101": "New Orleans, LA",
}

SOURCE_MAP = {
  "census": census,
}


def _resolve_country_code(country: str, country_code: str | None) -> str:
  if country_code:
    return country_code
  code = COUNTRY_NAME_TO_CODE.get(country.strip().lower())
  if not code:
    raise click.ClickException(
      f"No built-in Census country code for `{country}`. "
      f"Pass --country-code with Schedule C code "
      f"(see https://www.census.gov/foreign-trade/schedules/c/countryname.html)."
    )
  return code

def _months_for_year(year: int, today: date) -> list[int]:
  """Months to request for a given year.

  For past years, all 12 months. For the current year, only months up to and
  including the current month (later months aren't published yet, so querying
  them just produces errors). For any future year, nothing.
  """
  if year < today.year:
    return list(range(1,13))
  if year == today.year:
    return list(range(1, today.month + 1))
  return []


@click.command()
@click.option("--country", default="Israel", show_default=True,
              help="Country name to ingest (used for labeling and code lookup).")
@click.option("--country-code", default=None,
              help="Census Schedule C country code. Overrides the name lookup.")
@click.option("--years-back", default=13, show_default=True, type=int,
              help="How many years back from the current year to fetch.")
@click.option("--district", default="2101", show_default=True,
              help="Customs district code (default 2101 = Port of New Orleans).")
@click.option("--source", default="census", show_default=True,
              type=click.Choice(list(SOURCE_MAP.keys()), case_sensitive=False),
              help="Data source to ingest from.")
@click.option("--hs-level", default="HS6", show_default=True,
              type=click.Choice(["HS2", "HS4", "HS6", "HS10"], case_sensitive=False),
              help="HS specificity level to request from the API.")
@click.option("--db", "db_path", default=str(database.DEFAULT_DB_PATH), show_default=True,
              help="Path to the SQLite database to write.")
def main(country, country_code, years_back, district, source, hs_level, db_path):
  """Download trade data into the local database."""
  src = SOURCE_MAP[source]
  code = _resolve_country_code(country, country_code)
  port_name = DISTRICT_TO_PORT_NAME.get(district, f"District {district}")

  today = date.today()
  current_year = date.today().year
  start_year = current_year - years_back
  years = list(range(start_year, current_year + 1))

  click.echo(
    f"Ingesting {source} data for {country} (code {code}) through "
    f"{port_name} [{district}]"
  )
  click.echo(f"HS Level: {hs_level}")
  click.echo(f"Years: {years[0]}..{years[-1]} ({len(years)} calendar years)\n")

  total_saved = 0

  for year in years:
    for month in _months_for_year(year, today):
      for direction, fetch in (
        (TradeDirection.IMPORT, src.fetch_imports),
        (TradeDirection.EXPORT, src.fetch_exports),
      ):
        label = direction.value
        try:
          records = fetch(
            year,
            month=month,
            country_code=code,
            hs_level=hs_level,  # <-- NEW
          )
        except Exception as e:
          click.echo(f"   {year}-{month:02d} {label:7s}   ERROR: {e}")
          continue

        # Keep stored port label in sync with requested district
        for r in records:
          r.port_code = district
          r.port_name = port_name

        saved = database.save_records(records, db_path=db_path)
        total_saved += saved
        click.echo(f"   {year}-{month:02d} {label:7s}   {saved:6d} records")

  click.echo(f"\nDone. Wrote {total_saved} records to {db_path}.")
  click.echo("Commit this file so the deployed dashboard can read it:")
  click.echo(f"   git add {db_path}")


if __name__ == "__main__":
  main()
