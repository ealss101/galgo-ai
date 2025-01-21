import streamlit as st

# --- PAGE SETUP ---
login_page = st.Page(
    "views/login_signup.py",
    title="Login/Sign Up",
    icon=":material/login:",
    default=True,
)
about_us_page = st.Page(
    "views/about_us.py",
    title="About Us",
    icon=":material/info:",
)
chat_bot_page = st.Page(
    "views/chat_bot.py",
    title="Galgo AI",
    icon=":material/robot:",
)
settings_page = st.Page(
    "views/settings.py",
    title="Settings",
    icon=":material/settings:",
)
instructions_page = st.Page(
    "views/instructions.py",
    title="How it Works",
    icon=":material/list:",
)
analytics_page = st.Page(
    "views/dashboard.py",
    title="Dashboard",
    icon=":material/analytics:",
)
support_page = st.Page(
    "views/contact_us.py",
    title="Contact Us",
    icon=":material/contact_support:",
)
terms_page = st.Page(
    "views/terms.py",
    title="Terms & Privacy",
    icon=":material/verified_user:",
)
profile_page = st.Page(
    "views/profile.py",
    title="My Profile",
    icon=":material/account_circle:",
)

# --- NAVIGATION SETUP ---
pg = st.navigation(
    {
        "Account": [login_page, profile_page, settings_page, terms_page],
        "Features": [chat_bot_page, analytics_page],
        "Info": [about_us_page, instructions_page, support_page],
    }
)

# --- RUN NAVIGATION ---
pg.run()
