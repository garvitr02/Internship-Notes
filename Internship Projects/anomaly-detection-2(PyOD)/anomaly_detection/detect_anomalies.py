import os
import requests
import time
import pandas as pd
from pyod.models.iforest import IForest  # Isolation Forest from PyOD

PROMETHEUS_URL = os.getenv('PROMETHEUS_URL', 'http://prometheus:9090')
PUSHGATEWAY_URL = os.getenv('PUSHGATEWAY_URL', 'http://pushgateway:9091')

def fetch_cpu_usage():
    query = 'rate(node_cpu_seconds_total[1m])'
    response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': query})
    result = response.json()['data']['result']
    data = {}
    for metric in result:
        instance = metric['metric']['instance']
        if instance not in data:
            data[instance] = []
        data[instance].append(float(metric['value'][1]))
    return data

def detect_anomalies(data):
    # Ensure the data is in the correct format
    df = pd.DataFrame.from_dict(data, orient='index').transpose()
    if df.empty:
        print("No data fetched for anomaly detection.")
        return pd.DataFrame()  # Return an empty dataframe if no data

    # Handle any NaN values
    df.fillna(0, inplace=True)
    
    model = IForest(contamination=0.1)
    model.fit(df)
    df['anomaly'] = model.predict(df)
    anomalies = df[df['anomaly'] == 1]
    return anomalies

def push_anomalies_to_prometheus(anomalies):
    for instance in anomalies.index:
        data = f"anomaly{{instance=\"{instance}\"}} 1\n"
        response = requests.post(f"{PUSHGATEWAY_URL}/metrics/job/anomaly_detection", data=data)
        if response.status_code != 202:
            print(f"Error pushing data to Prometheus: {response.status_code}")

def main():
    while True:
        data = fetch_cpu_usage()
        anomalies = detect_anomalies(data)
        if not anomalies.empty:
            print("Detected anomalies: ", anomalies)
            push_anomalies_to_prometheus(anomalies)
        else:
            print("No anomalies detected.")
        time.sleep(60)

if __name__ == "__main__":
    main()
