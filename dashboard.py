"""Streamlit dashboard for Port of New Orleans trade data.

This is the PUBLIC, deployable version. It reads exclusively from the committed
local database (``data/trade.db``) produced by ``ingest.py``--it never calls a
trade API and never loads an API key. To refresh or expand the data, run
``python ingest.py`` locally and commit the updated database.

Run with: streamlit run dashboard.py
"""
import calendar
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

from analytics import log_visit
from src.models import ProductCategory
from src import database
from streamlit_js_eval import streamlit_js_eval

def format_period(period: str) -> str:
  year, month = period.split("-")
  month_abbr = calendar.month_abbr[int(month)].upper()
  return f"{month_abbr} {year}"

st.set_page_config(
  page_title="NOSHIP Trade Tracker",
  page_icon="🚢",
  layout="wide",
)

st.markdown("""
<!-- Open Graph metadata -->
<meta property="og:title" content="NOSHIP Trade Tracker" />
<meta property="og:description" content="Analyze imports and exports flowing between the Port of New Orleans and Israel." />
<meta property="og:image" content="https://i0.wp.com/noship.org/wp-content/uploads/2025/01/noship-logo-2.png?fit=2932%2C2062&ssl=1" />
<meta property="og:url" content="https://noshiptradetracker.streamlit.app/" />
<meta name="twitter:card" content="summary_large_image" />
""", unsafe_allow_html=True)


# Prevent double-logging
if "logged_visit" not in st.session_state:
    st.session_state.logged_visit = False

# Fetch location (async JS)
location_data = streamlit_js_eval(
    js_expressions="await fetch('https://ipapi.co/json').then(r => r.json())",
    key="get_location"
)

# Log only once, and only when location is ready
if not st.session_state.logged_visit:
    if location_data:
        log_visit(extra={
            "country": location_data.get("country_name"),
            "city": location_data.get("city"),
            "region": location_data.get("region"),
            "timezone": location_data.get("timezone"),
            "ip": location_data.get("ip")
        })
        st.session_state.logged_visit = True
    else:
        # First run: no location yet, log minimal visit
        log_visit()
        st.session_state.logged_visit = True

st.title("NOSHIP Trade Tracker")
st.markdown(
  """
  Analyze imports and exports flowing between the Port of New Orleans and Israel.
  To report issues, use the contact links at
  <a href="https://noship.org" target="_blank" style="color:#D90000; font-weight:bold;">
    noship.org
  </a>.
  """,
  unsafe_allow_html=True,
)

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


# Force all links to open in a new tab + visited links turn green
st.markdown(
  """
  <style>
    a:visited {
      color: #007A3D !important;
      font-weight: bold;
    }
  </style>

  <script>
    document.addEventListener("DOMContentLoaded", function() {
      const links = document.querySelectorAll("a");
      links.forEach(link => {
        link.setAttribute("target", "_blank");
      });
    });
  </script>
  """,
  unsafe_allow_html=True,
)

# Soft metric backgrounds + left color bars (final working version)
st.markdown(
    """
    <style>

    .metric-card {
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 4px solid transparent;
    }

    .metric-label {
        font-size: 0.85rem;
        opacity: 0.75;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 1.4rem;
        font-weight: bold;
        margin-top: 2px;
    }

    .metric-black {
        background-color: #F2F2F2;
        border-left-color: #000000;
    }

    .metric-red {
        background-color: #FDE7E7;
        border-left-color: #D90000;
    }

    .metric-green {
        background-color: #E6F4EA;
        border-left-color: #007A3D;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Unified hover + glow styling (metric cards + table hover)
# ------------------------------------------------------------
st.markdown(
  """
  <style>

  /* -----------------------------------------------------------
     METRIC CARD HOVER (your original styles)
  ----------------------------------------------------------- */

  .metric-card {
      transition: all 0.18s ease-in-out;
      will-change: transform, box-shadow;
  }

  .metric-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0,0,0,0.18);
  }

  .metric-black:hover {
      border-left-color: #333333 !important;
  }

  .metric-red:hover {
      border-left-color: #B00000 !important;
  }

  .metric-green:hover {
      border-left-color: #006A34 !important;
  }


  /* -----------------------------------------------------------
     TABLE ROW HOVER (subtle glow, matches your UI)
  ----------------------------------------------------------- */

  .row-weaponizable:hover {
      background-color: rgba(217, 0, 0, 0.12) !important;
      box-shadow: 0 4px 12px rgba(0,0,0,0.18);
  }

  .row-not:hover {
      background-color: rgba(0, 122, 61, 0.12) !important;
      box-shadow: 0 4px 12px rgba(0,0,0,0.18);
  }

  </style>
  """,
  unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Replace Streamlit avatar with ship icon
# ------------------------------------------------------------
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
    0%, 100%  { transform: translateX(0); opacity: 1; }
    50%       { transform: translateX(4px); opacity: 0.55; }
  }
  </style>
  """,
  unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------
