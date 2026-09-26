import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="RedNote U.S. Discourse Monitor",
    page_icon="📊",
    layout="wide"
)

st.title("RedNote U.S. Discourse Monitor")
st.write(
    "A research dashboard for examining discussion of the United States "
    "on Xiaohongshu (RedNote)."
)

st.warning(
    "Prototype: all data shown here is simulated. "
    "No live RedNote data is being collected yet."
)

# -----------------------------
# Research terms
# -----------------------------

keywords = {
    "美国": "United States",
    "美国人": "Americans",
    "中美关系": "U.S.–China relations",
    "特朗普": "Trump",
}

# -----------------------------
# Create simulated post-level data
# -----------------------------

np.random.seed(42)

dates = pd.date_range(
    end=pd.Timestamp.today().normalize(),
    periods=90
)

rows = []
post_number = 1

for date in dates:
    for keyword in keywords:

        number_of_posts = np.random.randint(2, 15)

        for _ in range(number_of_posts):

            rows.append(
                {
                    "Post ID": f"SIM-{post_number:05d}",
                    "Date": date,
                    "Keyword": keyword,
                    "English": keywords[keyword],
                    "Likes": np.random.randint(0, 5000),
                    "Comments": np.random.randint(0, 500),
                    "Saves": np.random.randint(0, 1500),
                    "Title": f"Simulated RedNote post about {keywords[keyword]}",
                }
            )

            post_number += 1

df = pd.DataFrame(rows)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Research Controls")

selected_keywords = st.sidebar.multiselect(
    "Keywords",
    options=list(keywords.keys()),
    default=list(keywords.keys())
)

date_range = st.sidebar.date_input(
    "Date range",
    value=(dates.min().date(), dates.max().date()),
    min_value=dates.min().date(),
    max_value=dates.max().date(),
)

filtered = df[df["Keyword"].isin(selected_keywords)]

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered = filtered[
        (filtered["Date"].dt.date >= start_date)
        & (filtered["Date"].dt.date <= end_date)
    ]

# -----------------------------
# Overview
# -----------------------------

st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Posts",
    f"{len(filtered):,}"
)

col2.metric(
    "Median Likes",
    f"{filtered['Likes'].median():,.0f}"
)

col3.metric(
    "Median Comments",
    f"{filtered['Comments'].median():,.0f}"
)

col4.metric(
    "Median Saves",
    f"{filtered['Saves'].median():,.0f}"
)

# -----------------------------
# Tabs
# -----------------------------

trends_tab, posts_tab, methods_tab = st.tabs(
    ["Trends", "Post Explorer", "Methodology"]
)

# -----------------------------
# Trends
# -----------------------------

with trends_tab:

    st.subheader("Post Volume Over Time")

    daily_counts = (
        filtered
        .groupby(["Date", "Keyword"])
        .size()
        .reset_index(name="Posts")
        .pivot(
            index="Date",
            columns="Keyword",
            values="Posts"
        )
        .fillna(0)
    )

    st.line_chart(daily_counts)

    st.subheader("Typical Engagement by Keyword")

    engagement = (
        filtered
        .groupby("Keyword")[["Likes", "Comments", "Saves"]]
        .median()
        .round()
    )

    st.bar_chart(engagement)

# -----------------------------
# Post explorer
# -----------------------------

with posts_tab:

    st.subheader("Posts")

    display_columns = [
        "Date",
        "Keyword",
        "Title",
        "Likes",
        "Comments",
        "Saves",
        "Post ID"
    ]

    st.dataframe(
        filtered[display_columns]
        .sort_values("Likes", ascending=False),
        use_container_width=True
    )

    csv = filtered.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="rednote_research_data.csv",
        mime="text/csv"
    )

# -----------------------------
# Methodology
# -----------------------------

with methods_tab:

    st.subheader("Research Question")

    st.write(
        "How does discussion of the United States on RedNote "
        "change over time?"
    )

    st.subheader("Tracked Search Terms")

    for chinese, english in keywords.items():
        st.write(f"**{chinese}** — {english}")

    st.subheader("Planned Variables")

    st.write(
        """
        Each collected post will eventually include:

        - Post ID
        - Search term
        - Publication date
        - Collection date/time
        - Post title
        - Post text
        - Likes
        - Comments
        - Saves
        - Hashtags
        - Post URL
        """
    )

    st.subheader("Current Limitation")

    st.write(
        "This prototype uses simulated data. "
        "The next development stage will replace it with "
        "publicly available RedNote data."
    )

st.divider()

st.caption(
    "RedNote U.S. Discourse Monitor — research prototype"
)
