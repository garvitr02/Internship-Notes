import os
import time
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
from utils import get_real_time_cpu_usage

def train_model(duration=300):
    model_path = '../data/trained_model.pkl'
    
    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}. Skipping training.")
        return

    print("Starting model training...")
    start_time = time.time()
    cpu_usages = []

    while time.time() - start_time < duration:
        cpu_usage = get_real_time_cpu_usage()
        cpu_usages.append(cpu_usage)
        time.sleep(1)

    model = IsolationForest(contamination=0.1)
    model.fit(np.array(cpu_usages).reshape(-1, 1))

    joblib.dump(model, model_path)
    print("Model trained and saved.")
