import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")   # back to login

import streamlit as st
from datetime import datetime
from helpers.firebase_helpers import db, scan_qr_code_ui

st.set_page_config(page_title="Issue Book", layout="centered")

# Back button to dashboard (right aligned)
col1, col2 = st.columns([4, 2])
with col2:
    if st.button("Back"):
        st.session_state.page = "dashboard"  # Optional if you're managing routing manually
        st.switch_page("Home.py")  # Make sure Home.py is your dashboard page

# Utility to reset session inputs
def reset_all():
    for key in ["scanned_book_id", "roll_number"]:
        st.session_state.pop(key, None)

# Main UI for issuing book
st.subheader("📕 Issue Book via QR Code")

if st.button("Rescan QR Code"):
    st.session_state.scanned_book_id = scan_qr_code_ui()

if "scanned_book_id" not in st.session_state:
    st.session_state.scanned_book_id = scan_qr_code_ui()

book_id = st.session_state.get("scanned_book_id")

if book_id:
    st.success(f"✅ Book ID Scanned: **{book_id}**")

    book = db.child("books").child(book_id).get().val()
    if not book:
        st.error("❌ Book not found in the database.")
    elif book.get("status") != "Available":
        st.error(f"⚠️ Book status is '{book.get('status')}'. It is not available for issue.")
    else:
        roll_number = st.text_input("Enter Student Roll Number", key="roll_number")
        confirm_disabled = not roll_number.strip()

        if st.button("Confirm Issue", disabled=confirm_disabled):
            student = db.child("students").child(roll_number).get().val()
            if not student:
                st.error("❌ Student not found.")
            else:
                issued_books = db.child("books").order_by_child("issued_to").equal_to(roll_number).get().val()
                issued_count = sum(1 for b in issued_books.values() if b["status"] == "Issued") if issued_books else 0

                if issued_count >= 2:
                    st.error("⚠️ Student has already issued 2 books. Please return one before issuing a new one.")
                else:
                    db.child("books").child(book_id).update({
                        "status": "Issued",
                        "issued_to": roll_number,
                        "issue_date": datetime.now().strftime("%Y-%m-%d")
                    })

                    db.child("history").push({
                        "book_id": book_id,
                        "title": book.get("title", "Unknown"),
                        "author": book.get("author", "Unknown"),
                        "student_id": roll_number,
                        "student_name": student.get("name", "Unknown"),
                        "action": "Check-Out",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })


                    st.success(
                                f"✅ Book Issued Successfully!\n\n"
                                f"**Book ID**: {book_id}  \n"
                                f"**Title**: {book['title']}  \n"
                                f"**Author**: {book['author']}  \n"
                                f"**Issued To**: {student['name']} ({roll_number})"
                            )
                    reset_all()
else:
    st.info("📷 Please scan a QR code to begin.")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    st.stop()
