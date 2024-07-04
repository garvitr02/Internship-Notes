import time
import numpy as np
import joblib
from pyod.models.iforest import IForest
from utils import get_real_time_cpu_usage, send_to_grafana

def start_detection():
    print("Starting real-time anomaly detection...")
    model_path = '/usr/src/app/data/trained_model.pkl'
    model = joblib.load(model_path)
    
    while True:
        cpu_usage = get_real_time_cpu_usage()
        X = np.array(cpu_usage).reshape(1, -1)
        anomaly_score = model.decision_function(X)[0]
        is_anomaly = model.predict(X)[0]
        print(f"Anomaly Score: {anomaly_score}, Is Anomaly: {is_anomaly}")

        if is_anomaly:
            send_to_grafana(anomaly_score, is_anomaly)
        
        time.sleep(1)  # Check every second

if __name__ == "__main__":
    start_detection()
