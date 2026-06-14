"""Local one-time data ingest for the NOLA Trade Tracker.

Run this on YOUR machine (where ``.env`` holds your private API keys). It pulls
trade data for a single coutnry through a single port over a span of years and
writes it into a committed SQLite database (``data/trade.db``). The public
Streamlit dashboard then reads only from that file and nevver touches an API or
your key.

Examples:
  # Default: Israel, last 13 years, Port of New Orleans, Census source
  python ingest.py

  # A different country / span
  python ingest.py --country Sudan --years-back 7

  # A country not in the build-in name->code map
  python ingest.py --country "South Korea" --country-code 5800

Re-running is safe: rows are replaced by key, so you can ingest several
countries into the same database by running this once per country.
"""

from datetime import date

import click

from src.models import TradeDirection
from src.sources import census
from src import database

# US Censuse Bureau "Schedule C" country codess. Extend this as you ingest more
# countries, or pass --country-code explicitly to override / add ad hoc.
COUNTRY_NAME_TO_CODE: dict[str, str] = { #TODO: What a weird selection of countries. lol. Pick some more apt ones?
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

# Customs district code -> human -readable port name. Today, the Census client is
# hard-wired to the New Orleans district (src/config.py:NOLA_DISTRICT_CODE);
# this map exists so the stored data is labeled correctly and so adding ports
# later is a small change rather than a schema migration.
DISTRICT_TO_PORT_NAME: dict[str, str] = {
  "2101": "New Orlenas, LA",
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
      f"No built-in Census country code for `{country}`."
      f"Pass --country-code with Schedule C code "
      f"(see https://www.census.gov/foreign-trade/schedules/c/countryname.html)."
    )
  return code


@click.command()
@click.option("--country", default="Israel", show_default=True,
              help="Coungtry name to ingest (used for labeling and code lookup).")
@click.option("--country-code", default=None,
              help="Census Schedule C country code. Overrides the name lookup.")
@click.option("--years-back", default=13, show_default=True, type=int,
              help="How many years back from the current year to fetch.")
@click.option("--district", default="2101", show_default=True,
              help="Customs district code (default 2101 = Port of New Orleans).")
@click.option("--source", default="census", show_default=True,
              type=click.Choice(list(SOURCE_MAP.keys()), case_sensitive=False),
              help="Data source to ingest from.")
@click.option("--db", "db_path", default=str(database.DEFAULT_DB_PATH), show_default=True,
              help="Path to the SQLite database to write.")
def main(country, country_code, years_back, district, source, db_path):
  """Download trade data into the local database."""
  src = SOURCE_MAP[source]
  code = _resolve_country_code(country, country_code)
  port_name = DISTRICT_TO_PORT_NAME.get(district, f"District {district}")

  current_year = date.today().year
  start_year = current_year - years_back
  years = list(range(start_year, current_year + 1))
  
  click.echo(
    f"Ingesting {source} data for {country} (code {code}) through "
    f"{port_name} [{district}]"
  )
  click.echo(f"Years: {years[0]}..{years[-1]} ({len(years)} calendar years)\n")

  total_saved = 0
  for year in years:
    for direction, fetch in (
      (TradeDirection.IMPORT, src.fetch_imports),
      (TradeDirection.EXPORT, src.fetch_exports),
    ):
      label = direction.value
      try:
        records = fetch(year, country_code=code)
      except Exception as e: # network / APII / parse error per year
        click.echo(f"   {year} {label:7s}   ERROR: {e}")
        continue

      # Keep the stored port label in sync with the requested district,
      # even though the Census client ccurrently queries NOLA by config
      for r in records:
        r.port_code = district
        r.port_name = port_name
      
      saved = database.save_records(records, db_path=db_path)
      total_saved += saved
      click.echo(f"   {year} {label:7s}   {saved:6d} records")
  
  click.echo(f"\nDone. Wrote {total_saved} records to {db_path}.")
  click.echo("Commit this file so the deployed dashboard can read it:")
  click.echo(f"   git add {db_path}")


if __name__ == "__main__":
  main()
  