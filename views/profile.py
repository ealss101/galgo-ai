import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to view Profile.")
else:

    st.title("My Profile")

    st.markdown("Manage your personal information and view account details.")

    # --- Section: Personal Information ---
    st.header("Personal Information")

    #potentially add profile pic here

    st.text_input("Full Name", value="John Doe", help="Update your name.")
    st.text_input("Email Address", value="johndoe@example.com", help="Your registered email address.")
    st.text_input("Phone Number", value="(123) 456-7890", placeholder="Enter your phone number")

    if st.button("Save Personal Information"):
        st.success("Your personal information has been updated.")

    # --- Section: Account Details ---
    st.header("Account Details")
    st.write("**Account Type:** Free User")
    st.write("**Membership Plan:** Basic (Upgrade to Pro for more features!)")
    st.write("**Date Joined:** January 1, 2023")
    st.write("**Last Login:** Today at 10:00 AM")

    # Upgrade Account Button
    if st.button("Upgrade to Pro"):
        st.info("Upgrade functionality coming soon!")

    # --- Section: Preferences ---
    st.header("Preferences")
    st.checkbox("Receive Email Updates", value=True)
    st.checkbox("Allow Push Notifications", value=False)
    if st.button("Save Preferences"):
        st.success("Your preferences have been saved.")

    # --- Section: Security ---
    st.header("Security")
    st.text_input("Change Password", type="password", placeholder="Enter a new password")
    st.button("Update Password")

    st.markdown("**Two-Factor Authentication (2FA)**")
    enable_2fa = st.checkbox("Enable 2FA", value=False)
    if enable_2fa:
        st.info("2FA setup is not yet implemented.")
    else:
        st.warning("Your account is less secure without 2FA.")

    # --- Section: Activity Log ---
    st.header("Recent Activity")
    activity_log = [
        "Logged in from Chrome on Windows - Today, 9:58 AM",
        "Changed email address - Jan 20, 2025, 2:30 PM",
        "Signed up for the app - Jan 1, 2023, 10:00 AM",
    ]
    st.write("Your recent activity:")
    for log in activity_log:
        st.write(f"- {log}")

    # --- Section: Delete Account ---
    st.header("Delete Account")
    if st.button("Delete Account"):
        st.error("This action is permanent and cannot be undone!")
