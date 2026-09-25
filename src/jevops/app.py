import streamlit as st

from jevops.parser import parse_errors
from jevops.cluster import cluster_errors

st.title("JevOps")

uploaded = st.file_uploader("Upload a log file")

if uploaded:
    lines = uploaded.read().decode().splitlines()
    errors = parse_errors(lines)
    clustered = cluster_errors(errors)

    rows = [{"Count": count, "Message": message} for message, count in clustered.items()]
    st.table(rows)