@st.cache_data(show_spinner="Loading trade database...")
def load_data():
  return database.load_dataframe()

df = load_data()

if df.empty:
  st.error("No data found in the local database.")
  st.info(
    "Run the ingest step locally and commit the result:\n\n"
    "```bash\npython ingest.py\n```\n\n"
    "This creates `data/trade.db`, which this dashboard reads from."
  )
  st.stop()


# ------------------------------------------------------------
# Sidebar Filters
# ------------------------------------------------------------
st.sidebar.header("Filters")

periods = sorted(df["period"].unique())

# Build mapping: "AUG 2026" → "2026-08"
pretty_to_raw = {format_period(p): p for p in periods}
pretty_periods = list(pretty_to_raw.keys())

# Default to first and last
start_pretty_default = pretty_periods[0]
end_pretty_default = pretty_periods[-1]

start_pretty = st.sidebar.selectbox(
  "Start",
  pretty_periods,
  index=0  # first item
)

end_pretty = st.sidebar.selectbox(
  "End",
  pretty_periods,
  index=len(pretty_periods) - 1  # last item
)

period_range = (
  pretty_to_raw[start_pretty],
  pretty_to_raw[end_pretty]
)


ports = sorted(df["port_name"].dropna().unique().tolist())
selected_port = st.sidebar.selectbox("Port Shipped Through", ports, index=0)

