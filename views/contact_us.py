import streamlit as st

st.title("Contact Us")

st.markdown("""
We’d love to hear from you! If you have any questions, concerns, or feedback, feel free to get in touch with us using the information below.
""")

st.subheader("Email Us")
st.write("You can reach us via email at [support@galgoai.com](mailto:support@galgoai.com).")

st.subheader("Call Us")
st.write("Our support team is available Monday to Friday, 9 AM to 5 PM (CST): **+1 (123) 456-7890**.")

st.subheader("Chat with Us")
st.write("Use our in-app chatbot to get immediate assistance.")

st.subheader("Address")
st.write("""
Galgo AI Headquarters  
1234 Innovation Lane  
Austin, TX 78701  
United States
""")

st.markdown("""
---
If you prefer, fill out the contact form below, and we’ll get back to you as soon as possible.
""")

# Contact form
with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Thank you for reaching out! We'll respond to your inquiry soon.")
