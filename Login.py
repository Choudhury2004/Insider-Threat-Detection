import streamlit as st
from auth import verify_user
from db_utils import log_login

st.set_page_config(
    page_title="Insider Threat System - Login",
    page_icon="🤖",
    layout="centered",
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'role' not in st.session_state:
    st.session_state['role'] = ""

st.title("🛡️ Insider Threat Detection System")
st.markdown("Please log in or visit the Sign Up page to create an account.")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        user_role = verify_user(username, password) # Function now returns the role or None
        if user_role:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['role'] = user_role # Store the role
            
            log_login(username) 
            
            st.success("Login successful! Redirecting...")
            st.switch_page("pages/1_Threat_Dashboard.py")
        else:
            st.error("Incorrect username or password.")

st.sidebar.info("New user? Go to the Sign Up page.")