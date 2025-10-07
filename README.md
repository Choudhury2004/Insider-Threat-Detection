# Insider-Threat-Detection
An intelligent system designed to detect and mitigate insider threats within an organization by analyzing user behavior and identifying anomalous activities in real-time.

Insider threats, whether malicious or unintentional, pose a significant risk to organizational security. 
This system leverages machine learning to create baselines of normal user behavior and detects deviations that could indicate a threat. By monitoring activities across endpoints, networks, and applications, it provides security teams with actionable alerts and insights to investigate and respond swiftly.
Features:
1. User Behavior Analytics
2. Anomaly Detection
3. Real-time Alerting
4. Dynamic Risk Scoring

Technology used:
1. Streamlit - Used to build and deploy the interactive web dashboard.
2. Pandas - For high-performance data manipulation, analysis, and reading input data.
3. Scikit-learn - For implementing the IsolationForest machine learning model for anomaly detection.
4. Plotly Express - To create rich, interactive charts and visualizations within the dashboard.
5. Matplotlib & Seaborn - For generating static plots during the analysis and model development phase.

insider-threat-detection/ |— data/ |— raw/ # original user activity logs |— processed/ # cleaned & encoded data for modeling |— models/ |— artifacts/ # saved IsolationForest models & encoders |— reports/ # generated alert CSVs & visualizations |— src/ |— app.py # main Streamlit dashboard application |— engine.py # core detection logic (rules & ML) |— train.py # standalone model training & evaluation |— utils.py # helpers, styling, & config |— tests/ # unit tests for the detection engine |— notebooks/ # EDA & model experiments |— requirements.txt # Python dependencies |— config.yaml # rule thresholds & model parameters |— Dockerfile # containerization |— README.md # this file
