import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# streamlit auth
APPLICATION_TOKEN = st.secrets["APP_TOKEN_RESEARCH"]
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "9013a235-fb25-4adc-9095-e285cb8cee04"
ENDPOINT = "accounting-research" 

# local auth
# APPLICATION_TOKEN = os.getenv("APP_TOKEN_RESEARCH")
# BASE_API_URL = "https://api.langflow.astra.datastax.com"
# LANGFLOW_ID = "9013a235-fb25-4adc-9095-e285cb8cee04"
# ENDPOINT = "accounting-research" 

# docker auth
# BASE_API_URL = "http://localhost:7860"
# FLOW_ID = "844b3bb7-af1c-442c-b233-e61d4850e6d4"
# ENDPOINT = "galgo-ai-simple" # The endpoint name of the flow

# Initialize session state
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the Chat Bot.")
    

else:

    st.info(
        "**Accounting Researcher**\n\n"
        "- Your AI-powered guide for financial accounting research.\n"
        "- Instantly search and retrieve financial accounting papers from your OneDrive.\n"
        "- Get AI-driven insights, summaries, and explanations on complex accounting topics.\n"
    )

    if "messages_research" not in st.session_state:
        st.session_state.messages_research = []

    def run_flow_research(message: str) -> str:
        """
        Sends the user message to the LangFlow API and retrieves the response.
        """
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
        headers = {
            "Authorization": f"Bearer {APPLICATION_TOKEN}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
        }
        
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()

        json_response = response.json()

        try:
            return json_response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
        except KeyError:
            st.error("Error: 'text' key missing in API response. Check API format.")
            return "Error: Unexpected API response format."



    # Display chat messages
    for message in st.session_state.messages_research:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if user_input := st.chat_input("Type your message here..."):
        # Add user input to chat history
        st.session_state.messages_research.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant's response
        with st.chat_message("assistant"):
            placeholder = st.empty()  # Placeholder for the assistant's response
            try:
                with st.spinner("Accounting Researcher is typing..."):
                    response = run_flow_research(user_input)
                placeholder.markdown(response)  # Replace placeholder with response
            except Exception as e:
                placeholder.markdown("There was an error processing your request.")
                st.error(f"Error: {e}")
                response = "There was an error processing your request."

        # Add assistant's response to chat history
        st.session_state.messages_research.append({"role": "assistant", "content": response})
