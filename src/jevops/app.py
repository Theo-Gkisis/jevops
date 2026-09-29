import time

import pandas as pd
import plotly.express as px
import streamlit as st

from jevops.cluster import cluster_errors
from jevops.parser import classify_all

STATUS_COLORS = {
    "normal": "#0ca30c",
    "warning": "#fab219",
    "error": "#ec835a",
    "critical": "#d03b3b",
}
CATEGORY_ORDER = ["normal", "warning", "error", "critical"]

st.set_page_config(page_title="JevOps", layout="wide")
st.title("JevOps")

uploaded = st.file_uploader("Upload a log file")

if uploaded:
    lines = uploaded.read().decode().splitlines()

    progress_bar = st.progress(0.0, text="Classifying unique patterns with JEV...")

    def update_progress(done, total):
        progress_bar.progress(done / total, text=f"Classifying unique patterns with JEV... {done}/{total}")

    start = time.time()
    classified = classify_all(lines, on_progress=update_progress)  # (line, category, confidence, cost)
    elapsed = time.time() - start
    progress_bar.empty()

    total_cost = sum(cost for _, _, _, cost in classified)

    counts = {cat: 0 for cat in CATEGORY_ORDER}
    for _, category, _, _ in classified:
        counts[category] = counts.get(category, 0) + 1
    total = sum(counts.values()) or 1

    time_col, cost_col = st.columns(2)
    time_col.metric("Time", f"{elapsed:.1f}s")
    cost_col.metric("Cost", f"${total_cost:.4f}")

    cols = st.columns(len(CATEGORY_ORDER))
    for col, cat in zip(cols, CATEGORY_ORDER):
        pct = 100 * counts[cat] / total
        col.metric(cat.capitalize(), counts[cat], f"{pct:.0f}%")

    chart_df = pd.DataFrame({"category": CATEGORY_ORDER, "count": [counts[c] for c in CATEGORY_ORDER]})
    fig = px.bar(
        chart_df,
        x="category",
        y="count",
        color="category",
        color_discrete_map=STATUS_COLORS,
        category_orders={"category": CATEGORY_ORDER},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Findings")
    severity_filter = st.multiselect(
        "Show severities", CATEGORY_ORDER, default=["error", "critical"]
    )
    problem_lines = [line for line, category, _, _ in classified if category in severity_filter]
    clustered = cluster_errors(problem_lines)

    rows = [{"Count": count, "Message": message} for message, count in clustered.items()]
    st.dataframe(rows, use_container_width=True)
