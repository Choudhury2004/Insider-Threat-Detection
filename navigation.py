import streamlit as st

def render_sidebar():
    """Renders the custom sidebar navigation based on the user's role."""
    
    user_role = st.session_state.get('role', "")

    st.sidebar.title("NAVIGATION")

    # The main page is referenced by its filename
    st.sidebar.page_link("Login.py", label="LOGIN")
    
    # Pages in the 'pages' directory need the 'pages/' prefix
    st.sidebar.page_link("pages/2_Sign_Up.py", label="SIGN UP")
    
    if st.session_state.get('logged_in'):
        st.sidebar.markdown("---")
        st.sidebar.page_link("pages/3_Email_Client.py", label="EMAIL CLIENT")
        st.sidebar.page_link("pages/4_File_Explorer.py", label="FILE EXPLORER")

        if user_role == 'Admin':
            st.sidebar.markdown("---")
            # This path must exactly match the file in your pages folder
            # Change the path to the correct filename
            st.sidebar.page_link("pages/1_Threat_Dashboard.py", label="THREAT DASHBOARD")

        st.sidebar.markdown("---")
        username = st.session_state.get('username', '')
        st.sidebar.success(f"Logged in as **{username}** ({user_role})")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.session_state['role'] = ''
            st.switch_page("Login.py")