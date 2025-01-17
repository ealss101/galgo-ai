import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pyrebase

load_dotenv()

# Local configuration
# APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
# FIREBASE_CONFIG = os.environ.get("FIREBASE_CONFIG")

APPLICATION_TOKEN = st.secrets["APP_TOKEN"]
FIREBASE_CONFIG = st.secrets["FIREBASE_CONFIG"]

# Firebase Configuration
firebaseConfig = {
    'apiKey': FIREBASE_CONFIG,
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

# Function to Run LangFlow Flow
def run_flow(message: str) -> str:
    BASE_API_URL = "https://api.langflow.astra.datastax.com"
    LANGFLOW_ID = "9013a235-fb25-4adc-9095-e285cb8cee04"
    ENDPOINT = "galgo-ai"

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()["outputs"][0]["outputs"][0]["results"]["text"]["text"]

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Stores the conversation history
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Home"  # Default tab is Home
if "email" not in st.session_state:
    st.session_state["email"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""

# Sidebar Login/Sign-Up
logo_url = "https://raw.githubusercontent.com/ealss101/galgo-ai/main/galgo-ai-rounded.png"
st.sidebar.image(logo_url, width=200)
st.sidebar.title("Menu")
choice = st.sidebar.selectbox("Login/Sign Up", ["Login", "Sign Up"])

if choice == "Login":
    with st.sidebar.form("login_form"):
        email = st.text_input("Enter email address", value=st.session_state["email"], key="email_input_form")
        password = st.text_input("Enter password", type="password", value=st.session_state["password"], key="password_input_form")
        login_button = st.form_submit_button("Login")

        if login_button:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email
                st.success(f"Welcome back, {email}!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")

# Sign-Up Functionality
if choice == "Sign Up":
    with st.sidebar.form("signup_form"):
        email = st.text_input("Enter a valid email", value="")
        password = st.text_input("Create your password", value="")
        signup_button = st.form_submit_button("Sign Up")
    
        if signup_button:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success("Your account was created successfully!")
                st.balloons()
                user = auth.sign_in_with_email_and_password(email, password)
                db.child(user["localId"]).child("username").set(email)
                db.child(user["localId"]).child("email").set(email)
                st.info("You can now log in.")
            except Exception as e:
                st.error(f"Error: {e}")

# Main Interface with Tabs
if st.session_state["logged_in"]:
    st.title("Galgo AI")

    # Create Tabs
    tabs = st.tabs(["Home", "Chat", "Settings"])

    # Home Tab
    with tabs[0]:
        st.markdown("""
        ### Welcome to Galgo AI!

        Galgo AI is your smart assistant, capable of:
        - Answering your questions with state-of-the-art AI.
        - Integrating RAG to your software and accounts.
        - Using tools such as Yahoo Finance, Wikipedia, Tavily and more.
        - Scraping the web for information.        

        Start chatting in the **Chat** tab or customize your experience in the **Settings** tab.
                    
        Bugs we are working on:
        - Redirection to "Home" tab after first chat output of the session
        - Page refresh causing forced log out
        """)

    # Chat Tab
    with tabs[1]:
        if st.session_state["active_tab"] != "Chat":
            st.session_state["active_tab"] = "Chat"

        # Display conversation history
        chat_container = st.container()
        with chat_container:
            for entry in st.session_state["messages"]:
                if entry["type"] == "user":
                    st.markdown(f"**You:** {entry['content']}")
                else:
                    st.markdown(f"**Galgo:** {entry['content']}")

        # Define function to handle user input
        def handle_user_input():
            user_input = st.session_state["new_input"]
            if user_input.strip():
                # Add user message to history
                st.session_state["messages"].append({"type": "user", "content": user_input})

                # Fetch AI response
                try:
                    with st.spinner("Galgo AI is typing..."):
                        ai_response = run_flow(user_input)
                    st.session_state["messages"].append({"type": "ai", "content": ai_response})
                except Exception as e:
                    st.error(f"Error: {e}")

                # Clear the input box
                st.session_state["new_input"] = ""

        # User input with on_change for Enter key
        st.text_input(
            "Message Galgo:",
            key="new_input",
            on_change=handle_user_input
        )

        # Scrollable chat history
        st.markdown(
            """
            <style>
            [data-testid="stVerticalBlock"] {
                max-height: 800px;
                overflow-y: auto;
            }
            </style>
            """, unsafe_allow_html=True
        )

    # Settings Tab
    with tabs[2]:
        if st.session_state["active_tab"] != "Settings":
            st.session_state["active_tab"] = "Settings"
        st.markdown(f"Logged in as: **{st.session_state['user_email']}**")

        if st.button("Logout", key="settings_logout_button"):
            st.session_state["logged_in"] = False
            st.session_state["email"] = None
            st.session_state["password"] = None
            st.session_state["messages"] = []
            st.rerun()
