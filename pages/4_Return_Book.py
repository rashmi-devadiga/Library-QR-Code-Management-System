import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")   # back to login

import streamlit as st
from datetime import datetime
from helpers.firebase_helpers import db, scan_qr_code_ui

st.set_page_config(page_title="Return Book", layout="centered")

col1, col2 = st.columns([4, 2])
with col2:
    if st.button("Back"):
        st.session_state.page = "dashboard"
        st.switch_page("Home.py") 

# Reset QR state
def reset_scanned():
    st.session_state.pop("scanned_book_id", None)

# Main UI
st.subheader("📗 Return Book via QR Code")

# Rescan functionality
if st.button("Rescan QR Code"):
    st.session_state.scanned_book_id = scan_qr_code_ui()

# If no scanned ID yet, scan once automatically
if "scanned_book_id" not in st.session_state:
    st.session_state.scanned_book_id = scan_qr_code_ui()

book_id = st.session_state.get("scanned_book_id")

if book_id:
    book = db.child("books").child(book_id).get().val()

    if not book:
        st.error("❌ Book not found in the database.")
    elif book.get("status") != "Issued":
        st.error(f"⚠️ Book is not currently marked as 'Issued'. Status: {book.get('status')}")
    else:
        roll_number = book.get("issued_to")
        student = db.child("students").child(roll_number).get().val() if roll_number else None

        if st.button("Confirm Return"):
            # Update book record
            db.child("books").child(book_id).update({
                "status": "Available",
                "issued_to": "",
                "issue_date": ""
            })

            # Log return in history
            db.child("history").push({
                "book_id": book_id,
                "title": book.get("title", "Unknown"),
                "author": book.get("author", "Unknown"),
                "student_id": roll_number,
                "student_name": student.get("name", "Unknown"),
                "action": "Return",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})


            st.success("✅ Book returned successfully!")
            st.markdown(f"""
                        **Book ID:** {book_id}  
                        **Title:** *{book.get('title', 'Unknown')}*  
                        **Returned by:** **{student.get('name', 'Unknown')}** ({roll_number})
                        """)


            reset_scanned()
else:
    st.info("📷 Please scan a book QR code to begin.")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    st.stop()
