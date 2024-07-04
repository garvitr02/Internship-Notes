FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data

CMD ["python", "src/main.py"]
