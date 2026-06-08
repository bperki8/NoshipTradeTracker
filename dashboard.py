"""Streamlit dashboard for Port of New Orleans trade data.

Run with: streamlit run dashboard.py
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.models import TradeDirection, TradeQuery, ProductCategory
from src.sources import census, usitc
from src.query import filter_records, summarize, to_dataframe
from src.categories import classify_hs_code

SOURCE_MAP = {
  "Census Bureau": census,
  "USITC DataWeb": usitc,
}

st.set_page_config(
  page_title="NOLA Trade Tracker",
  page_icon="🚢",
  layout="wide",
)

st.title("Port of New Orleans Trade Tracker")
st.markdown("Analyze imports and exports flowing through the Port of New Orleans.")


# --- Sidebar Filters ---
st.sidebar.header("Filters")

source_choice  = st.sidebar.selectbox(
  "Data Source",
  list(SOURCE_MAP.keys()),
)

direction_choice = st.sidebar.selectbox(
  "Trade Direction",
  ["Exports", "Both", "Imports"],
)

year = st.sidebar.number_input("Year", min_value=2013, max_value=2026, value=2025)

month_options = ["All Months"] + [f"{i:02d}" for i in range(1, 13)]
month_choice = st.sidebar.selectbox("Month", month_options)
month = int(month_choice) if month_choice != "All Months" else None

hs_level = st.sidebar.selectbox("HS Specificty Level", ["HS6", "HS2", "HS4", "HS10"])

country_filter = st.sidebar.text_input("Country (partial name match).", "Israel")

category_options = [c.value for c in ProductCategory]
selected_categories = st.sidebar.multiselect("Product Categories", category_options)


# --- Data Fetching ---
@st.cache_data(ttl=3600, show_spinner="Fetching trade data...")
def load_data(source_name: str, direction_str: str, yr: int, mo: int | None, hs_level: str) -> pd.DataFrame:
  src = SOURCE_MAP[source_name]
  records = []

  if direction_str in ("Both", "Imports"):
    records.extend(src.fetch_imports(yr, month=mo, hs_level=hs_level))
  if direction_str in ("Both", "Exports"):
    records.extend(src.fetch_exports(yr, month=mo, hs_level=hs_level))
  
  return to_dataframe(records)


try:
  df = load_data(source_choice, direction_choice, year, month, hs_level)
except EnvironmentError as e:
  st.error(str(e))
  st.info("Copy `.env.example` to `.env` and add you API keys to get started.")
  st.stop()
except Exception as e:
  st.error(f"Failed to fetch data: {e}")
  st.stop()

if df.empty:
  st.warning("No data returned. Try a different year or check your API key.")
  st. stop()


# --- Apply Filters ---
filtered_df = df.copy()

if country_filter:
  filtered_df = filtered_df[
    filtered_df["country_name"].str.contains(country_filter, case=False, na=False)
  ]

if selected_categories:
  filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

st.sidebar.markdown(f"**{len(filtered_df):,}** records after filtering.")


# --- Summary Metrics ---
col1, col2, col3, col4 = st.columns(4)

total_value = filtered_df["value_usd"].sum()
import_value = filtered_df[filtered_df["direction"] == "import"]["value_usd"].sum()
export_value = filtered_df[filtered_df["direction"] == "export"]["value_usd"].sum()
n_countries = filtered_df["country_name"].nunique()

col1.metric("Total Trade Value", f"${total_value / 1e6:,.1f}M")
col2.metric("Import Value", f"${import_value / 1e6:,.1f}M")
col3.metric("Export Value", f"${export_value / 1e6:,.1f}M")
col4.metric("Trading Partners", f"{n_countries}")


# --- Charts ---
st.markdown("---")

chart_col1, chart_col2 = st.columns(2)

# Trade by Category (bar chart)
with chart_col1:
  st.subheader("Trade Value by Category")
  cat_df = (
    filtered_df.groupby("category")["value_usd"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
  )
  fig_cat = px.bar(
    cat_df,
    x="value_usd",
    y="category",
    orientation="h",
    labels={"value_usd": "Value (USD)", "category": "Category"},
    color="category",
    color_discrete_sequence=px.colors.qualitative.Set3,
  )
  fig_cat.update_layout(showlegend=False, height=500)
  st.plotly_chart(fig_cat, use_container_width=True)

# Top Trading Partners (bar chart)
with chart_col2:
  st.subheader("Top 15 Trading Partners")
  country_df = (
    filtered_df.groupby("country_name")["value_usd"]
    .sum()
    .nlargest(15)
    .sort_values(ascending=True)
    .reset_index()
  )
  fig_country = px.bar(
    country_df,
    x="value_usd",
    y="country_name",
    orientation="h",
    labels={"value_usd": "Value (USD)", "country_name": "Country"},
    color="value_usd",
    color_continuous_scale="Viridis",
  )
  fig_country.update_layout(showlegend=False, height=500)
  st.plotly_chart(fig_country, use_container_width=True)


# Trade Over Time (line chart)
st.subheader("Trade Value Over Time")
if "period" in filtered_df.columns:
  time_df = (
    filtered_df.groupby(["period", "direction"])["value_usd"]
    .sum()
    .reset_index()
  )
  fig_time = px.line(
    time_df,
    x="period",
    y="value_usd",
    color="direction",
    labels={"value_usd": "Value (USD)", "period": "Period", "direction": "Direction"},
    markers=True,
  )
  fig_time.update_layout(height=400)
  st.plotly_chart(fig_time, use_container_width=True)


# Category Treemap
st.subheader("Trade Composition")
if not filtered_df.empty:
  treemap_df = (
    filtered_df.groupby(["category", "country_name"])["value_usd"]
    .sum()
    .reset_index()
  )
  # Only show top entires to keep treemap readable
  treemap_df = treemap_df.nlargest(50, "value_usd")

  fig_tree = px.treemap(
    treemap_df,
    path=["category", "country_name"],
    values="value_usd",
    color="value_usd",
    color_continuous_scale="RdYlGn",
  )
  fig_tree.update_layout(height=600)
  st.plotly_chart(fig_tree, use_container_width=True)


# Import vs Export Pie
st.subheader("Import vs. Export Split")
pie_col1, pie_col2 = st.columns(2)

with pie_col1:
  dir_df = filtered_df.groupby("direction")["value_usd"].sum().reset_index()
  fig_pie = px.pie(
    dir_df,
    values="value_usd",
    names="direction",
    color_discrete_map={"import": "#636EFA", "export": "#EF553B"},
  )
  st.plotly_chart(fig_pie, use_container_width=True)

with pie_col2:
  st.markdown("### Category Breakdown")
  cat_summary = (
    filtered_df.groupby("category")["value_usd"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
  )
  cat_summary["value_formatted"] = cat_summary["value_usd"].apply(
    lambda x: f"${x / 1e6:,.1F}M" if x >= 1e6 else f"${x / 1e3:,.1f}K"
  )
  st.dataframe(
    cat_summary[["category", "value_formatted"]].rename(
      columns={"category": "Category", "value_formatted": "Trade Value"}
    ),
    hide_index=True,
    use_container_width=True,
  )

# Weaponizable Pie
st.subheader("Weaponizable vs. Not Split")
pie_col1, pie_col2 = st.columns(2)
print(f"!!! weaponizable pie filtered_df = {filtered_df} !!!")

with pie_col1:
  dir_df = filtered_df.groupby("is_weaponizable")["value_usd"].sum().reset_index()
  fig_pie = px.pie(
    dir_df,
    values="value_usd",
    names="is_weaponizable",
    color_discrete_map={"false": "#636EFA", "true": "#EF553B"},
  )
  st.plotly_chart(fig_pie, use_container_width=True)

with pie_col2:
  st.markdown("### Weaponizability Breakdown")
  cat_summary = (
    filtered_df.groupby("is_weaponizable")["value_usd"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
  )
  cat_summary["value_formatted"] = cat_summary["value_usd"].apply(
    lambda x: f"${x / 1e6:,.1F}M" if x >= 1e6 else f"${x / 1e3:,.1f}K"
  )
  st.dataframe(
    cat_summary[["is_weaponizable", "value_formatted"]].rename(
      columns={"is_weaponizable": "Weaponizable", "value_formatted": "Trade Value"}
    ),
    hide_index=True,
    use_container_width=True,
  )


# --- Raw Data Table ---
st.markdown("---")
st.subheader("Raw Data")
st.dataframe(
  filtered_df.sort_values("value_usd", ascending=False).head(500),
  use_container_width=True,
)

# Export button
csv = filtered_df.to_csv(index=False)
st.download_button(
  "Download filtered data as CSV.",
  csv,
  "nola_trade_data.csv",
  "text/csv",
)
