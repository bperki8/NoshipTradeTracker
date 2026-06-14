import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import load_visits

st.set_page_config(page_title="Usage Dashboard", layout="wide")

st.title("📊 Usage Dashboard")
st.caption("Analytics based on local persistent `analytics.json`")

# Load data
visits = load_visits()
df = pd.DataFrame(visits)

if df.empty:
    st.info("No analytics data yet.")
    st.stop()

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["date"] = df["timestamp"].dt.date
df["month"] = df["timestamp"].dt.to_period("M").astype(str)
df["year"] = df["timestamp"].dt.year
df["hour"] = df["timestamp"].dt.hour

# --- Summary Metrics ---
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Visits", len(df))
col2.metric("Unique Days", df["date"].nunique())
col3.metric("Unique Months", df["month"].nunique())
col4.metric("Unique Years", df["year"].nunique())

st.markdown("---")

# --- Daily Active Users ---
st.subheader("📅 Daily Active Users")
daily = df.groupby("date").size().reset_index(name="visits")
fig_daily = px.line(daily, x="date", y="visits", markers=True)
st.plotly_chart(fig_daily, use_container_width=True)

# --- Monthly Active Users ---
st.subheader("📆 Monthly Active Users")
monthly = df.groupby("month").size().reset_index(name="visits")
fig_monthly = px.bar(monthly, x="month", y="visits")
st.plotly_chart(fig_monthly, use_container_width=True)

# --- Visitors by Country ---
if "country" in df.columns:
    st.subheader("🌍 Visitors by Country")
    country_counts = df["country"].value_counts().reset_index()
    country_counts.columns = ["country", "visits"]
    fig_country = px.bar(country_counts, x="country", y="visits")
    st.plotly_chart(fig_country, use_container_width=True)

# --- Visitors by City ---
if "city" in df.columns:
    st.subheader("🏙️ Visitors by City")
    city_counts = df["city"].value_counts().reset_index()
    city_counts.columns = ["city", "visits"]
    fig_city = px.bar(city_counts, x="city", y="visits")
    st.plotly_chart(fig_city, use_container_width=True)

# --- Time of Day Heatmap ---
st.subheader("⏰ Time of Day Heatmap")
heat = df.groupby(["hour", "date"]).size().reset_index(name="visits")
fig_heat = px.density_heatmap(
    heat,
    x="hour",
    y="date",
    z="visits",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_heat, use_container_width=True)

# --- Geographic Map ---
if {"latitude", "longitude"}.issubset(df.columns):
    st.subheader("🗺️ Visitor Map")
    fig_map = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="city",
        color="country",
        projection="natural earth"
    )
    st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")
st.caption("Data stored locally in `analytics.json`")
