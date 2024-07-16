import os
import time
import joblib
import numpy as np
from utils import get_real_time_cpu_usage, send_to_prometheus

def start_detection():
    model_path = '/usr/src/app/data/trained_model.pkl'
    if not os.path.exists(model_path):
        print("Model not found. Exiting.")
        return
    
    model, scaler = joblib.load(model_path)
    
    while True:
        cpu_usage = get_real_time_cpu_usage()
        X = np.array([[cpu_usage]])
        X_scaled = scaler.transform(X)
        
        anomaly_score = model.decision_function(X_scaled)
        is_anomaly = int(model.predict(X_scaled)[0] == -1)  # Corrected to -1

        send_to_prometheus(anomaly_score[0], is_anomaly)
        
        time.sleep(1)

if __name__ == "__main__":
    start_detection()
