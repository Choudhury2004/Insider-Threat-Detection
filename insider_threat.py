import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Step 1: Load log file ---
log_file = os.path.join("logs", "user_activity.csv")
df = pd.read_csv(log_file)
print("Loaded log data:")
print(df)

# --- Step 2: Encode User_ID ---
le = LabelEncoder()
df['User_ID'] = le.fit_transform(df['User_ID'])

# --- Step 3: Train anomaly detection model ---
X = df[['Login_Hour','Files_Accessed','Emails_Sent','USB_Devices_Used']]
model = IsolationForest(contamination=0.2, random_state=42)
model.fit(X)

# --- Step 4: Predict anomalies ---
df['Anomaly'] = model.predict(X)
df['Anomaly'] = df['Anomaly'].replace({1:'Normal', -1:'Suspicious'})

# --- Step 5: Save alerts ---
alerts_file = os.path.join("alerts", "suspicious_activity.csv")
suspicious = df[df['Anomaly'] == 'Suspicious']
suspicious.to_csv(alerts_file, index=False)
print(f"\nSuspicious activity saved to {alerts_file}")
print(suspicious)

# --- Step 6: Visualize results ---
sns.scatterplot(x='Files_Accessed', y='Emails_Sent', hue='Anomaly', data=df, s=100)
plt.title('Insider Threat Detection Visualization')
plt.show()