countries = sorted(df["country_name"].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Country", countries, index=0)

direction_choice = st.sidebar.selectbox(
  "Trade Direction", ["Exports", "Both", "Imports"],
)

category_options = [c.value for c in ProductCategory]
present_categories = [c for c in category_options if c in set(df["category"])]
selected_categories = st.sidebar.multiselect("Product Categories", present_categories)


# ------------------------------------------------------------
# Apply Filters
# ------------------------------------------------------------
filtered_df = df.copy()

if selected_country:
  filtered_df = filtered_df[filtered_df["country_name"] == selected_country]
if selected_port:
  filtered_df = filtered_df[filtered_df["port_name"] == selected_port]

if direction_choice == "Imports":
  filtered_df = filtered_df[filtered_df["direction"] == "import"]
if direction_choice == "Exports":
  filtered_df = filtered_df[filtered_df["direction"] == "export"]

filtered_df = filtered_df[
  (filtered_df["period"] >= period_range[0]) & (filtered_df["period"] <= period_range[1])
]

if selected_categories:
  filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

st.sidebar.markdown(f"**{len(filtered_df):,}** records after filtering.")

if filtered_df.empty:
  st.warning("No records match the current filters. Try widening them.")
  st.stop()


# ------------------------------------------------------------
# Sidebar Badge
# ------------------------------------------------------------
st.sidebar.markdown(
  """
  <hr style="margin-top: 2rem; margin-bottom: 1rem;">
  <div style="text-align: center; font-size: 0.9rem; opacity: 0.85;">
    <a href="https://noship.org" target="_blank" title="Visit NOSHIP.org">
      <img 
        src="https://i0.wp.com/noship.org/wp-content/uploads/2025/01/noship-logo-2.png?fit=2932%2C2062&ssl=1"
        width="120"
        style="opacity: 0.95; margin-bottom: 0.4rem;"
      >
    </a>
  </div>
  """,
  unsafe_allow_html=True,
)

def format_list(items):
  if not items:
    return "all categories"
  if len(items) == 1:
    return items[0]
  if len(items) == 2:
    return f"{items[0]} and {items[1]}"
  return ", ".join(items[:-1]) + f", and {items[-1]}"

category_phrase = format_list(selected_categories)

year_text = (
  f"{format_period(period_range[0])}-{format_period(period_range[1])}"
  if period_range[0] != period_range[1]
  else f"{format_period(period_range[0])}"
)

# Build the commodity phrase cleanly
if category_phrase == "all categories":
  commodity_phrase = "commodities across all categories"
else:
  commodity_phrase = f"{category_phrase} commodities"

if direction_choice == "Exports":
  subtitle = (
    f"All {commodity_phrase} exported from the Port of New Orleans "
    f"to Israel ({year_text})."
  )
elif direction_choice == "Imports":
  subtitle = (
    f"All {commodity_phrase} imported to the Port of New Orleans "
    f"from Israel ({year_text})."
  )
else:
  subtitle = (
    f"All {commodity_phrase} shipped between the Port of New Orleans "
    f"and Israel ({year_text})."
  )


# ------------------------------------------------------------
# Summary Metrics
# ------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_value = filtered_df["value_usd"].sum()
not_weaponizable_value = filtered_df[filtered_df["is_weaponizable"] == 0]["value_usd"].sum()
weaponizable_value = filtered_df[filtered_df["is_weaponizable"] == 1]["value_usd"].sum()

def metric_card(label, value, color_class):
  st.markdown(
    f"""
    <div class="metric-card {color_class}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """,
    unsafe_allow_html=True,
  )

with col1:
  metric_card("Total Trade Value", f"${total_value / 1e6:,.1f}M", "metric-black")
with col2:
  metric_card("Weaponizable", f"${weaponizable_value / 1e6:,.1f}M", "metric-red")
with col3:
  metric_card("Not Weaponizable", f"${not_weaponizable_value / 1e6:,.1f}M", "metric-green")
with col4:
  metric_card("Date Range", year_text, "metric-black")


# ------------------------------------------------------------
# Weaponizability Breakdown
# ------------------------------------------------------------
st.markdown("---")

st.markdown(
  """
  <h2 style="text-align:center; font-weight:700; margin-top:0;">
    Weaponizability Breakdown
  </h2>
  """,
  unsafe_allow_html=True
)
# Subtitle
st.empty().markdown(
  f"""
  <p style="
    text-align:center;
    font-size:0.85rem;
    color:var(--text-color-secondary);
    margin-top:-0.5rem;
    padding-bottom:0.4rem;
  ">
    {subtitle}
  </p>
  """,
  unsafe_allow_html=True
)


pie_col1, pie_col2 = st.columns(2)


# ------------------------------------------------------------
# PIE CHART (polished hover info)
# ------------------------------------------------------------
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
    color_discrete_map={0: "#007A3D", 1: "#D90000"},
  )

  fig_pie.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate="<b>%{label}</b><br>Value: $%{value:,.0f}<extra></extra>"
  )

  fig_pie.update_layout(
    showlegend=False,
    margin=dict(t=10, b=10, l=10, r=10)
  )

  st.plotly_chart(fig_pie, use_container_width=True)


# ------------------------------------------------------------
# TABLE (polished, consistent, subtle hover)
# ------------------------------------------------------------
with pie_col2:

  st.markdown("<div style='height:131px;'></div>", unsafe_allow_html=True)

  cat_summary = (
    filtered_df.groupby("is_weaponizable")["value_usd"]
    .sum()
    .reset_index()
  )

  cat_summary["Weaponizable"] = cat_summary["is_weaponizable"].map({
    0: "Not Weaponizable",
    1: "Weaponizable",
  })

  # Force consistent ordering
  cat_summary = cat_summary.sort_values(
    by="Weaponizable",
    key=lambda s: s.map({"Weaponizable": 0, "Not Weaponizable": 1})
  )

  cat_summary["value_formatted"] = cat_summary["value_usd"].apply(
    lambda x: f"${x / 1e6:,.1F}M" if x >= 1e6 else f"${x / 1e3:,.1f}K"
  )

  def color_label(val):
    if val == "Weaponizable":
      return "background-color: #D90000; color: white;"
    else:
      return "background-color: #007A3D; color: white;"

  styled = (
    cat_summary[["Weaponizable", "value_formatted"]]
    .rename(columns={"value_formatted": "Trade Value"})
    .style.map(color_label, subset=["Weaponizable"])
  )

  st.dataframe(styled, hide_index=True, use_container_width=True)


# ------------------------------------------------------------
# Trade Value Over Time (dual-axis)
# ------------------------------------------------------------
st.subheader("Trade Value Over Time")
st.empty().caption(subtitle)

