import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="RedNote Research Monitor",
    page_icon="📊",
    layout="wide"
)

st.title("RedNote Research Monitor")
st.write("An open-source dashboard for researching trends on Xiaohongshu (RedNote).")

st.info(
    "Prototype version: the data shown below is simulated. "
    "No live RedNote data is being collected yet."
)

# -----------------------------
# Simulated dataset
# -----------------------------

np.random.seed(42)

keywords = ["人工智能", "美国", "旅游", "留学"]
dates = pd.date_range(end=pd.Timestamp.today(), periods=30)

rows = []

for keyword in keywords:
    for day in dates:
        posts = np.random.randint(10, 100)
        likes = np.random.randint(100, 3000)
        comments = np.random.randint(10, 400)
        saves = np.random.randint(20, 800)

        rows.append(
            {
                "Date": day,
                "Keyword": keyword,
                "Posts": posts,
                "Likes": likes,
                "Comments": comments,
                "Saves": saves,
            }
        )

df = pd.DataFrame(rows)

# -----------------------------
# Sidebar controls
# -----------------------------

st.sidebar.header("Research Controls")

selected_keywords = st.sidebar.multiselect(
    "Select keywords",
    options=keywords,
    default=keywords
)

filtered_df = df[df["Keyword"].isin(selected_keywords)]

# -----------------------------
# Summary statistics
# -----------------------------

st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Posts",
    f"{filtered_df['Posts'].sum():,}"
)

col2.metric(
    "Likes",
    f"{filtered_df['Likes'].sum():,}"
)

col3.metric(
    "Comments",
    f"{filtered_df['Comments'].sum():,}"
)

col4.metric(
    "Saves",
    f"{filtered_df['Saves'].sum():,}"
)

# -----------------------------
# Posting trends
# -----------------------------

st.subheader("Posting Activity Over Time")

post_chart = (
    filtered_df
    .pivot(index="Date", columns="Keyword", values="Posts")
)

st.line_chart(post_chart)

# -----------------------------
# Engagement comparison
# -----------------------------

st.subheader("Engagement by Keyword")

engagement = (
    filtered_df
    .groupby("Keyword")[["Likes", "Comments", "Saves"]]
    .mean()
    .round()
)

st.bar_chart(engagement)

# -----------------------------
# Data explorer
# -----------------------------

st.subheader("Research Data")

st.write(
    "Eventually, this section will contain observations collected "
    "from RedNote."
)

st.dataframe(
    filtered_df.sort_values("Date", ascending=False),
    use_container_width=True
)

# -----------------------------
# About
# -----------------------------

st.divider()

st.caption(
    "RedNote Research Monitor — prototype research tool. "
    "All data currently displayed is simulated."
)
