import streamlit as st
import sys
import os

# This adds the main project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now the imports for your custom modules will work
from db_utils import log_activity
from navigation import render_sidebar
from datetime import datetime

render_sidebar()

st.set_page_config(page_title="Email Client", page_icon="✉️")

# --- AUTHENTICATION CHECK ---
if not st.session_state.get('logged_in'):
    st.error("Please log in first.")
    st.stop()

st.title("✉️ Secure Mail Client")
username = st.session_state['username']
st.info(f"You are logged in as **{username}**. Actions here will be logged.")

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Folders")
    st.button("📥 Inbox", use_container_width=True)
    st.button("📤 Sent", use_container_width=True)
    st.button("🗑️ Trash", use_container_width=True)

with col2:
    st.subheader("Compose New Email")
    with st.form("email_form", clear_on_submit=True):
        to_address = st.text_input("To:", "external.contact@example.com")
        subject = st.text_input("Subject:", "Project confidential data")
        body = st.text_area("Body:", "Here is the data you requested.", height=150)
        
        submitted = st.form_submit_button("Send Email")
        if submitted:
            current_hour = datetime.now().hour
            log_activity(username, current_hour, 0, 1, 0)
            st.success(f"Email to {to_address} sent and activity logged.")
            st.rerun()

st.markdown("---")
st.subheader("🔥 High-Risk Simulation")
if st.button("Send 50 Emails to External Address"):
    current_hour = datetime.now().hour
    for _ in range(50):
        log_activity(username, current_hour, 0, 1, 0)
    st.warning("Logged sending 50 separate emails. This should trigger an alert.")
    st.rerun()