from train import train_model
from detect import start_detection

def main():
    train_duration = 300  # 5 minutes
    train_model(duration=train_duration)
    start_detection()

if __name__ == "__main__":
    main()
