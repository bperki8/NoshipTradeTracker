"""Streamlit dashboard for Port of New Orleans trade data.

This is the PUBLIC, deployable version. It reads exclusively from the committed
local database (``data/trade.db``) produced by ``ingest.py``--it never calls a
trade API and never loads an API key. To refresh or expand the data, run
``python ingest.py`` locally and commit the updated database.

Run with: streamlit run dashboard.py
"""
import plotly.io as pio
import plotly.express as px
import streamlit as st

from src.models import ProductCategory
from src import database

# Palestinian Light Theme
pio.templates["palestine_light"] = pio.templates["plotly_white"].update({
    "layout": {
        "font": {"color": "#000000"},
        "paper_bgcolor": "#FFFFFF",
        "plot_bgcolor": "#FFFFFF",
        "colorway": ["#D90000", "#007A3D", "#000000"],
    }
})

# Force Light Mode
pio.templates.default = "palestine_light"

# Light Mode CSS
st.markdown(
    """
    <style>
    body, .stApp, .main, .block-container {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    .stSidebar, .stSidebar > div {
        background-color: #F5F5F5 !important;
    }
    </style>
    """,
  unsafe_allow_html=True,
)

st.set_page_config(
  page_title="NOLA Trade Tracker",
  page_icon="🚢",
  layout="wide",
)

st.markdown(
  """
  <style>
  [data-testid="stStatusWidget"] [data-testid="Avatar"],
  [data-testid="stStatusWidget"] img,
  [data-testid="stStatusWidget"] svg {
      display: none !important;
  }
  [data-testid="stStatusWidget"] > div::before {
      content: "🚢";
      font-size: 1.1rem;
      margin-right: 0.4rem;
      display: inline-block;
      animation: nola-sail 1.4s ease-in-out infinite;
  }
  @keyframes nola-sail {
      0%, 100%  { transform: translateX(0);   opacity: 1; }
      50%       { transform: translateX(4px); opacity: 0.55; }
  }
  </style>
  """,
  unsafe_allow_html=True,
)

st.title("Port of New Orleans Trade Tracker")
st.markdown("Analyze imports and exports flowing through the Port of New Orleans.")


# --- Data loading (from the committed local databae, cached) ---
@st.cache_data(show_spinner="Loading trade database...")
def load_data():
  return database.load_dataframe()


df = load_data()

if df.empty:
  st.error("No data found in the local databawse.")
  st.info(
    "Run the ingest step locally and commit the result:\n\n"
    "```bash\npython ingest.py          # default: Israel, last 13 years\n```\n\n"
    "This creates `data/trade.db`, which this dashboard reads from."
  )
  st.stop()


# --- Sidebar Filters (populated dynamically from whatever is in the DB) ---
st.sidebar.header("Filters")

countries = sorted(df["country_name"].dropna().unique().tolist())
selected_countries  = st.sidebar.multiselect(
  "Countries", countries, default=countries,
  help="Driven by the data in the database. Ingest more countries to add options.",
)

ports = sorted(df["port_name"].dropna().unique().tolist())
selected_ports = st.sidebar.multiselect("Ports", ports, default=ports)

sources = sorted(df["source"].dropna().unique().tolist())
selected_sources = st.sidebar.multiselect("Data Source", sources, default=sources)

direction_choice = st.sidebar.selectbox(
  "Trade Direction", ["Exports", "Both", "Imports"],
)

year_min, year_max = int(df["year"].min()), int(df["year"].max())
if year_min < year_max:
  year_range = st.sidebar.slider(
    "Year Range", min_value=year_min, max_value=year_max,
    value=(year_min, year_max),
  )
else:
  year_range = (year_min, year_max)
  st.sidebar.markdown(f"**Year:** {year_min}")

category_options = [c.value for c in ProductCategory]
present_categories = [c for c in category_options if c in set(df["category"])]
selected_categories = st.sidebar.multiselect("Product Categories", present_categories)


# --- Apply Filters ---
filtered_df = df.copy()

if selected_countries:
  filtered_df = filtered_df[filtered_df["country_name"].isin(selected_countries)]
if selected_ports:
  filtered_df = filtered_df[filtered_df["port_name"].isin(selected_ports)]
if selected_sources:
  filtered_df = filtered_df[filtered_df["source"].isin(selected_sources)]

if direction_choice == "Imports":
  filtered_df = filtered_df[filtered_df["direction"] == "import"]
if direction_choice == "Exports":
  filtered_df = filtered_df[filtered_df["direction"] == "export"]

filtered_df = filtered_df[
  (filtered_df["year"] >= year_range[0]) & (filtered_df["year"] <= year_range[1])
]

if selected_categories:
  filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

st.sidebar.markdown(f"**{len(filtered_df):,}** records after filtering.")

if filtered_df.empty:
  st.warning("No records match the current filters. Try widening them.")
  st.stop()


# --- Summary Metrics ---
col1, col2, col3, col4 = st.columns(4)

