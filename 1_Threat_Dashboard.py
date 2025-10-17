import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_utils import get_all_activity_as_df
from navigation import render_sidebar

# Render the custom sidebar
render_sidebar()

st.set_page_config(page_title="Threat Dashboard", page_icon="📊", layout="wide")

# --- ROLE-BASED ACCESS CONTROL ---
if not st.session_state.get('logged_in'):
    st.error("Please log in first to access the dashboard.")
    st.stop()
if st.session_state.get('role') != 'Admin':
    st.error("🔒 You do not have permission to view this page.")
    st.info("This page is for Administrators only.")
    st.stop()

# --- HELPER & DETECTION LOGIC ---
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def style_risk(df):
    """Applies color styling to the DataFrame based on Risk Score."""
    def get_color(score):
        if score > 0.66:
            return 'background-color: #ff4d4d; color: white;' # High Risk - Red
        elif score > 0.33:
            return 'background-color: #ffa500;' # Medium Risk - Orange
        else:
            return 'background-color: #ffe4b2;' # Low Risk - Light Orange
            
    return df.style.applymap(get_color, subset=['Risk_Score'])

def detect_threats_rules(df, thresholds):
    df['Risk_Score'] = 0
    df['Reason'] = ''
    score_increment = 1.0 / len(thresholds)
    rule1 = (df['Login_Hour'] >= thresholds['late_hour']) | (df['Login_Hour'] <= thresholds['early_hour'])
    df.loc[rule1, 'Risk_Score'] += score_increment; df.loc[rule1, 'Reason'] += 'Unusual Login; '
    rule2 = df['Files_Accessed'] > thresholds['files_accessed']
    df.loc[rule2, 'Risk_Score'] += score_increment; df.loc[rule2, 'Reason'] += 'Excessive Files; '
    rule3 = df['Emails_Sent'] > thresholds['emails_sent']
    df.loc[rule3, 'Risk_Score'] += score_increment; df.loc[rule3, 'Reason'] += 'High Emails; '
    rule4 = df['USB_Devices_Used'] >= thresholds['usb_devices']
    df.loc[rule4, 'Risk_Score'] += score_increment; df.loc[rule4, 'Reason'] += 'Multiple USBs; '
    suspicious_df = df[df['Risk_Score'] > 0].copy()
    suspicious_df['Reason'] = suspicious_df['Reason'].str.strip().str.rstrip(';')
    return suspicious_df.sort_values(by='Risk_Score', ascending=False)

def detect_threats_ml(df, contamination=0.1):
    features = ['Login_Hour', 'Files_Accessed', 'Emails_Sent', 'USB_Devices_Used']
    X = df[features]
    model = IsolationForest(contamination=contamination, random_state=42)
    df['Anomaly'] = model.fit_predict(X)
    df['Risk_Score'] = model.decision_function(X)
    df['Risk_Score'] = (df['Risk_Score'].min() - df['Risk_Score']) / (df['Risk_Score'].min() - df['Risk_Score'].max())
    suspicious_df = df[df['Anomaly'] == -1].copy()
    suspicious_df['Reason'] = 'ML Anomaly Detected'
    return suspicious_df.sort_values(by='Risk_Score', ascending=False)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🛡️ Threat Detection Engine")
    detection_method = st.radio("Select Detection Method", ("Rule-Based Engine", "Machine Learning Engine"))
    if detection_method == "Rule-Based Engine":
        thresholds = {
            'late_hour': st.slider("Late Hour", 20, 23, 22), 'early_hour': st.slider("Early Hour", 0, 6, 5),
            'files_accessed': st.slider("File Access", 10, 100, 40), 'emails_sent': st.slider("Email Volume", 10, 100, 50),
            'usb_devices': st.slider("USB Count", 1, 5, 2)
        }
    else:
        contamination_rate = st.slider("Anomaly Rate (%)", 1, 25, 10) / 100

# --- MAIN PANEL ---
st.title("📊 Insider Threat Dashboard")
df = get_all_activity_as_df()

if df.empty:
    st.warning("No activity logged yet. Use the simulation pages to generate data.")
    st.stop()

if detection_method == "Rule-Based Engine":
    suspicious_df = detect_threats_rules(df, thresholds)
else:
    suspicious_df = detect_threats_ml(df, contamination_rate)

st.markdown("### 📈 Dashboard Overview")
col1, col2 = st.columns([1, 1])
with col1:
    st.metric("Total Activities Logged", f"{len(df):,}")
    st.metric("Alerts Generated", f"{len(suspicious_df):,}")
with col2:
    if not suspicious_df.empty:
        fig = px.histogram(suspicious_df, x='Risk_Score', nbins=20, title='Distribution of Alert Risk Scores', color_discrete_sequence=['#ff4d4d'])
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("No alerts to display.")

st.markdown("### 🚨 Alert Log")
if not suspicious_df.empty:
    # New code
# Create a new DataFrame for display that excludes the 'Login_Hour' column
    display_df = suspicious_df.drop(columns=['Login_Hour'])

# Display the styled version of the new DataFrame
    st.dataframe(style_risk(display_df), use_container_width=True)
else:
    st.success("✅ No threats detected with the current settings.")