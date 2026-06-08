"""Client for the UN Comtrade API.

Docs: 
  - https://comtradedeveloper.un.org/product#product=free
  - https://comtradedeveloper.un.org/api-details#api=preview-v1&operation=65ee390ccf5b6fd0ea10bfed

Comtrade provides a global perspective -- useful for cross-referencing
Census data or seeing what the trading partner reports. The free tier
allows ~100 requests per hour.

TODO: This source has not been tested. It's not really necessary, because the USCB data is
pretty thorough, but just putting it out here in case anyone is ineterested in getting it
to work as a comparison to the USCB data.
"""

import requests

from ..config import COMTRADE_BASE_URL, require_comtrade_key
from ..models import TradeDirection, TradeRecord
from ..categories import classify_hs_code

# Us reporter code in Comtrade
US_REPORTER_CODE = "842"


def _parse_records(data: list[dict], direction: TradeDirection) -> list[TradeRecord]:
  """Parse Comtrade API response into TradeRecord objects."""
  records = []

  for item in data:
    hs_code = str(item.get("cmdCode", ""))
    if not hs_code or hs_code == "TOTAL":
      continue

    value_usd = float(item.get("primaryValue", 0) or 0)
    weight_kg = item.get("netWgt")
    if weight_kg is not None:
      weight_kg = float(weight_kg)
    
    period_str = str(item.get("period", ""))
    year = int(period_str[:4]) if len(period_str) >= 4 else 0
    month = int(period_str[4:6]) if len(period_str) >= 6 else 0

    records.append(TradeRecord(
      direction=direction,
      country_code=str(item.get("partnerCode", "")),
      country_name=item.get("partnerDesc", ""),
      hs_code=hs_code,
      commodity_description=item.get("cmdDesc", ""),
      category=classify_hs_code(hs_code),
      value_usd=value_usd,
      weight_kg=weight_kg,
      quantity=float(item["qty"]) if item.get("qty") else None,
      qunatity_unit=item.get("qtyUnitAbbr"),
      year=year,
      month=month,
      port_code="",
      port_name="United States (national)",
      source="comtrade",
    ))
  
  return records


def fetch_trade_data(
    direction: TradeDirection,
    year: int,
    month: int | None = None,
    partner_code: str | None = None,
    hs_code: str | None = None,
) -> list[TradeRecord]:
  """Fetch trade data from the UN Comtrade API.
  
  Note: Comtrade data is at the national level (not port-specific),
  so it complements Census port-level data with a global view.
  
  Args:
    direction: Import or export.
    year: The year to query.
    month: Optional month (1-12).
    partner_code: Optional Comtrade partner country code.
    hs_code: Optional HS code prefix to filter by.
  
  Returns:
    List of TradeRecord objects.
  """
  api_key = require_comtrade_key()

  flow_code = "M" if direction == TradeDirection.IMPORT else "X"
  period = f"{year}{month:02d}" if month else str(year)

  params = {
    "reporterCode": US_REPORTER_CODE,
    "flowCode": flow_code,
    "period": period,
    "subscription-key": api_key,
  }

  if partner_code:
    params["partnerCode"] = partner_code
  
  if hs_code:
    params["cmdCode"] = hs_code
  
  response = requests.get(COMTRADE_BASE_URL, params=params, timeout=30)
  response.raise_for_status()
  
  result = response.json()
  data = result.get("data", [])
  return _parse_records(data, direction)


def fetch_import(year: int, **kwargs) -> list[TradeRecord]:
  """Convenience wrapper for fetching imports."""
  return fetch_trade_data(TradeDirection.IMPORT, year, **kwargs)


def fetch_exports(year: int, **kwargs) -> list[TradeRecord]:
  """Convenience wrapper for fetching exports."""
  return fetch_trade_data(TradeDirection.EXPORT, year, **kwargs)
