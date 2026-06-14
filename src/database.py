"""Local SQLite store for trade records.

This module is the bridge between the one-time *ingest* step (which pulls data
from the live APIs using your private keys) and the *dashboard* (which is
deployed publicly and must never touch and API or a key).

The ingest script calls :func:`save_records` to persist data into a committed
SQLite file (``data/trade.db``). The dashboard calls :func:`load_dataframe`
to read it back. Because the schemas keeps every dimension in a real column
(source, country, district/port, ...), you can later ingest aditional
countries, ports, or sources into the *same* file and the dashboard will pick
them up automatically.
"""
from __future__ import annotations

import pandas as pd
import sqlite3

from pathlib import Path

from .models import TradeRecord
from .categories import classify_hs_code

# Default location of the committed database, resolved relative to the project
# root (one level up from this src/ package) so it works regardless of the
# current working directory (local shell, Streamlit Cloud, etc.).
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "trade.db"

TABLE_NAME = "trade_records"

# Columns persisted for each record. Several are fixed today (district/port is
# always New Orleans, source is always census) but are stored explicitly so the
# dataset can grow to multiple ports / sources / countries with a migration.
_COLUMNS = [
  "source",
  "direction",
  "country_code",
  "country_name",
  "district_code",
  "port_name",
  "hs_code",
  "commodity",
  "category",
  "is_weaponizable",
  "value_usd",
  "weight_kg",
  "year",
  "month",
]

# A row is uniquely identified by this combination. Re-ingesting the same
# country/port/year refreshes those rows (INSERT OR REPLACE) rather than
# duplicating them, so the ingest script is safe to re-run.
_PRIMARY_KEY = [
  "source",
  "direction",
  "country_code",
  "district_code",
  "hs_code",
  "year",
  "month",
]

_CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
  source        TEXT NOT NULL,
  direction     TEXT NOT NULL,
  country_code  TEXT NOT NULL,
  country_name  TEXT,
  district_code TEXT NOT NULL,
  port_name     TEXT,
  hs_code       TEXT NOT NULL,
  commodity     TEXT,
  category      TEXT,
  is_weaponizable  INTEGER,                -- store as 0/1
  value_usd     REAL,
  weight_kg     REAL,
  year          INTEGER NOT NULL,
  month         INTEGER NOT NULL,
  PRIMARY KEY ({", ".join(_PRIMARY_KEY)})
)
"""


def connect(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
  """Open a connection to the SQLite database, creating the file/dir if needed."""
  db_path = Path(db_path)
  db_path.parent.mkdir(parents=True, exist_ok=True)
  return sqlite3.connect(str(db_path))


def init_db(conn: sqlite3.Connection) -> None:
  """Create the trade_records table if it does not already exist."""
  conn.execute(_CREATE_TABLE_SQL)
  conn.commit()


def _record_to_row(record: TradeRecord) -> tuple:
  ptype = classify_hs_code(record.hs_code)
  category = ptype.category  # This is a ProductCategory enum
  
  return (
    record.source,
    record.direction.value,
    record.country_code,
    record.country_name,
    record.port_code,
    record.port_name,
    record.hs_code,
    record.commodity_description,
    category.value,
    int(ptype.potential_to_weaponize),
    record.value_usd,
    record.weight_kg,
    record.year,
    record.month,
  )


def save_records(records: list[TradeRecord], db_path: str | Path = DEFAULT_DB_PATH) -> int:
  """Persist trade records into the database, replacing matching rows.

  Returns the number of rows written. Safe to call repeatedly and across
  multiple countries/ports--existing rows with the same primary key are
  overwritten, everything else is appended.
  """
  if not records:
    return 0
  
  placeholders = ", ".join("?" for _ in _COLUMNS)
  insert_sql = (
    f"INSERT OR REPLACE INTO {TABLE_NAME} ({', '.join(_COLUMNS)}) "
    f"VALUES ({placeholders})"
  )

  conn = connect(db_path)
  try:
    init_db(conn)
    rows = [_record_to_row(r) for r in records]
    conn.executemany(insert_sql, rows)
    conn.commit()
  finally:
    conn.close()
  
  return len(records)


def load_dataframe(db_path: str | Path = DEFAULT_DB_PATH) -> pd.DataFrame:
  """Load all trade records as a DataFrame shaped like ``query.to_dataframe``.

  Adds a ``period`` column (``YYYY-MM``) and a ``port`` alias so the dashboard
  can reuse the same plotting code that worked against the live API output.
  Returns an empty DataFrame if the database file does not exist yet.
  """
  db_path = Path(db_path)
  if not db_path.exists():
    return pd.DataFrame()
  
  conn = sqlite3.connect(str(db_path))
  try:
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
  except (pd.errors.DatabaseError, sqlite3.DatabaseError):
    # Table not created yet (empty/new DB file).
    return pd.DataFrame()
  finally:
    conn.close()
  
  if df.empty:
    return df
  
  df["period"] = df["year"].astype(str) + "-" + df["month"].astype(int).map(lambda m: f"{m:02d}")
  df["port"] = df["port_name"]
  return df
