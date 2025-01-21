import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to use Settings.")
else:
    st.title("Settings")

    st.markdown("Customize your Galgo AI experience below.")

    # --- Section: Account Settings ---
    st.header("Account Settings")
    st.text_input("Update Email Address", placeholder="Enter your new email")
    st.text_input("Update Password", type="password", placeholder="Enter your new password")
    if st.button("Save Account Changes"):
        st.success("Account settings updated successfully!")

    # --- Section: Notification Preferences ---
    st.header("Notification Preferences")
    email_notifications = st.checkbox("Enable Email Notifications", value=True)
    sms_notifications = st.checkbox("Enable SMS Notifications")
    st.radio("Notification Frequency", ["Instant", "Daily Digest", "Weekly Summary"], index=1)

    if st.button("Save Notification Preferences"):
        st.success("Notification preferences saved!")

    # --- Section: Privacy and Security ---
    st.header("Privacy & Security")
    st.checkbox("Two-Factor Authentication (2FA)", value=False)
    st.text_input("Backup Email for Account Recovery", placeholder="Enter your backup email")
    st.button("Enable Two-Factor Authentication")

    st.markdown("**Delete Account**")
    if st.button("Delete Account"):
        st.warning("Are you sure? This action cannot be undone!")

    # --- Section: App Settings ---
    st.header("App Settings")
    theme = st.radio("Theme", ["Light", "Dark"], index=0)
    st.checkbox("Enable Chat History", value=True)
    st.slider("Chat Response Speed", min_value=0.5, max_value=3.0, value=1.0, step=0.1, help="Adjusts how fast the chatbot responds.")
    st.button("Save App Settings")

    # --- Section: Support ---
    st.header("Support")
    st.markdown("""
    - **Need help?** Visit our [FAQ page](#).
    - **Contact us:** Email [support@galgoai.com](mailto:support@galgoai.com).
    """)

    # --- Section: About ---
    st.header("About")
    st.markdown("""
    Galgo AI is committed to enhancing your productivity with intelligent chat solutions.  
    **Version**: 1.0.0  
    **Website**: [www.galgo-ai.com](http://www.galgo-ai.com)
    """)
