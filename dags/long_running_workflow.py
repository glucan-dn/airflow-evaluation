from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="long_running_workflow",
    default_args=default_args,
    schedule_interval=None,  # Manually triggered
    catchup=False,
) as dag:

    long_task = BashOperator(
        task_id="long_running_task",
        bash_command="sleep 180",  # Sleep for 10 minutes (600 seconds)
    )