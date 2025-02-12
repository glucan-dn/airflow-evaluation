# Airflow Docker Deployment Guide

A comprehensive guide for deploying and managing Apache Airflow using Docker Compose. This guide will help you set up, manage, and troubleshoot your Airflow environment.

## Prerequisites

Before you begin, ensure you have:
- Docker Engine
- Docker Compose
- Git (optional)
- At least 4GB RAM available
- Python 3.8 or higher

## 🚀 Quick Start

### Initial Setup

First, let's get everything up and running:

```bash
# Clean up any existing Airflow instances
docker-compose down --volumes --remove-orphans
docker network prune -f
docker container prune -f

# Initialize Airflow
docker-compose up airflow-init

# Start Airflow services
docker-compose up -d

# Scale up to 2 workers (recommended)
docker-compose up -d --scale airflow-worker=2
```

### Accessing the UI

Once everything is running, you can access the Airflow web interface:
- URL: http://localhost:8080
- Default Username: airflow
- Default Password: airflow

## 📝 Examples & Documentation

This repository includes several example workflows. 
Their definition, including extensive Airflow evaluation can be found at: [Airflow Evaluation](https://drivenets.atlassian.net/wiki/spaces/RES/pages/4992696349/Apache+Airflow)


## 🔧 Worker Management

### Viewing Worker Status

Monitor your workers with these commands:

```bash
# List all running workers
docker ps --filter "name=airflow-worker"

# Check specific worker logs
docker logs airflow-dock-airflow-worker-1

# View active tasks on a worker
docker exec -it airflow-dock-airflow-worker-1 celery -A airflow.executors.celery_executor inspect active
```

### Managing Workers

Control your worker instances:

```bash
# Stop a specific worker
docker stop airflow-dock-airflow-worker-1

# Start a specific worker
docker start airflow-dock-airflow-worker-2

# Check Celery worker status
airflow celery worker list

# Make airflow worker stop consuming tasks from the 'default' queue. celery@airflow-worker-fbc98e9fe6bb  is the worker hostname.
airflow  celery -A airflow.providers.celery.executors.celery_executor.app control cancel_consumer -d celery@airflow-worker-fbc98e9fe6bb default

```

## 📊 Service Management

View and manage your Airflow services:

```bash
# List all available services
docker-compose config --services

Expected output:
- airflow-webserver
- airflow-scheduler
- airflow-worker
- airflow-triggerer
- airflow-init
- postgres
- redis
```

## 📁 Project Structure

```
.
├── dags/                 # Your DAG files
├── logs/                 # Airflow logs
├── plugins/              # Custom plugins
├── config/               # Configuration files
├── data/                 # Data directory
├── docker-compose.yaml   # Docker configuration
└── .env                  # Environment variables
```

## 🔍 Troubleshooting

### Common Issues

1. **Worker Not Starting**
   ```bash
   # Check worker logs
   docker logs airflow-dock-airflow-worker-1
   ```

2. **Tasks Stuck in Queue**
   ```bash
   # Check active tasks
   docker exec -it airflow-dock-airflow-worker-1 celery -A airflow.executors.celery_executor inspect active
   ```

3. **Database Connection Issues**
   ```bash
   # Restart services
   docker-compose restart postgres
   docker-compose restart airflow-webserver
   ```

## 🛠 Best Practices

**Scaling**
   - Start with 2 workers
   - Scale based on workload
   - Monitor resource usage


## 📚 Additional Resources

- [Official Airflow Documentation](https://airflow.apache.org/docs/)
- [Drivenets Airflow Evaluation](https://drivenets.atlassian.net/wiki/spaces/RES/pages/4992696349/Apache+Airflow)
- [Celery Documentation](https://docs.celeryproject.org/)
