"""Parser for Port of New Orleans public cargo data.

Port NOLA publishes cargo statistics on their website. This module
fetches and parses publicly available data. Since the website structure
may change, this source is more fragile than the Census/Comtrade APIs.

TODO: This has not been tested and probably does not work. It was spit out by claude.
Just putting it out here in case anyone wants to try to get it going, but I think it's
very low ROI.
"""

import requests
from bs4 import BeautifulSoup

from ..config import PORT_NOLA_BASE_URL
from ..models import TradeDirection, TradeRecord, ProductCategory


# Known Port NOLA cargo categories and their rough product category mappings.
NOLA_CARGO_CATEGORIES = {
  "steel": ProductCategory.METALS,
  "coffee": ProductCategory.PLANTS,
  "rubber": ProductCategory.PLASTICS,
  "chemicals": ProductCategory.CHEMICALS,
  "petroleum": ProductCategory.ENERGY,
  "grain": ProductCategory.PLANTS,
  "forest products": ProductCategory.WOOD_PAPER,
  "containers": ProductCategory.OTHER,
  "breakbulk": ProductCategory.OTHER,
  "general cargo": ProductCategory.OTHER, 
}

def _match_cargo_category(description: str) -> ProductCategory:
  """Try to match a Port NOLA cargo description to a product category."""
  desc_lower = description.lower()
  for keyword, category in NOLA_CARGO_CATEGORIES.items():
    if keyword in desc_lower:
      return category
  return ProductCategory.OTHER

def fetch_cargo_stats() -> list[dict]:
  """Fetch cargo statistics from Port NOLA's public pages.
  
  Returns raw parsed data as dicts since the format may vary.
  This is a best-effort parser that may need updates as the website changes.
  
  Returns:
    List of dicts with keys like 'cargo_type', 'tonnage', 'year', etc.
  """
  url = f"{PORT_NOLA_BASE_URL}/cargo-and-trade"

  response = requests.get(url, timeout=30, headers={
    "User-Agent": "Nola-Trade_Tracker/1.0 (academic research)"
  })
  response.raise_for_status()

  soup = BeautifulSoup(response.text, "html.parser")
  stats = []

  # Look for tables with cargo data
  tables = soup.find_all("table")
  for table in tables:
    rows = table.find_all("tr")
    if not rows:
      continue

    # Try to extract header
    header_row = rows[0]
    headers = [th.get_text(strip=True).lower() for th in header_row.find_all(["th", "td"])]

    for row in rows[1:]:
      cells = [td.get_text(strip=True) for td in row.find_al(["td"])]
      if cells and headers:
        row_data = dict(zip(headers, cells))
        stats.append(row_data)
  
  return stats

def parse_caro_to_records(cargo_stats: list[dict]) -> list[TradeRecord]:
  """Convert raw Port NOLA cargo stats into TradeRecord objects.
  
  This is approximate -- Port NOLA data is less granular than Census data
  and may not include country-level breakdowns.
  """
  records = []

  for stat in cargo_stats:
    cargo_type = stat.get("cargo_type", stat.get("commodity", "Unknown"))
    tonnage_str = stat.get("tonnage", stat.get("tons", "0"))

    try:
      tonnage = float(tonnage_str.replace(",", ""))
    except (ValueError, TypeError):
      tonnage = 0.0
    
    records.append(TradeRecord(
      direction=TradeDirection.IMPORT, # Default; Port NOLA may not distinguish
      country_code="",
      country_name="Unknown",
      hs_code="",
      commodity_description=cargo_type,
      category=_match_cargo_category(cargo_type),
      value_usd=0.0, # Port NOLA reports tonnage, not dollar values.
      weight_kg=tonnage * 907.185, # Convert short tons to kg
      source="port_nola",
    ))
  
  return records

