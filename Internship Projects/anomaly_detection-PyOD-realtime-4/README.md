# Real-Time CPU Anomaly Detection with Grafana

## Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd project_root
    ```

2. **Start Docker containers:**
    ```bash
    docker-compose up -d
    ```

3. **Access Grafana:**
    - Open a browser and go to `http://localhost:3000`
    - Add Prometheus as a data source:
        - Navigate to Configuration > Data Sources > Add data source > Prometheus
        - Set the URL to `http://prometheus:9090`

4. **Create a new dashboard in Grafana:**
    - Add a panel with the following Prometheus query to visualize CPU usage:
        ```prometheus
        rate(node_cpu_seconds_total{job="node", mode="user"}[1m])
        ```
    - Add another panel to visualize anomalies (after implementing anomaly export):
        ```prometheus
        anomaly_metric{job="node"}
        ```

## Generate Anomalies for Testing

To simulate an anomaly in your system, you can artificially increase CPU usage:

```bash
# Use stress-ng to generate CPU load
docker run --rm -it polinux/stress stress --cpu 8 --timeout 60s
