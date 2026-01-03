import streamlit as st
import pandas as pd
import io
from helpers.firebase_helpers import db

# AUTH GUARD
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")

st.set_page_config(page_title="Transaction History", layout="wide")

# ---------------- VIEW STATE ----------------
if "txn_view" not in st.session_state:
    st.session_state.txn_view = "All"

# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([6, 1, 1])

with col3:
    with st.popover("⋮"):
        if st.button("Checkout List", use_container_width=True):
            st.session_state.txn_view = "Check-Out"
            st.rerun()

        if st.button("Return List", use_container_width=True):
            st.session_state.txn_view = "Return"
            st.rerun()


        if st.button("Download CSV", use_container_width=True):
            st.session_state.download_csv = True

        if st.button("Clear History", use_container_width=True):
            db.child("history").remove()
            st.success("✅ Transaction history cleared")
            st.stop()

with col2:
    if st.button("Back"):
        st.switch_page("Home.py")

# ---------------- TITLE ----------------
st.subheader("📖 Transaction History")

# ---------------- LOAD DATA ----------------
history = db.child("history").get().val() or {}

if not history:
    st.info("No transactions found.")
    st.stop()

# FULL DATA (for CSV)
df_all = pd.DataFrame(history.values())

# Ensure columns exist
for col in ["title", "author", "student_name", "student_id"]:
    if col not in df_all.columns:
        df_all[col] = ""

df_all = df_all.sort_values("timestamp", ascending=False)

# COPY for VIEW
df_view = df_all.copy()

# ---------------- SEARCH ----------------
search = st.text_input("Search (Book / Student / ID)").lower()

if search:
    df_view = df_view[
        df_view.astype(str)
        .apply(lambda row: row.str.lower().str.contains(search).any(), axis=1)
    ]

# ---------------- FILTER VIEW ----------------
if st.session_state.txn_view == "Check-Out":
    df_view = df_view[df_view["action"] == "Check-Out"]

elif st.session_state.txn_view == "Return":
    df_view = df_view[df_view["action"] == "Return"]

# ---------------- CSV DOWNLOAD (ALL HISTORY) ----------------
if st.session_state.get("download_csv", False):
    csv_buffer = io.StringIO()
    df_all.to_csv(csv_buffer, index=False)  # ✅ ALWAYS FULL HISTORY

    st.download_button(
        "📥 Download Transaction CSV",
        data=csv_buffer.getvalue(),
        file_name="transaction_history.csv",
        mime="text/csv"
    )

    st.session_state.download_csv = False

# ---------------- DISPLAY TABLE ----------------
display_cols = [
    "timestamp",
    "action",
    "book_id",
    "title",
    "author",
    "student_name",
    "student_id",
]

st.dataframe(df_view[display_cols], use_container_width=True)