# --- Toggle for Year vs Month ---
granularity = st.radio(
  "Time Granularity",
  ["Yearly", "Monthly"],
  horizontal=True,
)

# Dynamic legend labels
if direction_choice == "Imports":
  total_label = "Total Imports"
  weapon_label = "Weaponizable Imports"
elif direction_choice == "Exports":
  total_label = "Total Exports"
  weapon_label = "Weaponizable Exports"
else:
  total_label = "Total Trade"
  weapon_label = "Weaponizable Trade"

# --- Ensure period is a datetime ---
filtered_df["period"] = pd.to_datetime(filtered_df["period"], errors="coerce")

# --- Build grouping key based on toggle ---
if granularity == "Yearly":
  filtered_df["period_group"] = filtered_df["period"].dt.year.astype(str)
else:
  filtered_df["period_group"] = filtered_df["period"].dt.to_period("M").astype(str)

# --- Aggregate ---
total_time_df = (
  filtered_df.groupby("period_group")["value_usd"]
  .sum()
  .reset_index()
)

weapon_time_df = (
  filtered_df[filtered_df["is_weaponizable"] == 1]
  .groupby("period_group")["value_usd"]
  .sum()
  .reset_index()
)

# --- Merge ---
merged = total_time_df.merge(
  weapon_time_df,
  on="period_group",
  how="left",
  suffixes=("_total", "_weapon")
)
merged["value_usd_weapon"] = merged["value_usd_weapon"].fillna(0)
merged["pct_weaponizable"] = (
  merged["value_usd_weapon"] / merged["value_usd_total"]
).fillna(0) * 100

# --- X-axis label formatting ---
if granularity == "Yearly":
  x_vals = merged["period_group"]
  hover_x = "<b>%{x}</b><br>"
else:
  # Monthly: convert "YYYY-MM" to nicer "YYYY‑MM"
  x_vals = merged["period_group"]
  hover_x = "<b>%{x}</b><br>"  # already clean

fig = go.Figure()

# --- Total trade trace ---
fig.add_trace(go.Scatter(
  x=x_vals,
  y=merged["value_usd_total"],
  mode="lines+markers",
  name=total_label,
  line=dict(color="#000000", width=2),
  yaxis="y1",
  hovertemplate=(
    hover_x +
    f"{total_label}: $%{{y:,.0f}}<br>" +
    "<extra></extra>"
  ),
))

# --- Weaponizable trade trace ---
fig.add_trace(go.Scatter(
  x=x_vals,
  y=merged["value_usd_weapon"],
  mode="lines+markers",
  name=weapon_label,
  line=dict(color="#007A3D", width=2),
  yaxis="y1",
  hovertemplate=(
    hover_x +
    f"{weapon_label}: $%{{y:,.0f}}<br>" +
    "<extra></extra>"
  ),
))

# --- Percentage trace ---
fig.add_trace(go.Scatter(
  x=x_vals,
  y=merged["pct_weaponizable"],
  mode="lines+markers",
  name="% Weaponizable",
  line=dict(color="#D90000", width=2, dash="dash"),
  yaxis="y2",
  customdata=merged[["value_usd_weapon", "value_usd_total"]],
  hovertemplate=(
    hover_x +
    "% Weaponizable: %{y:.1f}%<br>" +
    f"{weapon_label}: $%{{customdata[0]:,.0f}}<br>" +
    f"{total_label}: $%{{customdata[1]:,.0f}}<br>" +
    "<extra></extra>"
  ),
))

fig.update_layout(
  height=450,
  yaxis=dict(title="Trade Value (USD)", showgrid=False),
  yaxis2=dict(
    title="% Weaponizable",
    overlaying="y",
    side="right",
    showgrid=False,
    range=[0, max(merged["pct_weaponizable"].max() * 1.2, 5)],
  ),
  legend=dict(orientation="h"),
)

st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------
# CATEGORY TREEMAP
# ------------------------------------------------------------
st.subheader("Trade Composition")
st.empty().caption(subtitle)

# --- Prepare Data ---
df = filtered_df.assign(
  commodity=filtered_df["commodity"].fillna("(unlabeled)")
)

# Compute weaponizable ratio per category
category_ratio = (
  df.groupby("category")["is_weaponizable"]
    .mean()
    .rename("weaponizable_ratio")
)

