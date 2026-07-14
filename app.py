import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Spain Top 50 Songs Dashboard", layout="wide")

st.title("🎵 Spain Top 50 Songs Analysis Dashboard")

# Load Dataset
df = pd.read_csv("Atlantic_Spain.csv")

# Convert Date
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

# Sidebar
st.sidebar.header("Filters")

artists = st.sidebar.multiselect(
    "Select Artist",
    sorted(df["artist"].unique()),
    default=sorted(df["artist"].unique())
)

df = df[df["artist"].isin(artists)]

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Songs", len(df))
col2.metric("Unique Artists", df["artist"].nunique())
col3.metric("Average Popularity", round(df["popularity"].mean(), 2))
col4.metric("Explicit Songs", int(df["is_explicit"].sum()))

st.markdown("---")

# Top Artists
st.subheader("Top Artists")

artist_count = (
    df["artist"]
    .value_counts()
    .reset_index()
)

artist_count.columns = ["Artist", "Songs"]

fig = px.bar(
    artist_count.head(10),
    x="Artist",
    y="Songs",
    color="Songs"
)

st.plotly_chart(fig, use_container_width=True)

# Popularity Distribution
st.subheader("Popularity Distribution")

fig2 = px.histogram(
    df,
    x="popularity",
    nbins=20,
    color="album_type"
)

st.plotly_chart(fig2, use_container_width=True)

# Explicit Content
st.subheader("Explicit vs Clean Songs")

explicit = (
    df["is_explicit"]
    .value_counts()
    .reset_index()
)

explicit.columns = ["Explicit", "Count"]

explicit["Explicit"] = explicit["Explicit"].replace(
    {True: "Explicit", False: "Clean"}
)

fig3 = px.pie(
    explicit,
    names="Explicit",
    values="Count"
)

st.plotly_chart(fig3, use_container_width=True)

# Album Types
st.subheader("Album Types")

fig4 = px.bar(
    df["album_type"].value_counts().reset_index(),
    x="album_type",
    y="count"
)

st.plotly_chart(fig4, use_container_width=True)

# Playlist Positions
st.subheader("Song Positions")

fig5 = px.scatter(
    df,
    x="position",
    y="popularity",
    color="artist",
    hover_data=["song"]
)

st.plotly_chart(fig5, use_container_width=True)

# Song Duration
st.subheader("Song Duration")

df["duration_min"] = df["duration_ms"] / 60000

fig6 = px.box(
    df,
    y="duration_min",
    color="album_type"
)

st.plotly_chart(fig6, use_container_width=True)

# Dataset
st.subheader("Dataset")

st.dataframe(df)

# Download
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "Spain_Songs.csv",
    "text/csv"
)
