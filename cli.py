"""CLIT tool for querying Port of New Orleans trade data.

Usage:
  python cli.py imports --year 2017 --country Israel --category weapons
  python cli.py exports --year 2017 --top-countries 10
  python cli.py summary --year 2017

Available categories: `food`, `chemicals`, `health`, `textiles`, `metals`, `machinery`, `electronics`, `vehicles`, `weapons`, `energy`, `wood_paper`, `plastics`, `other`
"""
import click
from src.models import TradeDirection, TradeQuery, ProductCategory
from src.sources import census, usitc
from src.query import filter_records, summarize, top_countries, top_categories, to_dataframe


SOURCE_MAP = {
  "census": census,
  "usitc": usitc,
}
SOURCE_CHOICES = list(SOURCE_MAP.keys())


CATEGORY_CHOICES = [c.name.lower() for c in ProductCategory]


def _format_usd(value: float) -> str:
  if value >= 1_000_000_000:
    return f"${value / 1_000_000_000:.2f}B"
  if value >= 1_000_000:
    return f"${value / 1_000_000:.2f}M"
  if value >= 1_000:
    return f"${value / 1_000:.1f}K"
  return f"${value:.0f}"


def _resolve_categories(category_names: tuple[str, ...]) -> list[ProductCategory]:
  if not category_names:
    return []
  return [ProductCategory[name.upper()] for name in category_names]


@click.group()
def cli():
  """NOSHIP Trade Tracker - Query Port of New Orleans trade data."""
  pass


@cli.command()
@click.option("--year", required=True, type=int, help="Year to query.")
@click.option("--month", type=int, help="Month to query (1-12).")
@click.option("--country", help="Filter by country name (partial match).")
@click.option("--country-code", help="Filter by country code.")
@click.option("--category", multiple=True, type=click.Choice(CATEGORY_CHOICES, case_sensitive=False),
              help="Filter by product category. Can specify multiple. Available categories: `food`, `chemicals`, `health`, `textiles`, `metals`, `machinery`, `electronics`, `vehicles`, `weapons`, `energy`, `wood_paper`, `plastics`, `other`.")
@click.option("--top-countries", "top_n_countries", type=int, help="Show top N countries.")
@click.option("--top-categories", "top_n_categories", type=int, help="Show top N categories.")
@click.option("--export-csv", type=click.Path(), help="Export results to CSV.")
@click.option("--source", type=click.Choice(SOURCE_CHOICES, case_sensitive=False),
              default="census", help="Data source (default: census).")
def imports(year, month, country, country_code, category, top_n_countries, top_n_categories, export_csv, source):
  """Query import data through Port of New Orleans."""
  src = SOURCE_MAP[source]
  click.echo(f"Fetching {year} import data for Port of New Orleans from {source}...")

  records = src.fetch_imports(year, month=month)
  click.echo(f"Retrieved {len(records)} records.")

  query = TradeQuery(
    direction=TradeDirection.IMPORT,
    country_name=country,
    country_code=country_code,
    categories=_resolve_categories(category),
  )
  filtered = filter_records(records, query)
  click.echo(f"After filtering: {len(filtered)} records.")

  _display_results(filtered, top_n_countries, top_n_categories, export_csv)


@cli.command()
@click.option("--year", required=True, type=int, help="Year to query.")
@click.option("--month", type=int, help="Month to query (1-12).")
@click.option("--country", help="Filter by country name (partial match).")
@click.option("--country-code", help="Filter by country code.")
@click.option("--category", multiple=True, type=click.Choice(CATEGORY_CHOICES, case_sensitive=False),
              help="Filter by product category. Can specify multiple. Available categories: `food`, `chemicals`, `health`, `textiles`, `metals`, `machinery`, `electronics`, `vehicles`, `weapons`, `energy`, `wood_paper`, `plastics`, `other`.")