# Compute weaponizable value per commodity
weaponizable_value = (
  df[df["is_weaponizable"] == 1]
    .groupby(["category", "commodity"])["value_usd"]
    .sum()
    .rename("weaponizable_value")
)

# Aggregate commodity-level values
treemap_df = (
  df.groupby(["category", "commodity", "is_weaponizable"])["value_usd"]
    .sum()
    .reset_index()
    .merge(category_ratio, on="category")
    .merge(weaponizable_value, on=["category", "commodity"], how="left")
    .fillna({"weaponizable_value": 0})
)

# --- Add category-level rows so hover works on parent nodes ---
category_totals = treemap_df.groupby("category")["value_usd"].sum()
category_weaponizable_totals = (
  treemap_df[treemap_df["is_weaponizable"] == 1]
    .groupby("category")["value_usd"]
    .sum()
)

category_level = (
  pd.DataFrame({
    "category": category_totals.index,
    "commodity": "(category-level)",
    "is_weaponizable": None,
    "value_usd": category_totals.values,
    "weaponizable_value": category_weaponizable_totals.reindex(category_totals.index).fillna(0).values,
  })
  .merge(category_ratio, on="category")
)

treemap_df = pd.concat([treemap_df, category_level], ignore_index=True)

# --- Color Logic ---
treemap_df["color_value"] = treemap_df.apply(
  lambda row: (
    row["weaponizable_ratio"]
    if row["commodity"] == "(category-level)"
    else row["is_weaponizable"]
  ),
  axis=1
)

# --- Hover Text ---
treemap_df["hover"] = treemap_df.apply(
  lambda row: (
    f"<b>Category:</b> {row['category']}<br>"
    f"<b>Commodity:</b> {row['commodity']}<br>"
    f"<b>Total Value:</b> ${row['value_usd']:,.0f}<br>"
    f"<b>Weaponizable Value:</b> ${row['weaponizable_value']:,.0f}<br>"
    f"<b>Category Weaponizable %:</b> {row['weaponizable_ratio']*100:.1f}%"
  ),
  axis=1
)

# --- Build Treemap ---
fig_tree = px.treemap(
  treemap_df,
  path=["category", "commodity"],
  values="value_usd",
  color="color_value",
  hover_data={"hover": True},
  custom_data=["hover"],
  color_continuous_scale=[
    (0.0, "#007A3D"),  # green
    (0.5, "#FFD700"),  # yellow
    (1.0, "#D90000"),  # red
  ],
  range_color=(0, 1),
)

# --- FIX HOVER FOR CATEGORY NODES ---
# Build mapping from (category, commodity) → hover text
hover_map = {
  (row["category"], row["commodity"]): row["hover"]
  for _, row in treemap_df.iterrows()
}

# Assign hover text in the exact order Plotly created nodes
for trace in fig_tree.data:
  new_customdata = []
  for node_id in trace.ids:
    parts = node_id.split("/")
    if len(parts) == 1:
      key = (parts[0], "(category-level)")
    else:
      key = (parts[0], parts[1])
    new_customdata.append(hover_map.get(key, ""))
  trace.customdata = new_customdata
  trace.hovertemplate = "%{customdata}<extra></extra>"

fig_tree.update_coloraxes(
  colorbar=dict(
    tickvals=[0, 1],
    ticktext=["Not Weaponizable", "Weaponizable"],
    title=None
  )
)

fig_tree.update_layout(height=600)
st.plotly_chart(fig_tree, use_container_width=True)


# ------------------------------------------------------------
# Weaponizability by Category
# ------------------------------------------------------------
st.subheader("Weaponizability by Category")
st.empty().caption(subtitle)

# Aggregate
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

# Compute totals + percentages for hover
totals = stack_df.groupby("category")["value_usd"].sum().rename("total_value")
stack_df = stack_df.merge(totals, on="category")
stack_df["pct_of_category"] = (stack_df["value_usd"] / stack_df["total_value"]) * 100

# Order categories by total value
category_order = (
  stack_df.groupby("category")["value_usd"]
  .sum()
  .sort_values(ascending=False)
  .index
)

# Build figure
fig_stack = px.bar(
  stack_df,
  x="category",
  y="value_usd",
  color="weaponizable_label",
  category_orders={"category": category_order},
  color_discrete_map={
    "Not Weaponizable": "#007A3D",
    "Weaponizable": "#D90000",
  },
)

