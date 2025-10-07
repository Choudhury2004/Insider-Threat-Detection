import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Advanced Insider Threat Dashboard",
    page_icon="🤖",
    layout="wide",
)

# --- HELPER FUNCTIONS ---
@st.cache_data
def convert_df_to_csv(df):
    """Converts a DataFrame to a CSV string for downloading."""
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

# --- DETECTION LOGIC ---
def detect_threats_rules(df, thresholds):
    """Rule-based detection with risk scoring."""
    df['Risk_Score'] = 0
    df['Reason'] = ''
    
    # Calculate score based on number of rules broken
    score_increment = 1.0 / len(thresholds)
    
    # Rule 1: Unusual Login Hours
    rule1 = (df['Login_Hour'] >= thresholds['late_hour']) | (df['Login_Hour'] <= thresholds['early_hour'])
    df.loc[rule1, 'Risk_Score'] += score_increment
    df.loc[rule1, 'Reason'] += 'Unusual Login; '

    # Rule 2: Excessive File Access
    rule2 = df['Files_Accessed'] > thresholds['files_accessed']
    df.loc[rule2, 'Risk_Score'] += score_increment
    df.loc[rule2, 'Reason'] += 'Excessive Files; '
    
    # Rule 3: High Email Volume
    rule3 = df['Emails_Sent'] > thresholds['emails_sent']
    df.loc[rule3, 'Risk_Score'] += score_increment
    df.loc[rule3, 'Reason'] += 'High Emails; '
    
    # Rule 4: Multiple USBs
    rule4 = df['USB_Devices_Used'] >= thresholds['usb_devices']
    df.loc[rule4, 'Risk_Score'] += score_increment
    df.loc[rule4, 'Reason'] += 'Multiple USBs; '

    suspicious_df = df[df['Risk_Score'] > 0].copy()
    suspicious_df['Reason'] = suspicious_df['Reason'].str.strip().str.rstrip(';')
    return suspicious_df.sort_values(by='Risk_Score', ascending=False)

def detect_threats_ml(df, contamination=0.1):
    """ML-based anomaly detection using Isolation Forest."""
    features = ['Login_Hour', 'Files_Accessed', 'Emails_Sent', 'USB_devices_Used'.replace('_','')]
    # Quick fix for potential column name mismatch
    if 'USB_devices_Used' not in df.columns and 'USB_Devices_Used' in df.columns:
        features = ['Login_Hour', 'Files_Accessed', 'Emails_Sent', 'USB_Devices_Used']
        
    X = df[features]
    
    model = IsolationForest(contamination=contamination, random_state=42)
    df['Anomaly'] = model.fit_predict(X) # -1 for anomalies, 1 for inliers
    
    # Create a risk score from anomaly scores
    df['Risk_Score'] = model.decision_function(X)
    df['Risk_Score'] = (df['Risk_Score'].min() - df['Risk_Score']) / (df['Risk_Score'].min() - df['Risk_Score'].max())
    
    suspicious_df = df[df['Anomaly'] == -1].copy()
    suspicious_df['Reason'] = 'ML Anomaly Detected'
    return suspicious_df.sort_values(by='Risk_Score', ascending=False)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Threat Detection Engine")
    detection_method = st.radio(
        "Select Detection Method",
        ("Rule-Based Engine", "Machine Learning Engine"),
        help="Choose the engine to analyze the data. ML can find unusual patterns that rules might miss."
    )
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload User Activity CSV", type="csv")
    
    st.markdown("---")
    if detection_method == "Rule-Based Engine":
        st.header("Rule Thresholds")
        thresholds = {
            'late_hour': st.slider("Suspicious Login Hour (Late)", 20, 23, 22),
            'early_hour': st.slider("Suspicious Login Hour (Early)", 0, 6, 5),
            'files_accessed': st.slider("Suspicious File Access", 10, 100, 40),
            'emails_sent': st.slider("Suspicious Email Volume", 10, 100, 50),
            'usb_devices': st.slider("Suspicious USB Count", 1, 5, 2)
        }
    else:
        st.header("ML Model Settings")
        contamination_rate = st.slider(
            "Anomaly Rate (%)", 1, 25, 10,
            help="The percentage of data expected to be anomalous. Adjust based on domain knowledge."
        ) / 100

# --- MAIN PANEL ---
st.title("🤖 Advanced Insider Threat Dashboard")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    if detection_method == "Rule-Based Engine":
        suspicious_df = detect_threats_rules(df, thresholds)
    else:
        suspicious_df = detect_threats_ml(df, contamination_rate)

    # --- METRICS AND CHARTS ---
    st.markdown("### 📊 Dashboard Overview")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("Total Activities Logged", f"{len(df):,}")
        st.metric("Alerts Generated", f"{len(suspicious_df):,}")
    
    with col2:
        if not suspicious_df.empty:
            fig = px.histogram(
                suspicious_df, 
                x='Risk_Score', 
                nbins=20, 
                title='Distribution of Alert Risk Scores',
                color_discrete_sequence=['#ff4d4d']
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No alerts to generate risk distribution chart.")
    
    st.markdown("---")

    # --- ALERTS TABLE ---
    st.markdown("### 🚨 Alert Log")
    if not suspicious_df.empty:
        st.dataframe(style_risk(suspicious_df), use_container_width=True)
        
        csv_download = convert_df_to_csv(suspicious_df)
        st.download_button(
            label="📥 Download Alerts as CSV",
            data=csv_download,
            file_name='suspicious_activity_report.csv',
            mime='text/csv',
        )
    else:
        st.success("✅ No threats detected with the current settings.")
        
else:
    st.warning("Please upload a CSV file to begin analysis.")
    st.image("Insider_Threat.png", caption="System ready for analysis.", use_container_width=True)