import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# streamlit auth
APPLICATION_TOKEN = st.secrets["APP_TOKEN_SIMPLE"]
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "9013a235-fb25-4adc-9095-e285cb8cee04"
ENDPOINT = "galgo-ai-simple"

# local auth
# APPLICATION_TOKEN = os.getenv("APP_TOKEN_SIMPLE")
# BASE_API_URL = "https://api.langflow.astra.datastax.com"
# LANGFLOW_ID = "9013a235-fb25-4adc-9095-e285cb8cee04"
# ENDPOINT = "galgo-ai-simple"

# docker auth
# BASE_API_URL = "http://localhost:7860"
# FLOW_ID = "844b3bb7-af1c-442c-b233-e61d4850e6d4"
# ENDPOINT = "galgo-ai-simple" # The endpoint name of the flow

# Initialize session state
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the Chat Bot.")
else:

    st.info(
        "**All In Agent**\n\n"
        "- Go *all in* with your personal communication & knowledge assistant\n"
        "- Tools included: Gmail, Google Calendar, Google Drive, OneDrive, Yahoo Finance, Wikipedia, Reddit, Github.\n"
    )
        
    if "messages_simple" not in st.session_state:
        st.session_state.messages_simple = []


    def run_flow_simple(message: str) -> str:
        """
        Sends the user message to the LangFlow API and retrieves the response.
        """
        # normal auth
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
        headers = {
            "Authorization": f"Bearer {APPLICATION_TOKEN}",
            "Content-Type": "application/json",
        }

        # docker auth
        # api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT}"
        # headers = None
        
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
        }
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["outputs"][0]["outputs"][0]["results"]["text"]["text"]

    # Display chat messages
    for message in st.session_state.messages_simple:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if user_input := st.chat_input("Type your message here..."):
        # Add user input to chat history
        st.session_state.messages_simple.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant's response
        with st.chat_message("assistant"):
            placeholder = st.empty()  # Placeholder for the assistant's response
            try:
                with st.spinner("Galgo AI is typing..."):
                    response = run_flow_simple(user_input)
                placeholder.markdown(response)  # Replace placeholder with response
            except Exception as e:
                placeholder.markdown("There was an error processing your request.")
                st.error(f"Error: {e}")
                response = "There was an error processing your request."

        # Add assistant's response to chat history
        st.session_state.messages_simple.append({"role": "assistant", "content": response})
