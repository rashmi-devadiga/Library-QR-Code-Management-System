import streamlit as st

# ------------------ Auth Check ------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")

import pandas as pd
import time
from helpers.firebase_helpers import db

st.markdown("""
<style>
.table-header {
    font-weight: 600;
    padding: 10px 0;
    border-bottom: 1px solid #e6e6e6;
}
.table-row {
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
}
.remove-link button {
    background: none !important;
    border: none !important;
    padding: 0 !important;
    color: #d11a2a !important;
    text-decoration: underline !important;
    cursor: pointer !important;
}
.remove-link button:hover {
    color: #a00000 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------
col1, col2 = st.columns([2, 1])
with col2:
    if st.button("Back"):
        st.switch_page("Home.py")

# ------------------ Add Student ------------------
st.subheader("Add New Student")

if "student_msg" not in st.session_state:
    st.session_state.student_msg = ""
    st.session_state.student_msg_type = ""

with st.form("add_student_form", clear_on_submit=True):
    student_id = st.text_input("Student ID")
    student_name = st.text_input("Student Name")
    submitted = st.form_submit_button("Add Student")

    if submitted:
        if not student_id or not student_name:
            st.session_state.student_msg = "⚠️ Please fill all fields."
            st.session_state.student_msg_type = "error"
        else:
            if db.child("students").child(student_id).get().val():
                st.session_state.student_msg = f"❌ Student ID '{student_id}' already exists."
                st.session_state.student_msg_type = "error"
            else:
                db.child("students").child(student_id).set({
                    "name": student_name
                })
                st.session_state.student_msg = f"✅ Student '{student_name}' added successfully!"
                st.session_state.student_msg_type = "success"
        st.rerun()

# Status message
if st.session_state.student_msg:
    if st.session_state.student_msg_type == "success":
        st.success(st.session_state.student_msg)
    else:
        st.error(st.session_state.student_msg)

    time.sleep(2)
    st.session_state.student_msg = ""
    st.session_state.student_msg_type = ""
    st.rerun()

# ------------------ Student List (Book-Style UI) ------------------
st.subheader("Student List")

search_query = st.text_input("Search by Student ID or Name")

students = db.child("students").get().val() or {}

filtered_students = {
    sid: student for sid, student in students.items()
    if search_query.lower() in sid.lower()
    or search_query.lower() in student["name"].lower()
} if search_query else students

if filtered_students:
    # ---- Table Header ----
    h1, h2, h3 = st.columns([3, 5, 2])
    h1.markdown("<div class='table-header'>Student ID</div>", unsafe_allow_html=True)
    h2.markdown("<div class='table-header'>Name</div>", unsafe_allow_html=True)
    h3.markdown("<div class='table-header'>Remove</div>", unsafe_allow_html=True)

    # ---- Table Rows ----
    for sid, student in filtered_students.items():
        c1, c2, c3 = st.columns([3, 5, 2])

        c1.markdown(f"<div class='table-row'>{sid}</div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='table-row'>{student['name']}</div>", unsafe_allow_html=True)

        with c3:
            st.markdown("<div class='remove-link'>", unsafe_allow_html=True)
            if st.button("Remove", key=f"remove_{sid}"):
                db.child("students").child(sid).remove()
                st.success(f"Student {sid} removed")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No students found.")

# ------------------ Safety Check ------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    st.stop()
