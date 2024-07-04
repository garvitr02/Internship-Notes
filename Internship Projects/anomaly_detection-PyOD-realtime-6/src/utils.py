import requests
import os
import time
from prometheus_api_client import PrometheusConnect

def get_real_time_cpu_usage():
    prom_url = os.getenv('PROMETHEUS_URL', 'http://prometheus:9090')
    prom = PrometheusConnect(url=prom_url, disable_ssl=True)
    cpu_query = 'sum(rate(node_cpu_seconds_total{mode!="idle"}[1m]))'
    
    try:
        result = prom.custom_query(query=cpu_query)
        if result:
            return float(result[0]['value'][1])
        return 0.0
    except Exception as e:
        print(f"Error querying Prometheus: {e}")
        return 0.0

def send_to_prometheus(anomaly_score, is_anomaly):
    prometheus_pushgateway_url = os.getenv('PROMETHEUS_PUSHGATEWAY_URL', 'http://pushgateway:9091')
    job = "anomaly_detection"
    instance = "instance1"

    data = f"""
    # HELP cpu_anomaly_detection_score Anomaly detection score for CPU usage
    # TYPE cpu_anomaly_detection_score gauge
    cpu_anomaly_detection_score{{job="{job}", instance="{instance}"}} {anomaly_score}
    
    # HELP cpu_anomaly_detection_is_anomaly Anomaly detection flag for CPU usage
    # TYPE cpu_anomaly_detection_is_anomaly gauge
    cpu_anomaly_detection_is_anomaly{{job="{job}", instance="{instance}"}} {is_anomaly}
    """

    response = requests.post(f"{prometheus_pushgateway_url}/metrics/job/{job}/instance/{instance}", data=data)
    if response.status_code != 202:
        print("Failed to send metrics to Prometheus")
