import streamlit as st
import pyrebase
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Firebase Configuration
firebaseConfig = {
    'apiKey': st.secrets["FIREBASE_CONFIG"],
    'authDomain': "galgo-ai.firebaseapp.com",
    'projectId': "galgo-ai",
    'databaseURL': "https://galgo-ai-default-rtdb.firebaseio.com/",
    'storageBucket': "galgo-ai.firebasestorage.app",
    'messagingSenderId': "542357248806",
    'appId': "1:542357248806:web:9255cda97962eb458e3fe7",
    'measurementId': "G-47G2RHCNSY"
}

# Firebase Initialization
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Title and Logo
logo_url = "https://raw.githubusercontent.com/ealss101/galgo-ai/main/galgo-ai-rounded.png"
st.markdown(
    f"""
    <div style="display: flex; align-items: left; justify-content: left;">
        <h1 style="margin-right: 10px;">Welcome</h1>
        <img src="{logo_url}" alt="Logo" width="120" style="margin-top: -5px;">
    </div>
    """,
    unsafe_allow_html=True,
)

# Dropdown for Login/Sign-Up
action = st.selectbox("Choose Action", ["Login", "Sign Up"])

# Login Form
if action == "Login":
    st.header("Login")
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        login_button = st.form_submit_button("Login")

        if login_button:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(f"Welcome back, {email}!")
                st.rerun()  # Reload the page to apply the logged-in state
            except Exception as e:
                st.error(f"Login failed: {e}")

# Sign-Up Form
elif action == "Sign Up":
    st.header("Sign Up")
    with st.form("signup_form"):
        email = st.text_input("Email", placeholder="Enter a valid email")
        password = st.text_input("Password", type="password", placeholder="Create your password")
        signup_button = st.form_submit_button("Sign Up")

        if signup_button:
            try:
                # Create a new user
                user = auth.create_user_with_email_and_password(email, password)
                user_id = user['localId']
                db.child("users").child(user_id).set({
                    "email": email
                })
                st.success("Account created successfully!")
                st.info("You can now log in.")
            except Exception as e:
                st.error(f"Sign-Up failed: {e}")

# If the user is logged in
if st.session_state.logged_in:
    st.success(f"Logged in as {st.session_state.user_email}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.rerun()
