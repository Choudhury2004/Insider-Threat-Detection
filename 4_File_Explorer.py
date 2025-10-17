import streamlit as st
import sys
import os

# This adds the main project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now the imports for your custom modules will work
from db_utils import log_activity
from navigation import render_sidebar
from datetime import datetime
import random

render_sidebar()

st.set_page_config(page_title="File Explorer", page_icon="📁")

# --- AUTHENTICATION CHECK ---
if not st.session_state.get('logged_in'):
    st.error("Please log in first.")
    st.stop()

st.title("📁 Corporate File Explorer")
username = st.session_state['username']
st.info(f"You are logged in as **{username}**. Actions here will be logged.")

st.subheader("Project Alpha (Confidential)")
files = ["financials_q3.xlsx", "roadmap_2026.docx", "client_database.csv", "source_code.zip"]

for file in files:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"📄 {file}")
    with col2:
        if st.button("Download", key=f"download_{file}"):
            files_accessed = random.randint(1, 5)
            current_hour = datetime.now().hour
            log_activity(username, current_hour, files_accessed, 0, 0)
            st.success(f"'{file}' downloaded. Logged access of {files_accessed} files.")
            st.rerun()
    with col3:
        if st.button("Copy to USB", key=f"usb_{file}"):
            files_accessed = random.randint(1, 5)
            current_hour = datetime.now().hour
            log_activity(username, current_hour, files_accessed, 0, 1)
            st.warning(f"'{file}' copied to USB. High-risk activity logged.")
            st.rerun()

st.markdown("---")
st.subheader("🔥 High-Risk Simulation")
if st.button("Download All Project Files at 3 AM"):
    suspicious_hour = 3
    files_to_log = random.randint(100, 150)
    log_activity(username, suspicious_hour, files_to_log, 0, 0)
    st.warning(f"Simulated mass download of {files_to_log} files at {suspicious_hour}:00.")
    st.rerun()