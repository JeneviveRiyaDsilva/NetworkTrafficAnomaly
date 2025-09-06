import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import matplotlib.patches as mpatches

data = pd.read_csv("network_traffic.csv")

features = data[['bytes_sent', 'bytes_received']]

model = IsolationForest(contamination=0.2, random_state=42)
model.fit(features)

data['anomaly'] = model.predict(features)
data['anomaly_label'] = data['anomaly'].apply(lambda x: 'ANOMALY' if x == -1 else 'NORMAL')

print("=== Anomaly Detection Results ===")
print(data[['source_ip', 'dest_ip', 'bytes_sent', 'bytes_received', 'anomaly_label']])

plt.figure(figsize=(10,7))

colors = data['anomaly_label'].map({'NORMAL':'green', 'ANOMALY':'red'})
sizes = data['anomaly_label'].map({'NORMAL':100, 'ANOMALY':300}) 

plt.scatter(data['bytes_sent'], data['bytes_received'], c=colors, s=sizes, alpha=0.6, edgecolor='k')

for i, row in data.iterrows():
    if row['anomaly_label'] == 'ANOMALY':
        
        circle = plt.Circle((row['bytes_sent'], row['bytes_received']), 200, color='red', fill=False, linewidth=2)
        plt.gca().add_patch(circle)
    
        plt.text(row['bytes_sent'] + 100, row['bytes_received'] + 100,
                 row['source_ip'], fontsize=9, fontweight='bold', color='red')

plt.xlabel("Bytes Sent")
plt.ylabel("Bytes Received")
plt.title("Network Traffic Anomaly Detection (Enhanced)")
plt.grid(True, linestyle='--', alpha=0.5)

normal_patch = mpatches.Patch(color='green', label='Normal')
anomaly_patch = mpatches.Patch(color='red', label='Anomaly')
plt.legend(handles=[normal_patch, anomaly_patch])

plt.show()
