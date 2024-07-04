import time
import numpy as np
import joblib
from pyod.models.iforest import IForest
import os
from utils import get_real_time_cpu_usage

def train_model(duration=300):
    model_path = '/usr/src/app/data/trained_model.pkl'

    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}. Skipping training.")
        return

    print("Starting model training...")
    
    # Add delay to ensure Prometheus has data
    time.sleep(30)

    end_time = time.time() + duration
    data = []

    while time.time() < end_time:
        cpu_usage = get_real_time_cpu_usage()
        data.append(cpu_usage)
        time.sleep(1)  # Collect data every second

    X = np.array(data).reshape(-1, 1)
    model = IForest()
    model.fit(X)

    joblib.dump(model, model_path)
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()
