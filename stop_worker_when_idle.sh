#!/bin/bash

WORKER_NAME="airflow-worker-1-1"  # Change this to the worker you want to stop
MAX_RETRIES=10  # Number of times to check
SLEEP_TIME=3  # Seconds between checks

echo "Checking if $WORKER_NAME is idle before stopping..."

for ((i=1; i<=MAX_RETRIES; i++)); do
    RUNNING_TASKS=$(docker exec "$WORKER_NAME" celery -A airflow.executors.celery_executor.app inspect active 2>/dev/null)

    if [[ -z "$RUNNING_TASKS" ]]; then
        echo "✅ No active tasks. Stopping $WORKER_NAME..."
        docker stop "$WORKER_NAME"
        exit 0
    else
        echo "⏳ Worker is still running tasks. Retry $i/$MAX_RETRIES..."
        sleep "$SLEEP_TIME"
    fi
done

echo "❌ Worker is still busy after $MAX_RETRIES retries. Not stopping."
exit 1