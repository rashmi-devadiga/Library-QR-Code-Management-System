import streamlit as st

# AUTH GUARD
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")

import pandas as pd
import time
from datetime import datetime, timedelta
from helpers.firebase_helpers import db, generate_qr_code, get_download_link

# ---------------- VIEW STATE ----------------
if "book_view" not in st.session_state:
    st.session_state.book_view = "Add"

# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([6, 1, 1])

with col3:
    with st.popover("⋮"):
        if st.button("Add Book", use_container_width=True):
            st.session_state.book_view = "Add"
            st.rerun()

        if st.button("Issued Books", use_container_width=True):
            st.session_state.book_view = "Issued"
            st.rerun()

        if st.button("Available Books", use_container_width=True):
            st.session_state.book_view = "Available"
            st.rerun()

with col2:
    if st.button("Back"):
        st.switch_page("Home.py")

# ---------------- DATA ----------------
books = db.child("books").get().val() or {}
students = db.child("students").get().val() or {}

# ================= ADD BOOK VIEW =================
if st.session_state.book_view == "Add":

    st.subheader("Add New Book")

    with st.container(border=True):

        if "book_added" not in st.session_state:
            st.session_state.book_added = False
        if "clear_inputs" not in st.session_state:
            st.session_state.clear_inputs = False

        if st.session_state.clear_inputs:
            st.session_state.book_id = ""
            st.session_state.title = ""
            st.session_state.author = ""
            st.session_state.clear_inputs = False

        book_id = st.text_input("Book ID", key="book_id")
        title = st.text_input("Book Title", key="title")
        author = st.text_input("Author Name", key="author")

        if st.button("Add Book"):
            if book_id and title and author:
                if db.child("books").child(book_id).get().val():
                    st.error(f"❌ Book ID '{book_id}' already exists.")
                else:
                    db.child("books").child(book_id).set({
                        "title": title,
                        "author": author,
                        "status": "Available"
                    })
                    st.session_state.book_added = True
                    st.session_state.clear_inputs = True
                    st.rerun()
            else:
                st.warning("Please fill all fields.")

        if st.session_state.book_added:
            st.success("✅ Book added successfully!")
            time.sleep(1.5)
            st.session_state.book_added = False
            st.rerun()

    # -------- BOOK LIST --------
    st.subheader("📚 Book List")
    search_query = st.text_input("Search by Title or Author").lower()

    filtered_books = {
        b_id: book for b_id, book in books.items()
        if not search_query
        or search_query in book["title"].lower()
        or search_query in book["author"].lower()
    }

    if filtered_books:
        st.dataframe(pd.DataFrame([
            {
                "Book ID": b_id,
                "Title": book["title"],
                "Author": book["author"],
                "Status": book["status"]
            }
            for b_id, book in filtered_books.items()
        ]), use_container_width=True)
    else:
        st.info("No books found.")

    # -------- QR + REMOVE --------
    for b_id, book in filtered_books.items():
        st.markdown("---")
        col1, col2 = st.columns([1, 1])

        with col1:
            qr = generate_qr_code(b_id)
            st.image(qr, width=120)
            st.markdown(get_download_link(qr, f"{b_id}.png"), unsafe_allow_html=True)

        with col2:
            if st.button(f"🗑 Remove {b_id}", key=b_id):
                if book["status"] == "Issued":
                    st.error("Cannot remove issued book.")
                else:
                    db.child("books").child(b_id).remove()
                    st.warning(f"Book {b_id} removed.")
                    st.rerun()

# ================= ISSUED BOOKS VIEW =================
elif st.session_state.book_view == "Issued":

    st.subheader("Issued Books")

    search = st.text_input(
        "🔍 Search by Book ID / Title / Student",
        key="issued_search"
    ).lower()

    issued_rows = []

    for b_id, book in books.items():
        if book.get("status") == "Issued":
            sid = book.get("issued_to", "")
            sname = students.get(sid, {}).get("name", "Unknown")
            issue_date = book.get("issue_date", "Unknown")

            if search and not (
                search in b_id.lower()
                or search in book["title"].lower()
                or search in sname.lower()
            ):
                continue

            try:
                return_date = (
                    datetime.strptime(issue_date, "%Y-%m-%d") + timedelta(days=10)
                ).strftime("%Y-%m-%d")
            except:
                return_date = "Unknown"

            issued_rows.append({
                "Book ID": b_id,
                "Title": book["title"],
                "Issued To": sid,
                "Student Name": sname,
                "Issue Date": issue_date,
                "Return Date": return_date
            })

    if issued_rows:
        st.dataframe(pd.DataFrame(issued_rows), use_container_width=True)
    else:
        st.info("No matching issued books found.")

# ================= AVAILABLE BOOKS VIEW =================
elif st.session_state.book_view == "Available":

    st.subheader("Available Books")

    search = st.text_input(
        "🔍 Search by Book ID / Title / Author",
        key="available_search"
    ).lower()

    available_books = []

    for b_id, book in books.items():
        if book.get("status") == "Available":

            if search and not (
                search in b_id.lower()
                or search in book["title"].lower()
                or search in book["author"].lower()
            ):
                continue

            available_books.append({
                "Book ID": b_id,
                "Title": book["title"],
                "Author": book["author"]
            })

    if available_books:
        st.dataframe(pd.DataFrame(available_books), use_container_width=True)
    else:
        st.info("No matching available books found.")
