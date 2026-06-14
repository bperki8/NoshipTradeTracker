# NOSHIP Trade Tracker

Analyze imports and exports flowing through the Port of New Orleans using public trade data.

The project has two halves:

1.  **Ingest (runs locally with your API keys):** `ingest.py` downloads trade
    data for a country and writes it into a committed SQLite database
    (`data/trade.db`).
2.  **Dashboard (deploys publicly, no keys):** `dashboard.py` reads only from
    that committed database. It never calls a trade API and never loads a token,
    so it is safe to host on Streamlit Community Cloud.

## Data Sources

- **US Census Bureau** (primary) -> Port-level, commodity-level trade data with country, value, and weight breakdowns.

## Setup (local, for ingest only)

1.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2.  Get a free Census Bureau API key: https://api.census.gov/data/key_signup.html

3.  Configure your key:
    ```bash
    cp .env.example .env
    # Edit .env and add CENSUS_API_KEY
    ```

## Step 1 - Build the database locally

Run the ingest script once on your macchine. By default it pulls **Israel**,
the **last 13 years**, through the **Port of New Orleans**, from **Census**:

```bash
python ingest.py
```

Useful options:

```bash
# A different country / span
python ingest.py --country Sudan --years-back 7

# A country not in th ebuilt-in name->code map (pass the Census Schedule C code)
python ingest.py --country "South Korea" --country-code 5800
```

The script is safe to re-run: rows are replaced by key, so you can ingest
several countries into the **same** database by running it once per country.
The dashboard's filters populate automatically from whatever is in the DB.

Then ccommit the generated database:

```bash
git add data/trade.db
git commit -m "Add trade data for Israel"
```

## Step 2 - Run the dashboard

Locally:

```bash
streamlit run dashboard.py
```

(May need to use `py -m streamlit run dashboard.py`.)

The dashboard offers filters for country, port, source, direction, year range,
and product category; bar charts for trade by category and top commodities (or
top trading partners once multiple countries are ingested); a line chart over
time; a treemap; an import/export split; a weaponizable/not split; and a CSV
download.

## Step 3 - Deploy to Streamlit Community Cloud

1.  Push this repository to GitHub (including the committed `data/trade.db`).
2.  On https://share.streamlit.io, create a new app from your repo.
3.  Set the **main files path** to `nola-trade-tracker/dashboard.py`.
4.  Deploy. No secrets are required, because the dashboard reads only the committed
    database, so your Census key never leaves your machine.

To refresh or expand the public data later, re-run `ingest.py` locally and
commit the updated `data/trade.db`; Streamlit redeploys on push.

## Product Categories

TODO: I think this needs to be updated, because some of the categorizations have changed since original writing.

Products are classified using the Harmonized System (HS) code chapters:

| Category                                 | HS Chapters  |
| ---------------------------------------- | ------------ |
| Animal Exploitation & Food & Agriculture | 01-24        |
| Energy & Petroleum                       | 27           |
| Chemicals                                | 28-29, 31-38 |
| Health & Pharmaceuticals                 | 30, 33, 90   |
| Plastics & Rubber                        | 39-40        |
| Textiles & Apparel                       | 41-43, 50-67 |
| Wood & Paper                             | 44-49        |
| Metals & Minerals                        | 25-26, 68-83 |
| Machinery & Equipment                    | 84           |
| Electronics                              | 85           |
| Vehicles & Transport                     | 86-89        |
| Weapons & Defense                        | 93           |

## Project Structure

```
NolaTradeTracker/
|—src/
|  |—config.py         # Environment variables and API settings (ingest only).
|  |—models.py         # Data Classes (TradeRecord, TradeQuery, etc.)
|  |—categories.py     # HS code -> product category mapping.
|  |—query.py          # Filtering and aggregation
|  |-database.py       # SQLite store: save (ingest) + load (dashboard)
|  |—sources/
|      |—census.py     # US Census Bureau API client
|      |—comtrade.py   # UN Comtrade API client
|      |—port_nola.py  # Port NOLA website parser
|
|-data/
|  |-trade.db          # Committed SQLite database (created by ingest.py)
|
|-ingest.py            # Local one-time data download + database
|—cli.py               # Command-line interface (live API)
|—dashboard.py         # Streamlit dashboard (reads the committed database)
|—requirements.txt
|—.env.example
```
