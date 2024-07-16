import os
from train import train_model
from detect import start_detection

def main():
    model_path = '/usr/src/app/data/trained_model.pkl'
    if not os.path.exists(model_path):
        train_duration = int(os.getenv('TRAIN_DURATION', 14400))  # 4 hours
        train_model(duration=train_duration)
    
    start_detection()

if __name__ == "__main__":
    main()
