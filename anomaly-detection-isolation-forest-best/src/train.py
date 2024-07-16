import time
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import os
from utils import get_real_time_cpu_usage

def train_model(duration=14400):  # 4 hours by default
    model_path = '/usr/src/app/data/trained_model.pkl'

    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}. Skipping training.")
        return

    print("Starting model training...")
    
    time.sleep(30)

    end_time = time.time() + duration
    data = []

    while time.time() < end_time:
        cpu_usage = get_real_time_cpu_usage()
        data.append(cpu_usage)
        time.sleep(1)

    X = np.array(data).reshape(-1, 1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(contamination=0.05, n_estimators=100, max_samples='auto', random_state=42)
    model.fit(X_scaled)

    joblib.dump((model, scaler), model_path)
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()
