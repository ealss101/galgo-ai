import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pyrebase
from google.cloud import storage


load_dotenv()

# local configuration
# APPLICATION_TOKEN = os.environ.get("APP_TOKEN")  
# FIREBASE_CONFIG = os.environ.get("FIREBASE_CONFIG")

# for streamlit secrets
FIREBASE_CONFIG = st.secrets["FIREBASE_CONFIG"]
APPLICATION_TOKEN = st.secrets["APP_TOKEN"]

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "9013a235-fb25-4adc-9095-e285cb8cee04"
ENDPOINT = "galgo-ai"
firebaseConfig={
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
def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
        "Authorization": "Bearer " + APPLICATION_TOKEN,
        "Content-Type": "application/json",
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

logo_url = "https://raw.githubusercontent.com/ealss101/galgo-ai/main/galgo-ai-rounded.png"
st.sidebar.image(logo_url, width=200)

# Sidebar menu
st.sidebar.title("Menu")
choice = st.sidebar.selectbox("Login/Sign Up", ["Login", "Sign Up"])

# Obtain User Input
email = st.sidebar.text_input("Enter your email address")
password = st.sidebar.text_input("Enter your password", type="password")

# Sign Up Functionality
if choice == "Sign Up":
    username = st.sidebar.text_input("Enter your username", value="Default")
    submit = st.sidebar.button("Create Account")

    if submit:
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("Your account was created successfully!")
            st.balloons()
            
            # Automatically sign in the user after registration
            user = auth.sign_in_with_email_and_password(email, password)
            
            # Save user data in Firebase Database
            db.child(user["localId"]).child("username").set(username)
            db.child(user["localId"]).child("email").set(email)
            st.info("You can now log in.")
        except Exception as e:
            st.error(f"Error: {e}")

# Login Functionality
if choice == "Login":
    login = st.sidebar.button("Login")

    if login:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = email
            st.success(f"Welcome back, {email}!")
        except Exception as e:
            st.error(f"Login failed: {e}")

# After Login
if st.session_state["logged_in"]:
    # Tab Navigation
    tabs = st.tabs(["Home", "Chat", "Settings"])

    # Home Tab
    with tabs[0]:
        st.title("Welcome to Galgo AI!")
        st.write("Use the tabs above to access different features.")

    # Run Flow Tab
    with tabs[1]:
        message = st.text_area("Message", placeholder="Ask anything...")   
        if st.button("Run"):
            if not message.strip():
                st.error("Please enter a message.")
            else:
                try:
                    with st.spinner("Running..."):
                        response = run_flow(message)
                    response_text = response["outputs"][0]["outputs"][0]["results"]["text"]["text"]
                    st.markdown(response_text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # Settings Tab
    with tabs[2]:
        st.title("Settings")
        st.write(f"Logged in as: {st.session_state['user_email']}")
        logout = st.button("Logout")
        if logout:
            st.session_state["logged_in"] = False
            st.session_state["user_email"] = None
            st.rerun()  # Redirect to login/signup page

if __name__ == "__main__":
    st.write("")
