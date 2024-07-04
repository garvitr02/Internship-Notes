import time
import requests
import os
import numpy as np

def get_real_time_cpu_usage():
    with open('/proc/stat', 'r') as f:
        lines = f.readlines()
    cpu_usage_lines = [line for line in lines if line.startswith('cpu')]
    cpu_usage = sum(float(line.split()[1]) for line in cpu_usage_lines)
    return cpu_usage

def send_to_grafana(anomaly_score, is_anomaly):
    grafana_url = os.getenv('GRAFANA_URL', 'http://grafana:3000')
    panel_id = os.getenv('GRAFANA_PANEL_ID', '1')
    dashboard_id = os.getenv('GRAFANA_DASHBOARD_ID', '1')

    data = {
        "time": int(time.time() * 1000),
        "tags": ["anomaly"],
        "text": f"Anomaly detected with score {anomaly_score} - {'Anomaly' if is_anomaly else 'Normal'}",
        "panelId": panel_id,
        "dashboardId": dashboard_id
    }

    response = requests.post(f"{grafana_url}/api/annotations", json=data, auth=('admin', 'admin'))
    if response.status_code != 200:
        print("Failed to send annotation to Grafana")