@click.option("--top-countries", "top_n_countries", type=int, help="Show top N countries.")
@click.option("--top-categories", "top_n_categories", type=int, help="Show top N categories.")
@click.option("--export-csv", type=click.Path(), help="Export results to CSV.")
@click.option("--source", type=click.Choice(SOURCE_CHOICES, case_sensitive=False),
              default="census", help="Data source (default: census).")
def exports(year, month, country, country_code, category, top_n_countries, top_n_categories, export_csv, source):
  """Query export data through Port of New Orleans."""
  src = SOURCE_MAP[source]
  click.echo(f"Fetching {year} export data for Port of New Orleans from {source}...")

  records = src.fetch_exports(year, month=month)
  click.echo(f"Retrieved {len(records)} records.")

  query = TradeQuery(
    direction=TradeDirection.EXPORT,
    country_name=country,
    country_code=country_code,
    categories=_resolve_categories(category),
  )
  filtered = filter_records(records, query)
  click.echo(f"After filtering: {len(filtered)} records.")

  _display_results(filtered, top_n_countries, top_n_categories, export_csv)


@cli.command()
@click.option("--year", required=True, type=int, help="Year to query.")
@click.option("--month", type=int, help="Month to query (1-12).")
@click.option("--source", type=click.Choice(SOURCE_CHOICES, case_sensitive=False),
              default="census", help="Data source (default: census).")
def summary(year, month, source):
  """Show a summary of all the trade through the Port of New Orleans."""
  src = SOURCE_MAP[source]
  click.echo(f"Fetching {year} trade data for Port of New Orleans from {source}...")

  import_records = src.fetch_imports(year, month=month)
  export_records = src.fetch_exports(year, month=month)
  all_records = import_records + export_records
  
  click.echo(f"Retrieved {len(all_records)} total records "
             f"({len(import_records)} imports, {len(export_records)} exports).\n")
  
  s = summarize(all_records)

  click.echo("=== Trade Summary ===")
  click.echo(f"Total Value: {_format_usd(s.tool_value_usd)}")
  click.echo(f"Records: {s.record_count}\n")

  click.echo("--- By Direction ---")
  for direction, value in s.by_direction.items():
    click.echo(f" {direction.capitalize():10s} {_format_usd(value):>12s}")
  
  click.echo("\n--- Top Categories ---")
  for cat, value in list(s.by_category.items())[:10]:
    click.echo(f" {cat:30s} {_format_usd(value):>12s}")
  
  click.echo("\n--- Top Countries ---")
  for country_name, value in list(s.by_country.items())[:10]:
    click.echo(f" {country_name:30s} {_format_usd(value):>12s}")


def _display_results(records, top_n_countries, top_n_categories, export_csv):
  """Display filtered results."""
  if not records:
    click.echo(f"No records found matching your criteria.")
    return
  
  s = summarize(records)
  click.echo(f"\nTotal Value: {_format_usd(s.total_value_usd)}")

  if top_n_countries:
    click.echo(f"\n--- Top {top_n_countries} Countries ---")
    for name, value in top_countries(records, top_n_countries):
      click.echo(f"   {name:30s} {_format_usd(value):>12s}")
  
  if top_n_categories:
    click.echo(f"\n--- Top {top_n_categories} Categories ---")
    for cat, value in top_categories(records, top_n_categories):
      click.echo(f"   {cat:30s} {_format_usd(value):>12s}")
  
  if not top_n_countries and not top_n_categories:
    click.echo("\n--- By Category ---")
    for cat, value in s.by_category.items():
      click.echo(f"   {cat:30s} {_format_usd(value):>12s}")
    click.echo("\n\n--- By Weaponizable ---")
    for weap, value in s.by_weaponizable.items():
      click.echo(f"   {weap} {_format_usd(value):>12s}")
  
  if export_csv:
    df = to_dataframe(records)
    df.to_csv(export_csv, index=False)
    click.echo(f"\nExported {len(df)} records to {export_csv}.")


if __name__ == "__main__":
  cli()