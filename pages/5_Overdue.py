import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")   # back to login

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from helpers.firebase_helpers import db

st.set_page_config(page_title="Overdue Books", layout="wide")

col1, col2 = st.columns([4, 2])
with col2:
    if st.button("Back"):
        st.session_state.page = "dashboard"
        st.switch_page("Home.py") 
st.subheader("📅 Overdue Books with Penalty")

# Fetch books data
books = db.child("books").get().val() or {}

overdue_books = []
for book_id, book in books.items():
    if book.get("status") == "Issued":
        issue_date_str = book.get("issue_date")
        try:
            issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d")
            due_date = issue_date + timedelta(days=10)
            if datetime.now() > due_date:
                days_overdue = (datetime.now() - due_date).days
                penalty = days_overdue * 10  # ₹10 per day overdue

                student_id = book.get("issued_to", "Unknown")
                student_name = "Unknown"
                if student_id != "Unknown":
                    student = db.child("students").child(student_id).get().val()
                    if student:
                        student_name = student.get("name", "Unknown")

                overdue_books.append({
                    "Book ID": book_id,
                    "Title": book.get("title", "Unknown"),
                    "Author": book.get("author", "Unknown"),
                    "Issued To (Roll No.)": student_id,
                    "Student Name": student_name,
                    "Issue Date": issue_date.strftime("%Y-%m-%d"),
                    "Days Overdue": days_overdue,
                    "Penalty (₹)": penalty
                })
        except Exception:
            continue


if overdue_books:
    st.dataframe(pd.DataFrame(overdue_books), use_container_width=True)
else:
    st.info("✅ No overdue books at this time.")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    st.stop()
