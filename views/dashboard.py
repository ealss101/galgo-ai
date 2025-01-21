import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to view Dashboard.")
else:
    st.title("Dashboard")

    st.markdown("Gain insights into your usage and performance with Galgo AI.")

    # --- Section: Overview Metrics ---
    st.header("Overview Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Messages Sent", value="1,240", delta="+12%")
    with col2:
        st.metric(label="Total Sessions", value="250", delta="+5%")
    with col3:
        st.metric(label="Average Session Duration", value="15 mins", delta="-3%")

    # --- Section: Usage Trends ---
    st.header("Usage Trends")
    st.markdown("Analyze your message activity over the past week:")

    # Sample Data for the Graph
    data = {
        "Date": pd.date_range(start="2025-01-15", periods=7, freq="D"),
        "Messages Sent": [150, 170, 160, 180, 200, 210, 230],
    }
    df = pd.DataFrame(data)

    # Line Chart
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Messages Sent"], marker="o")
    ax.set_title("Messages Sent Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Messages Sent")
    ax.grid(True)
    st.pyplot(fig)

    # --- Section: User Activity ---
    st.header("User Activity")
    st.markdown("See a breakdown of your activity by feature:")

    activity_data = {
        "Feature": ["Chatbot", "Settings", "Dashboard", "Profile"],
        "Usage Count": [1200, 150, 80, 70],
    }
    activity_df = pd.DataFrame(activity_data)

    # Display Activity Breakdown
    st.dataframe(activity_df)

    # --- Section: Goals ---
    st.header("Your Goals")
    st.markdown("Set and track your goals to maximize productivity.")
    st.slider("Daily Message Goal", min_value=50, max_value=500, value=200, step=10)
    if st.button("Save Goal"):
        st.success("Your goal has been saved!")

    # --- Section: Performance Tips ---
    st.header("Performance Tips")
    st.markdown("""
    Here are some tips to improve your experience:
    - Use shortcuts to quickly interact with the chatbot.
    - Explore advanced settings to personalize responses.
    - Visit the FAQ for tips on maximizing productivity.
    """)
