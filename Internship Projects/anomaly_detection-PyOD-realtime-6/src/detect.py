import time
import os
import joblib
import numpy as np
from pyod.models.iforest import IForest
from utils import get_real_time_cpu_usage, send_to_prometheus

def start_detection():
    model_path = '/usr/src/app/data/trained_model.pkl'
    if not os.path.exists(model_path):
        print(f"Model file not found at {model_path}")
        return

    model = joblib.load(model_path)
    print("Starting real-time anomaly detection...")

    while True:
        cpu_usage = get_real_time_cpu_usage()
        cpu_usage = np.array([[cpu_usage]])
        anomaly_score = model.decision_function(cpu_usage)
        is_anomaly = model.predict(cpu_usage)
        
        send_to_prometheus(anomaly_score[0], is_anomaly[0])
        time.sleep(1)

if __name__ == "__main__":
    start_detection()