# Correct customdata assignment per trace
for trace in fig_stack.data:
  label = trace.name  # "Weaponizable" or "Not Weaponizable"
  mask = stack_df["weaponizable_label"] == label

  trace.customdata = stack_df.loc[
    mask, ["weaponizable_label", "pct_of_category", "total_value"]
  ].to_numpy()

  trace.hovertemplate = (
    "<b>%{x}</b><br>" +
    "%{customdata[0]}: $%{y:,.0f}<br>" +
    "Share of Category: %{customdata[1]:.1f}%<br>" +
    "Category Total: $%{customdata[2]:,.0f}<br>" +
    "<extra></extra>"
  )

fig_stack.update_layout(
  barmode="stack",
  legend_title_text=None
)

st.plotly_chart(fig_stack, use_container_width=True)


# ------------------------------------------------------------
# Two-column layout for category + partners/commodities
# ------------------------------------------------------------
# TODO: Delete for good or add it back.
# chart_col1, chart_col2 = st.columns(2)

# with chart_col1:
#   st.subheader("Trade Value by Category")
#   cat_df = (
#     filtered_df.groupby("category")["value_usd"]
#     .sum()
#     .sort_values(ascending=True)
#     .reset_index()
#   )
#   fig_cat = px.bar(
#     cat_df,
#     x="value_usd",
#     y="category",
#     orientation="h",
#     labels={"value_usd": "Value (USD)", "category": "Category"},
#     color="category",
#     color_discrete_sequence=px.colors.qualitative.Set3,
#   )
#   fig_cat.update_layout(showlegend=False, height=500)
#   st.plotly_chart(fig_cat, use_container_width=True)

# n_countries = filtered_df["country_name"].nunique()
# with chart_col2:
#   if n_countries > 1:
#     st.subheader("Top 15 Trading Partners")
#     country_df = (
#       filtered_df.groupby("country_name")["value_usd"]
#       .sum()
#       .nlargest(15)
#       .sort_values(ascending=True)
#       .reset_index()
#     )
#     fig_country = px.bar(
#       country_df,
#       x="value_usd",
#       y="country_name",
#       orientation="h",
#       labels={"value_usd": "Value (USD)", "country_name": "Country"},
#       color="value_usd",
#       color_continuous_scale="Viridis",
#     )
#     fig_country.update_layout(showlegend=False, height=500)
#     st.plotly_chart(fig_country, use_container_width=True)
#   else:
#     st.subheader("Top 15 Commodities")
#     comm_df = (
#       filtered_df.groupby("commodity")["value_usd"]
#       .sum()
#       .nlargest(15)
#       .sort_values(ascending=True)
#       .reset_index()
#     )
#     comm_df["commodity"] = comm_df["commodity"].fillna("(unlabeled)").str.slice(0, 40)
#     fig_comm = px.bar(
#       comm_df,
#       x="value_usd",
#       y="commodity",
#       orientation="h",
#       labels={"value_usd": "Value (USD)", "commodity": "Commodity"},
#       color="value_usd",
#       color_continuous_scale="Viridis",
#     )
#     fig_comm.update_layout(showlegend=False, height=500)
#     st.plotly_chart(fig_comm, use_container_width=True)


# # Import vs Export Pie
# st.subheader("Import vs. Export Split")
# pie_col1, pie_col2 = st.columns(2)

# with pie_col1:
#   dir_df = filtered_df.groupby("direction")["value_usd"].sum().reset_index()
#   dir_df["direction"] = dir_df["direction"].str.lower()
#   fig_pie = px.pie(
#     dir_df,
#     values="value_usd",
#     names="direction",
#     color="direction",
#     color_discrete_map={
#       "import": "#007A3D",
#       "export": "#D90000",
#     },
#   )
#   st.plotly_chart(fig_pie, use_container_width=True)

# Raw Data Table
st.markdown("---")
st.subheader("Raw Data")
st.empty().caption(subtitle)
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

# --- NOSHIP Footer Attribution ---
st.markdown(
  """
  <div style="text-align: center; margin-top: 3rem; opacity: 0.75;">
    Built by 
    <a href="https://noship.org" target="_blank" 
       style="text-decoration: none; color: #D90000; font-weight: bold;"
       title="Visit NOSHIP.org">
      NOSHIP
    </a>.
  </div>
  """,
  unsafe_allow_html=True,
)
