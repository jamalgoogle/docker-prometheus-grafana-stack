markdown
# Prometheus Monitoring Stack

A comprehensive monitoring solution using Prometheus, Grafana, Node Exporter, and a custom Flask web application with built-in metrics.

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Configuration Files](#-configuration-files)
- [Running the Stack](#-running-the-stack)
- [Accessing Services](#-accessing-services)
- [Useful PromQL Queries](#-useful-promql-queries)
- [Troubleshooting](#-troubleshooting)
- [Next Steps](#-next-steps)

## 🏗️ Architecture Overview

This project demonstrates a complete monitoring stack with the following components:

- **Prometheus**: Time-series database for metrics collection and storage
- **Grafana**: Visualization platform for creating dashboards
- **Node Exporter**: System resource metrics collector
- **Custom Flask App**: Sample web application with built-in Prometheus metrics
- **Alertmanager**: Handles alerts from Prometheus and routes them

## 📁 Project Structure
prometheus-monitoring/
├── docker-compose.yml # Docker container definitions
├── prometheus.yml # Main Prometheus configuration
├── alert.rules.yml # Alerting rules for Prometheus
├── alertmanager.yml # Alertmanager configuration
├── app.py # Flask web application with metrics
├── requirements.txt # Python dependencies
└── README.md # This documentation

text

## ⚙️ Prerequisites

Before starting, ensure you have installed:

- **Docker** and **Docker Compose**
- **Python 3.7+** (for the Flask application)
- **pip** (Python package manager)

## 📦 Installation & Setup

1. **Clone or create the project directory**:
   ```bash
   mkdir prometheus-monitoring
   cd prometheus-monitoring
Create the configuration files as described in the sections below

Install Python dependencies for the Flask app:

bash
pip install -r requirements.txt
🔧 Configuration Files
1. Docker Compose (docker-compose.yml)
Defines and orchestrates all the monitoring services:

yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alert.rules.yml:/etc/prometheus/alert.rules.yml
    # ... other configuration

  alertmanager:
    image: prom/alertmanager:latest
    ports: ["9093:9093"]
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml

  node-exporter:
    image: prom/node-exporter:latest
    ports: ["9100:9100"]

  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:
2. Prometheus Configuration (prometheus.yml)
Main configuration file defining scrape targets and settings:

yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'web-application'
    static_configs:
      - targets: ['host.docker.internal:8000']
        labels:
          environment: 'production'

rule_files:
  - 'alert.rules.yml'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
3. Alert Rules (alert.rules.yml)
Defines conditions for triggering alerts:

yaml
groups:
- name: example
  rules:
  - alert: HighRequestLatency
    expr: http_request_latency_seconds{endpoint="/"} > 0.5
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "High request latency on homepage"
      description: "Request latency exceeded 0.5 seconds"

  - alert: ServiceDown
    expr: up{job="web-application"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Service is down"
      description: "Web application is not responding"
4. Alertmanager Configuration (alertmanager.yml)
Configures how alerts are handled and routed:

yaml
route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
receivers:
  - name: 'web.hook'
    webhook_configs:
      - url: 'http://127.0.0.1:5001/'
5. Flask Application (app.py)
Sample web application with integrated Prometheus metrics:

python
from flask import Flask
from prometheus_client import Counter, Gauge, generate_latest
import time
import random

app = Flask(__name__)

# Metrics definitions
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', 
                       ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Gauge('http_request_latency_seconds', 'HTTP Request Latency',
                       ['method', 'endpoint'])
ACTIVE_USERS = Gauge('active_users', 'Number of active users')

@app.route('/')
def home():
    start_time = time.time()
    time.sleep(random.uniform(0.1, 1.0))
    latency = time.time() - start_time
    
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    REQUEST_LATENCY.labels(method='GET', endpoint='/').set(latency)
    
    return f'Hello! Load time: {latency:.2f} seconds'

@app.route('/metrics')
def metrics():
    return generate_latest()

# ... other routes and functionality
6. Requirements (requirements.txt)
Python dependencies for the Flask application:

text
Flask==2.3.3
prometheus_client==0.18.0
🚀 Running the Stack
Start the Docker containers:

bash
docker-compose up -d
Run the Flask application:

bash
python app.py
Verify all services are running:

bash
docker-compose ps
🌐 Accessing Services
Prometheus UI: http://localhost:9090

Grafana: http://localhost:3000 (admin/admin)

Node Exporter: http://localhost:9100

Flask Application: http://localhost:8000

Alertmanager: http://localhost:9093

🔍 Useful PromQL Queries
promql
# Request rate per minute
rate(http_requests_total[1m])

# Current request latency
http_request_latency_seconds

# Active users count
active_users

# Memory usage
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes

# CPU usage
rate(node_cpu_seconds_total[1m])

# Service health status
up
🐛 Troubleshooting
Common Issues:
Targets not showing in Prometheus:

bash
docker-compose logs prometheus
curl http://localhost:8000/metrics
Grafana cannot connect to Prometheus:

Verify URL is http://prometheus:9090 in Grafana data source settings

Metrics not appearing:

Check Flask app is running: curl http://localhost:8000

Verify metrics endpoint: curl http://localhost:8000/metrics

Containers not starting:

bash
docker-compose down
docker-compose up -d
🚀 Next Steps
Enhancements to consider:
Add more metrics to the Flask application

Configure additional notification channels in Alertmanager (email, Slack)

Create advanced Grafana dashboards

Add database monitoring (MySQL, PostgreSQL, or MongoDB exporter)

Implement service discovery for dynamic environments

Set up TLS/SSL for secure communications

Configure persistent storage for metrics data

Learning Resources:
Prometheus Official Documentation

Grafana Documentation

Prometheus Client for Python

📊 Example Dashboards
Once Grafana is running, you can import these dashboard IDs:

Node Exporter Full: 1860

Prometheus 2.0 Overview: 3662

Web Application Monitoring: Create custom dashboard using the metrics from the Flask app

🤝 Contributing
To extend this project:

Fork the repository

Create a feature branch

Make your changes

Test thoroughly

Submit a pull request

📄 License
This project is provided as an educational example for learning Prometheus monitoring.

Happy Monitoring! 🎯
