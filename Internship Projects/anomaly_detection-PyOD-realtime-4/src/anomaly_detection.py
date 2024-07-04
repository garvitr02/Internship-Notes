import os
import time
import numpy as np
from prometheus_api_client import PrometheusConnect
from pyod.models.iforest import IForest
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Constants
PROMETHEUS_URL = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')
PUSHGATEWAY_URL = os.getenv('PUSHGATEWAY_URL', 'http://localhost:9091')
INITIAL_TRAINING_PERIOD = 300  # 5 minutes for initial training
ANOMALY_THRESHOLD = 0.05  # Adjust as needed

# Connect to Prometheus
prom = PrometheusConnect(url=PROMETHEUS_URL, disable_ssl=True)

# Define a function to get CPU metrics
def get_cpu_metrics():
    query = 'rate(node_cpu_seconds_total[1m])'
    result = prom.custom_query(query=query)
    return np.array([float(metric['value'][1]) for metric in result])

# Initialize the Isolation Forest model
model = IForest(contamination=ANOMALY_THRESHOLD)

# Initial training period
print("Starting initial training period...")
start_time = time.time()
training_data = []
while time.time() - start_time < INITIAL_TRAINING_PERIOD:
    data = get_cpu_metrics()
    if data.size > 0:
        training_data.append(data)
    time.sleep(10)  # Adjust interval as needed

# Flatten the training data and fit the model
training_data = np.concatenate(training_data).reshape(-1, 1)
model.fit(training_data)
print("Initial training completed.")

# Continuous anomaly detection
print("Starting anomaly detection...")
while True:
    data = get_cpu_metrics()
    if data.size > 0:
        data = data.reshape(-1, 1)
        labels = model.predict(data)
        anomalies = np.where(labels == 1)[0]
        print(f"Anomalies detected at indices: {anomalies}")

        # Push anomalies count to Prometheus Pushgateway
        registry = CollectorRegistry()
        gauge = Gauge('anomaly_metric', 'Anomalies detected', registry=registry)
        gauge.set(len(anomalies))
        push_to_gateway(PUSHGATEWAY_URL, job='anomaly_detection', registry=registry)

    time.sleep(60)  # Run every minute
