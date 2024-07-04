import time
import numpy as np
import joblib
from pyod.models.iforest import IForest
from utils import get_real_time_cpu_usage

def train_model(duration=300):
    print("Starting model training...")
    end_time = time.time() + duration
    data = []

    while time.time() < end_time:
        cpu_usage = get_real_time_cpu_usage()
        data.append(cpu_usage)
        time.sleep(1)  # Collect data every second

    X = np.array(data).reshape(-1, 1)
    model = IForest()
    model.fit(X)
    
    # Save the model
    joblib.dump(model, '/usr/src/app/data/trained_model.pkl')
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()
