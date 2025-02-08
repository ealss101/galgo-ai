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
    title="𝐀ll 𝐈n",
    icon=":material/robot:",
)
accounting_research_chat_bot_page = st.Page(
    "views/accounting_research_chat_bot.py",
    title="Accounting Researcher",
    icon=":material/psychology:",
)
law_agent_chat_bot_page = st.Page(
    "views/law_agent_chat_bot.py",
    title="Lawyer's Agent",
    icon=":material/gavel:",
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
        "Galgo AI Features": [chat_bot_page, accounting_research_chat_bot_page, law_agent_chat_bot_page, analytics_page],
        "Info": [about_us_page, instructions_page, support_page],
    }
)


with st.sidebar.expander("**Start a New Chat**", expanded=False):
    
    if st.button("All In", key="new_all_sidebar"):
        st.session_state.messages_simple = []
        st.switch_page("views/chat_bot.py")

    if st.button("Lawyer's Agent", key="new_law_sidebar"):
        st.session_state.messages_law = []
        st.switch_page("views/law_agent_chat_bot.py")

    if st.button("Accounting Researcher", key="new_research_sidebar"):
        st.session_state.messages_research = []
        st.switch_page("views/accounting_research_chat_bot.py")

# --- RUN NAVIGATION ---
pg.run()
