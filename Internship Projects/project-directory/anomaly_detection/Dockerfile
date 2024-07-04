FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY anomaly_detection.py /app/

CMD ["python", "/app/anomaly_detection.py"]
