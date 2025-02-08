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
# APPLICATION_TOKEN = os.getenv("APP_TOKEN_LAW")
# BASE_API_URL = "https://api.langflow.astra.datastax.com"
# LANGFLOW_ID = "9013a235-fb25-4adc-9095-e285cb8cee04"
# ENDPOINT = "lawyer-agent"

# docker auth
# BASE_API_URL = "http://localhost:7860"
# FLOW_ID = "844b3bb7-af1c-442c-b233-e61d4850e6d4"
# ENDPOINT = "galgo-ai-simple" # The endpoint name of the flow


# Initialize session state
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the Chat Bot.")
    

else:

    st.info(
        "**Lawyer's Agent**\n\n"
        "- Ask questions regarding your OneDrive documents and get answers from the Lawyer's Agent.\n"
        "- Designed to assist with legal document interpretation, navigation, and guidance.\n"
        "- Here are the documents available to the agent:\n"
        "    - [Executive Employment Agreement](https://1drv.ms/b/c/8573c846dfcb547d/Ebt1k7qZ7c9Gn5_0d9XtjfYBfaIFP3BIasrhJzEuv7wFFA?e=4hZH3n)\n"
        "    - [M&A Terms Sheet](https://1drv.ms/b/c/8573c846dfcb547d/ERdjACQurWVEqPOE5Ubpt-wBeNtAXOxERWg9CfD9V22RnA?e=Tf7hQz)\n"
        "    - [Software Development Agreement](https://1drv.ms/b/c/8573c846dfcb547d/ESb9TgUwfuhNpLgjZDWuzFcB0jcPyxct-kAYsIzkLKAwTQ?e=N4St9A)\n"
        "    - [NDA](https://1drv.ms/b/c/8573c846dfcb547d/ERoEayJb8MRPvtkvw9xIGksB9aiONRZtWXkdUD4KWXPThg?e=FMOa4s)\n"
        "    - [Shareholder's Agreement](https://1drv.ms/b/c/8573c846dfcb547d/Edul37RSvmxOvaEMW_aJjJ4BFBp8XWAosYkMk2pZDXUspQ?e=DrqA3B)\n"
    )



        
    if "messages_law" not in st.session_state:
        st.session_state.messages_law = []

    def run_flow_law(message: str) -> str:
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
    for message in st.session_state.messages_law:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if user_input := st.chat_input("Type your message here..."):
        # Add user input to chat history
        st.session_state.messages_law.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant's response
        with st.chat_message("assistant"):
            placeholder = st.empty()  # Placeholder for the assistant's response
            try:
                with st.spinner("Lawyer Agent is typing..."):
                    response = run_flow_law(user_input)
                placeholder.markdown(response)  # Replace placeholder with response
            except Exception as e:
                placeholder.markdown("There was an error processing your request.")
                st.error(f"Error: {e}")
                response = "There was an error processing your request."

        # Add assistant's response to chat history
        st.session_state.messages_law.append({"role": "assistant", "content": response})
