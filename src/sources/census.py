"""Client for the US Census Bureau of International Trade API.

Docs: https://www.census.gov/data/developers/data-sets/international-trade.html
      https://api.census.gov/data/timeseries/intltrade/imports/porths
      https://api.census.gov/data/timeseries/intltrade/exports/porths
      https://api.census.gov/data/timeseries/intltrade/imports.html
      https://api.census.gov/data/timeseries/intltrade/exports.html

This is the primary data source -- it provides port-level, commodity-level
trade data with country, value, and weight breakdowns.
"""

import requests
import pandas as pd

from ..config import CENSUS_BASE_URL, NOLA_CENSUS_PORT_CODE, require_census_key
from ..models import TradeDirection, TradeRecord, ProductCategory
from ..categories import classify_hs_code


def _build_url(direction: TradeDirection) -> str:
  if direction == TradeDirection.IMPORT:
    return f"{CENSUS_BASE_URL}/imports/porths"
  return f"{CENSUS_BASE_URL}/exports/porths"


def _parse_records(data: list[list[str]], direction: TradeDirection) -> list[TradeRecord]:
  """Parse Census Api JSON response into TradeRecord objects.
  
  The Census API returns data as a list of lsits where the first element
  is the header row.
  """
  if not data or len(data) < 2:
    return []
  
  headers = data[0]
  records = []

  for row in data [1:]:
    row_dict = dict(zip(headers, row))

    country_name = row_dict.get("CTY_NAME", "")
    if country_name == "TOTAL FOR ALL COUNTRIES":
      continue

    hs_code = row_dict.get("I_COMMODITY", row_dict.get("E_COMMODITY", ""))

    value_str = row_dict.get("GEN_VAL_MO", row_dict.get("ALL_VAL_MO", row_dict.get("GEN_VAL_YR", row_dict.get("ALL_VAL_YR", "0"))))
    try:
      value_usd = float(value_str) if value_str else 0.0
    except (ValueError, TypeError):
      value_usd = 0.0
    
    # TODO: Need to figure out the difference between the ones used here and CNT_WGT_MO/CNT_WGT_YR and AIR_WGT_MO/AIR_WGT_YR.
    weight_str = row_dict.get("VES_WGT_MO", row_dict.get("VES_WGT_YR", ""))
    try:
      weight_kg = float(weight_str) if weight_str else None
    except (ValueError, TypeError):
      weight_kg = None
    
    year, month = 0, 0
    year = int(row_dict.get("YEAR", ""))
    if not "GEN_VAL_YR" in headers and not "ALL_VAL_YR" in headers:
      month = int(row_dict.get("MONTH", ""))
    
    commodity_description = row_dict.get("I_COMMODITY_LDESC", row_dict.get("E_COMMODITY_LDESC", ""))
    if commodity_description in ["TOTAL EXPORTS FOR ALL COMMODITIES", "TOTAL IMPORTS FOR ALL COMMODITIES"]:
      continue

    records.append(TradeRecord(
      direction=direction,
      country_code=row_dict.get("CTY_CODE", ""),
      country_name=country_name,
      hs_code=hs_code,
      commodity_description=commodity_description,
      type=classify_hs_code(hs_code),
      value_usd=value_usd,
      weight_kg=weight_kg,
      year=year,
      month=month,
      source="census",
    ))
  
  return records


def fetch_trade_data(
    direction: TradeDirection,
    year: int,
    month: int | None = None,
    country_code: str | None = None,
    hs_chapter: str | None = None,
    hs_level: str | None = None,
) -> list[TradeRecord]:
  """Fetch trade data from the Census Bureau Api.
  
  Args:
    direction: Import or export.
    year: The year to query.
    month: Optional month (1-12). If None, fetches all months.
    country_code: Optional country code to filter by.
    hs_chapter: Optional 2-digit HS chapter to filter by.
  
  Returns:
    List of TradeRecord objects.
  """
  api_key = require_census_key()
  url = _build_url(direction)

  # Build query parameters.
  # Using:
  # exports - https://api.census.gov/data/timeseries/intltrade/exports/porths/variables.html
  # imports - https://api.census.gov/data/timeseries/intltrade/imports/porths/variables.html
  #
  # What do we actually want for the get_vars? Looks like exports and imports are different.
  # exports:
  #   ALL_VAL_YR: 15-digit Year-to-Date Total Value
  #   ALL_VAL_MO: 15-digit Total Value
  #   COMM_LVL: 4-character aggregation levels for commodity code. HS2=2-digit HS totals. HS4=4-digit HS totals. HS6=6-digit HS totals.
  #   E_COMMODITY: 	2-, 4-, or 6-digit Export Harmonized System Code
  #   E_COMMODITY_LDESC: 150-character Export Harmonized Code Description
  # imports:
  #   GEN_VAL_YR: 15-digit Year-to-Date General Imports, Total Value
  #   GEN_VAL_MO: 15-digit General Imports, Total Value
  #   COMM_LVL: 4-character aggregation levels for commodity code. HS2=2-digit HS totals. HS4=4-digit HS totals. HS6=6-digit HS totals.
  #   I_COMMODITY: 2-, 4-, 6-, or 10-character Import Harmonized Code
  #   I_COMMODITY_LDESC: 150-character Import Harmonized Code Description
  if direction == TradeDirection.IMPORT:
    get_vars = "CTY_CODE,CTY_NAME,PORT,PORT_NAME,I_COMMODITY,I_COMMODITY_LDESC"
  else:
    get_vars = "CTY_CODE,CTY_NAME,PORT,PORT_NAME,E_COMMODITY,E_COMMODITY_LDESC"
  
  params = {
    "get": get_vars,
    "key": api_key,
    "PORT": NOLA_CENSUS_PORT_CODE,
  }

  if year and month:
    if direction == TradeDirection.IMPORT:
      params["get"] += ",GEN_VAL_MO"
    else:
      params["get"] += ",ALL_VAL_MO"
    
    params["YEAR"] = f"{year}"
    params["MONTH"] = f"{month:02d}"
    
  elif year:
    # If only a year is provided, use the 12th month and get the Year-to-Date value
    # which would thus be the full year.
    # TODO: This is probably going to break fo rhte current year, because it's not 12th month yet, but maybe not.
    if direction == TradeDirection.IMPORT:
      params["get"] += ",GEN_VAL_YR"
    else:
      params["get"] += ",ALL_VAL_YR"
    
    params["YEAR"] = f"{year}"
    params["MONTH"] = "12"
  
  if country_code:
    # https://www.census.gov/foreign-trade/schedules/c/countryname.html
    # Israel: 5081
    # Gaza Strip administered by Israel: 5082
    # West Bank administered by Israel: 5083
    params["CTY_CODE"] = country_code
  
  if hs_level:
    params["COMM_LVL"] = f"{hs_level}"
  if hs_chapter:
    if direction == TradeDirection.IMPORT:
      params["I_COMMODITY"] = f"{hs_chapter}*"
    else:
      params["E_COMMODITY"] = f"{hs_chapter}*"
  
  response = requests.get(url, params=params, timeout=30)
  response.raise_for_status()

  data = response.json()
  return _parse_records(data, direction)

def fetch_imports(year: int, **kwargs) -> list[TradeRecord]:
  """Convenience wrapper for fetching imports."""
  return fetch_trade_data(TradeDirection.IMPORT, year, **kwargs)


def fetch_exports(year: int, **kwargs) -> list[TradeRecord]:
  """Convenience wrapper for fetching exports."""
  return fetch_trade_data(TradeDirection.EXPORT, year, **kwargs)