total_value = filtered_df["value_usd"].sum()

not_weaponizable_value = filtered_df[filtered_df["is_weaponizable"] == 0]["value_usd"].sum()
weaponizable_value = filtered_df[filtered_df["is_weaponizable"] == 1]["value_usd"].sum()

n_countries = filtered_df["country_name"].nunique()

col1.metric("Total Trade Value", f"${total_value / 1e6:,.1f}M")
col2.metric("Weaponizable", f"${weaponizable_value / 1e6:,.1f}M")
col3.metric("Not Weaponizable", f"${not_weaponizable_value / 1e6:,.1f}M")
col4.metric("Trading Partners", f"{n_countries}")



# --- Charts ---
st.markdown("---")

# Weaponizable Pie
st.subheader("Weaponizable vs. Not Split")
pie_col1, pie_col2 = st.columns(2)

with pie_col1:
    dir_df = filtered_df.groupby("is_weaponizable")["value_usd"].sum().reset_index()

    dir_df["weaponizable_label"] = dir_df["is_weaponizable"].map({
        0: "Not Weaponizable",
        1: "Weaponizable",
    })

    fig_pie = px.pie(
        dir_df,
        values="value_usd",
        names="weaponizable_label",
        color="is_weaponizable",
        color_discrete_map={
            0: "#007A3D",  # green
            1: "#D90000",  # red
        },
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

    cat_summary["Weaponizable"] = cat_summary["is_weaponizable"].map({
        0: "Not Weaponizable",
        1: "Weaponizable",
    })

    cat_summary["value_formatted"] = cat_summary["value_usd"].apply(
        lambda x: f"${x / 1e6:,.1F}M" if x >= 1e6 else f"${x / 1e3:,.1f}K"
    )

    st.dataframe(
        cat_summary[["Weaponizable", "value_formatted"]].rename(
            columns={"value_formatted": "Trade Value"}
        ),
        hide_index=True,
        use_container_width=True,
    )

st.subheader("Weaponizability by Category")

# Aggregate by category + weaponizability
stack_df = (
    filtered_df.groupby(["category", "is_weaponizable"])["value_usd"]
    .sum()
    .reset_index()
)

# Human-readable labels
stack_df["weaponizable_label"] = stack_df["is_weaponizable"].map({
    0: "Not Weaponizable",
    1: "Weaponizable",
})

# Sort categories by total trade value
category_order = (
    stack_df.groupby("category")["value_usd"].sum().sort_values(ascending=False).index
)

fig_stack = px.bar(
    stack_df,
    x="category",
    y="value_usd",
    color="weaponizable_label",
    category_orders={"category": category_order},
    color_discrete_map={
        "Not Weaponizable": "#007A3D",  # green
        "Weaponizable": "#D90000",      # red
    },
)

fig_stack.update_layout(barmode="stack")

st.plotly_chart(fig_stack, use_container_width=True)

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

# Top Commodities (most useful when focused on a single country) + Top Partners.
# When the DB holds one country, the partners chart is a single bar, so we lead
# with commodities; both stay meaningful as more countries are ingested.
with chart_col2:
  if n_countries > 1:
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
  else:
    st.subheader("Top 15 Commodities")
    comm_df = (
      filtered_df.groupby("commodity")["value_usd"]
      .sum()
      .nlargest(15)
      .sort_values(ascending=True)
      .reset_index()
    )
    comm_df["commodity"] = comm_df["commodity"].fillna("(unlabeled)").str.slice(0, 40)
    fig_comm = px.bar(
      comm_df,
      x="value_usd",
      y="commodity",
      orientation="h",
      labels={"value_usd": "Value (USD)", "commodity": "Commodity"},
      color="value_usd",
      color_continuous_scale="Viridis",
    )
    fig_comm.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig_comm, use_container_width=True)


# Trade Over Time (line chart)
st.subheader("Trade Value Over Time")
time_df = (
  filtered_df.groupby(["period", "direction"])["value_usd"]
  .sum()
  .reset_index()
  .sort_values("period")
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


# Category Treemap (category -> commodity, useful in single-country focus)
st.subheader("Trade Composition")
treemap_df = (
  filtered_df.assign(commodity=filtered_df["commodity"].fillna("(unlabeled)"))
  .groupby(["category", "commodity"])["value_usd"]
  .sum()
  .reset_index()
  .nlargest(50, "value_usd")
)
if not treemap_df.empty:
  fig_tree = px.treemap(
    treemap_df,
    path=["category", "commodity"],
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

    # Normalize direction labels if needed (optional)
    dir_df["direction"] = dir_df["direction"].str.lower()

    fig_pie = px.pie(
        dir_df,
        values="value_usd",
        names="direction",
        color="direction",
        color_discrete_map={
            "import": "#007A3D",  # green
            "export": "#D90000",  # red
        },
    )

    st.plotly_chart(fig_pie, use_container_width=True)


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
