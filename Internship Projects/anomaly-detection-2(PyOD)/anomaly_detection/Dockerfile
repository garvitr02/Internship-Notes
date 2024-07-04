FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY detect_anomalies.py detect_anomalies.py

CMD ["python", "detect_anomalies.py"]
