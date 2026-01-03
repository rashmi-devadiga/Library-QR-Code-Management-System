import streamlit as st
import pyrebase
from firebase_config import firebase_config

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Library Management System",
    layout="wide"
)

st.markdown(
    """
    <style>
    /* Remove horizontal lines in sidebar */
    section[data-testid="stSidebar"] hr {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HIDE SIDEBAR BEFORE LOGIN ----------------
if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- FIREBASE INIT ----------------
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

def login_page():
    st.markdown('<h2 style="text-align:center;">Login</h2>', unsafe_allow_html=True)
    
    # Inject CSS for button color
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #C8A2C8;  /* light purple */
            color: white;
            height: 40px;
            width: 100%;
            border-radius: 8px;
            font-size: 16px;
        }
        div.stButton > button:hover {
            background-color: #B07FB7;
        }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if not email or not password:
                st.warning("Please enter email and password")
            else:
                try:
                    # Try to log in
                    user = auth.sign_in_with_email_and_password(email, password)
                    
                    # If login succeeds, set session state and show success
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.success("✅ Successfully logged in")
                    st.rerun()
                except Exception as e:
                    st.error("❌ Invalid email or password")

def sidebar_logout():
    with st.sidebar:
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

# ---------------- DASHBOARD PAGE ----------------
def dashboard_page():
    st.markdown(
        """
        <style>
        /* Background gradient */
        .stApp {
            background: linear-gradient(to right, #e0f7fa, #ffffff);
        }

        /* Center title */
        .dashboard-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            color: #0d47a1;
            margin-bottom: 30px;
        }

        /* Metric cards */
        .card {
            background: #ffffff;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }

        .card-title {
            font-size: 1.2rem;
            color: #555;
            margin-bottom: 5px;
        }

        .card-value {
            font-size: 2rem;
            font-weight: bold;
            color: #0d47a1;
        }

        
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="dashboard-title">Library Management System</div>', unsafe_allow_html=True)

    books = db.child("books").get().val() or {}
    students = db.child("students").get().val() or {}

    total_books = len(books)
    total_students = len(students)
    available_books = sum(1 for b in books.values() if b.get("status") == "Available")

    # Cards layout
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"""
        <div class="card">
            <div class="card-icon">📚</div>
            <div class="card-title">Total Books</div>
            <div class="card-value">{total_books}</div>
        </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
        <div class="card">
            <div class="card-icon">👨‍🎓</div>
            <div class="card-title">Total Students</div>
            <div class="card-value">{total_students}</div>
        </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
        <div class="card">
            <div class="card-icon">✅</div>
            <div class="card-title">Available Books</div>
            <div class="card-value">{available_books}</div>
        </div>
    """, unsafe_allow_html=True)
    
# ---------------- ROUTER ----------------
if not st.session_state.logged_in:
    login_page()
else:
    sidebar_logout()
    dashboard_page()
