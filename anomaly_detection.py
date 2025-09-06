# Project 3: Network Traffic Anomaly Detection (Enhanced Visualization)
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import matplotlib.patches as mpatches

# -----------------------------
# Step 1: Load the CSV file
# -----------------------------
data = pd.read_csv("network_traffic.csv")

# Use bytes_sent and bytes_received to detect anomalies
features = data[['bytes_sent', 'bytes_received']]

# -----------------------------
# Step 2: Train Isolation Forest Model
# -----------------------------
model = IsolationForest(contamination=0.2, random_state=42)
model.fit(features)

# Predict anomalies (-1 = anomaly, 1 = normal)
data['anomaly'] = model.predict(features)
data['anomaly_label'] = data['anomaly'].apply(lambda x: 'ANOMALY' if x == -1 else 'NORMAL')

# -----------------------------
# Step 3: Show detected anomalies
# -----------------------------
print("=== Anomaly Detection Results ===")
print(data[['source_ip', 'dest_ip', 'bytes_sent', 'bytes_received', 'anomaly_label']])

# -----------------------------
# Step 4: Enhanced Visualization
# -----------------------------
plt.figure(figsize=(10,7))

# Color and size mapping
colors = data['anomaly_label'].map({'NORMAL':'green', 'ANOMALY':'red'})
sizes = data['anomaly_label'].map({'NORMAL':100, 'ANOMALY':300})  # anomalies bigger

# Scatter plot
plt.scatter(data['bytes_sent'], data['bytes_received'], c=colors, s=sizes, alpha=0.6, edgecolor='k')

# Highlight anomalies with circles and annotate IPs
for i, row in data.iterrows():
    if row['anomaly_label'] == 'ANOMALY':
        # Circle around anomaly
        circle = plt.Circle((row['bytes_sent'], row['bytes_received']), 200, color='red', fill=False, linewidth=2)
        plt.gca().add_patch(circle)
        # Annotate source IP
        plt.text(row['bytes_sent'] + 100, row['bytes_received'] + 100,
                 row['source_ip'], fontsize=9, fontweight='bold', color='red')

# Labels, title, grid
plt.xlabel("Bytes Sent")
plt.ylabel("Bytes Received")
plt.title("Network Traffic Anomaly Detection (Enhanced)")
plt.grid(True, linestyle='--', alpha=0.5)

# Manual legend
normal_patch = mpatches.Patch(color='green', label='Normal')
anomaly_patch = mpatches.Patch(color='red', label='Anomaly')
plt.legend(handles=[normal_patch, anomaly_patch])

plt.show()
