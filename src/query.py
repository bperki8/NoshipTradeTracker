"""Query and filtering layer for trade data.

Provides functions to filter, aggregate, and summarize trade records
from any data source into useful views.
"""

from collections import defaultdict

import pandas as pd

from .models import TradeRecord, TradeQuery, TradeSummary, TradeDirection, ProductCategory


def filter_records(records: list[TradeRecord], query: TradeQuery) -> list[TradeRecord]:
  """Filter a list of trade records based on query parameters."""
  filtered = records

  if query.direction:
    filtered = [r for r in filtered if r.direction == query.direction]
  
  if query.country_code:
    code = query.country_code.upper()
    filtered = [r for r in filtered if r.country_code.upper() == code]
  
  if query.country_name:
    name = query.country_name.lower()
    filtered = [r for r in filtered if name in r.country_name.lower()]
  
  if query.categories:
    filtered = [r for r in filtered if r.type.category in query.categories]
  
  if query.weaponizable != None:
    filtered = [r for r in filtered if r.type.potential_to_weaponize == query.weaponizable]
  
  if query.hs_code_prefix:
    prefix = query.hs_code_prefix
    filtered = [r for r in filtered if r.hs_code.startswith(prefix)]
  
  if query.year_start:
    filtered = [r for r in filtered if r.year >= query.year_start]
  
  if query.year_end:
    filtered = [r for r in filtered if r.year <= query.year_end]
  
  if query.month:
    filtered = [r for r in filtered if r.month == query.month]
  
  if query.min_value_usd:
    filtered = [r for r in filtered if r.value_usd >= query.min_value_usd]
  
  return filtered


def summarize(records: list[TradeRecord]) -> TradeSummary:
  """Aggregate trade records into a summary with breakdowns."""
  if not records:
    return TradeSummary(total_value_usd=0.0, record_count=0)
  
  total_value = sum(r.value_usd for r in records)

  by_category: dict[str, float] = defaultdict(float)
  by_weaponizable: dict[str, float] = defaultdict(float)
  by_country: dict[str, float] = defaultdict(float)
  by_period: dict[str, float] = defaultdict(float)
  by_direction: dict[str, float] = defaultdict(float)

  for r in records:
    by_category[r.type.category.value] += r.value_usd
    by_weaponizable[r.type.potential_to_weaponize] += r.value_usd
    by_country[r.country_name or r.country_code] += r.value_usd
    by_period[r.period] += r.value_usd
    by_direction[r.direction.value] += r.value_usd
  
  return TradeSummary(
    total_value_usd=total_value,
    record_count=len(records),
    by_category=dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True)),
    by_weaponizable=dict(sorted(by_weaponizable.items(), key=lambda x: x[1], reverse=True)),
    by_country=dict(sorted(by_country.items(), key=lambda x: x[1], reverse=True)),
    by_period=dict(sorted(by_period.items())),
    by_direction=dict(by_direction),
  )


def to_dataframe(records: list[TradeRecord]) -> pd.DataFrame:
  """Convert trade records to a pandas DataFrame for analysis."""
  if not records:
    return pd.DataFrame()
  
  rows = []
  for r in records:
    rows.append({
      "direction": r.direction.value,
      "country_code": r.country_code,
      "country_name": r.country_name,
      "hs_code": r.hs_code,
      "commodity": r.commodity_description,
      "category": r.type.category.value,
      "is_weaponizable": r.type.potential_to_weaponize,
      "value_usd": r.value_usd,
      "weight_kg": r.weight_kg,
      "year": r.year,
      "month": r.month,
      "period": r.period,
      "port": r.port_name,
      "source": r.source,
    })

  return pd.DataFrame(rows)


def top_countries(records: list[TradeRecord], n: int = 10) -> list[tuple[str, float]]:
  """Returns the top N countries by trade value."""
  summary = summarize(records)
  return list(summary.by_country.items())[:n]


def top_categories(records: list[TradeRecord], n: int = 10) -> list[tuple[str, float]]:
  """Return the top N product categories by trade value."""
  summary = summarize(records)
  return list(summary.by_category.items())[:n]