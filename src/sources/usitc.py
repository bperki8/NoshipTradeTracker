"""Client for the USITC Dataweb API.

Docs: https://www.usitc.gov/applications/datawebapi/dataweb_query_api.html
Swagger: https://datawebws.usitc.gov/dataweb/swagger-ui/index.html

USITC Dataweb provides U.S. import/export statistics filtered by HTS
commodity codes and custom districts. This lets us query trade flowing
through the New Orleans customs district specifically, giving a scond
port-level data source alongisde the Census Bureau.
"""

import requests

from ..config import USITC_BASE_URL, NOLA_DISTRICT_CODE, require_usitc_key
from ..models import TradeDirection, TradeRecord
from ..categories import classify_hs_code

# USITC uses the same customs district codes as Census
NOLA_DISTRICT = NOLA_DISTRICT_CODE


def _build_report_body(
    direction: TradeDirection,
    year: int,
    month: int | None = None,
    hs_code: str | None = None,
) -> dict:
  """Build the JSON request body for the runReport endpoint."""
  trade_type = "Import" if direction == TradeDirection.IMPORT else "Export"

  if month:
    timeframes = {
      "selectedTab": "monthRange",
      "monthRange": {
        "startMonth": month,
        "startYear": year,
        "endMonth": month,
        "endYear": year,
      },
    }
  else:
    timeframes = {
      "selectedTab": "fullYears",
      "fullYears": [year],
    }
  
  body = {
    "reportOptions": {
      "tradeType" : trade_type,
      "classificationSystem": "HTS",
      "timeframes": timeframes,
    },
    "searchOptions": {
      "MiscGroup": {
        "districts": {
          "selected": [NOLA_DISTRICT],
        },
      },
    },
  }

  if hs_code:
    body["searchOptions"]["commodities"] = {
      "selected": [hs_code],
    }
  
  return body


def _parse_records(data: list[dict], direction: TradeDirection) -> list[TradeRecord]:
  """Parse USITC Dataweb API response into TradeRecord objects.0

  The USITC Dataweb API documentation is sparse about the exact response schema from runReport. The
  _parse_records function handles several likely field name patterns (e.g., htsNumber/commodityCode,
  customsValue/value), but we may need to adjust the field mappings once we make our first real API call and see the
  actual response shape."""
  records = []

  for item in data:
    hs_code = str(item.get("htsNumber", item.get("commodityCode", "")))
    if not hs_code or hs_code in ("TOTAL", "Total"):
      continue

    try:
      value_usd = float(item.get("customsValue", item.get("value", 0)) or 0)
    except (ValueError, TypeError):
      value_usd = 0.0
    
    weight_raw = item.get("quantity", item.get("weight"))
    try:
      weight_kg = float(weight_raw) if weight_raw else None
    except (ValueError, TypeError):
      weight_kg = None
    
    country_code = str(item.get("countryCode", item.get("parnterCode", "")))
    country_name = item.get("countryDescription", item.get("partnerDescription", ""))

    year = int(item.get("year", 0) or 0)
    month = int(item.get("month", 0) or 0)

    records.append(TradeRecord(
      direction=direction,
      country_code=country_code,
      country_name=country_name,
      hs_code=hs_code,
      commodity_description=item.get("commodityDescription", item.get("htsDescription", "")),
      category=classify_hs_code(hs_code),
      value_usd=value_usd,
      weight_kg=weight_kg,
      year=year,
      month=month,
      source="usitc",
    ))
  
  return records


def fetch_trade_data(
    direction: TradeDirection,
    year: int,
    month: int | None = None,
    hs_code: str | None = None,
) -> list[TradeRecord]:
  """Fetch trade data from the USITC Dataweb API.

  Args:
    direction: Import or export.
    year: The year to query.
    month: Optional month (1-12). If None, fetches the full year.
    hs_code: Optional HTS code prefix to filter by.
  
  Returns:
    List of TradeRecord objects.
  """
  api_key = require_usitc_key()
  url = f"{USITC_BASE_URL}/api/v2/report2/runReport"

  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json; charset=utf-8",
  }

  body = _build_report_body(direction, year, month=month, hs_code=hs_code)

  response = requests.post(url, json=body, headers=headers, timeout=60)
  response.raise_for_status()

  result = response.json()
  data = result.get("data", result.get("reportData", []))

  if isinstance(data, dict):
    data = data.get("rows", data.get("items", []))
  
  return _parse_records(data, direction)


def fetch_imports(year: int, **kwargs) -> list[TradeRecord]:
  """Convenience wrapper for fetching imports."""
  return fetch_trade_data(TradeDirection.IMPORT, year, **kwargs)


def fetch_exports(year: int, **kwargs) -> list[TradeRecord]:
  """Convenience wrapper for fetching exports."""
  return fetch_trade_data(TradeDirection.EXPORT, year, **kwargs)
