# NOLA Trade Tracker

Analyze imports and exports flowing through the Port of New Orleans using public trade data.

## Data Sources

- **US Census Bureau** (primary) -> Port-level, commodity-level trade data with country, value, and weight breakdowns.
- **UN Comtrade** -> National-level international trade data for cross-referencing.
- **Port NOLA** -> Supplementary cargo statistics from the port's public reports.

## Setup

1. Install dependcies:

```bash
pip install -r requirements.txt
```

2. Get your API keys:

- **Census Bureau**: Free at https://api.census.gov/data/key_signup.html
- **UN Comtrade**: Free at https://comtradeplus.un.org

3. Configure your keys:

- Copy the parameter labels from `.env.example`.
- Add them (and your API keys) to your local `.env` at the root of this repo.

## Usage

### CLI

```bash
# View import summary for 2017
python cli.py imports --year 2017 --top-countries 10 --top-categories 5

# Filter exports to a specific country
python cli.py exports --year 2017 --country Israel --category weapons

# Full trade summary
python cli.py summary --year 2017

#Export filtered data to CSV
python cli.py exports --year 2017 --country Israel --export-csv israel_exports.csv
```

Available categories: `food`, `chemicals`, `health`, `textiles`, `metals`, `machinery`, `electronics`, `vehicles`, `weapons`, `energy`, `wood_paper`, `plastics`, `other`

### Dashboard

```bash
streamlit run dashboard.py
```

(May need to use `py -m streamlit run dashboard.py`.)

Opens an interactive browser dashboard with:

- Filters for direction, year, month, country, and product category.
- Bar charts for trade by category and top trading partners.
- Line chart of trade over time.
- Treemap showing trade composition.
- Import/export split pie chart.
- Downloadable filtered data as CSV.

## Product Categories

<!---
TODO: I think this needs to be updated.
-->

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
|  |—config.py         # Environment variables and API settings.
|  |—models.py         # Data Classes (TradeRecord, TradeQuery, etc.)
|  |—categories.py     # HS code -> product category mapping.
|  |—query.py          # Filtering and aggregation
|  |—sources/
|      |—census.py     # US Census Bureau API client
|      |—comtrade.py   # UN Comtrade API client
|      |—port_nola.py  # Port NOLA website parser
|—cli.py               # Command-line interface
|—dashboard.py         # Streamlit dashboard
|—requirements.txt
|—.env.example
```
