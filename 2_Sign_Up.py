import streamlit as st
import sys
import os

# This adds the main project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now the imports for your custom modules will work
from auth import add_user
from db_utils import log_login
from navigation import render_sidebar

render_sidebar()

st.set_page_config(page_title="Sign Up", page_icon="📝")

st.title("Create a New Account")

with st.form("signup_form"):
    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")
    is_admin = st.checkbox("Sign up as an Administrator")
    
    submitted = st.form_submit_button("Sign Up")

    if submitted:
        role = "Admin" if is_admin else "User"
        
        if add_user(new_user, new_pass, role):
            st.success("Account created successfully! You are now logged in.")
            
            st.session_state['logged_in'] = True
            st.session_state['username'] = new_user
            st.session_state['role'] = role
            
            log_login(new_user)
            
            st.info("Redirecting you to the main dashboard...")
            st.switch_page("pages/1_Threat_Dashboard.py")
        else:
            st.error("This username is already taken. Please choose another.")