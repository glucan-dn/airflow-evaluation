# Top level: Only Airflow and lightweight imports
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta
from airflow_tasks.execution_date_after_self import execution_date_after_self
from airflow_tasks.deployment_tasks_common import pre_deployment_checks_fn, download_stack_fn, finish_download_fn, deploy_stack_fn, run_pre_check_fn

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'cluster_deployment',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

pre_deployment_checks = PythonVirtualenvOperator(
    task_id='pre_deployment_checks',
    python_callable=pre_deployment_checks_fn,
    requirements=['pandas==2.1.4'], 
    system_site_packages=True,
    dag=dag,
)

download_stack = PythonVirtualenvOperator(
    task_id='download_stack',
    python_callable=download_stack_fn,
    requirements=['pandas==2.1.4'],
    system_site_packages=True,
    dag=dag,
)

run_pre_check = PythonVirtualenvOperator(
    task_id='run_pre_check',
    python_callable=run_pre_check_fn,
    requirements=['pandas==2.1.4'],
    system_site_packages=True,
    op_kwargs={
        'pre_deployment_checks_result': '{{ ti.xcom_pull(task_ids="pre_deployment_checks") }}'
    },
    dag=dag,
)

# This sensor will wait for an external signal
# Regular Airflow sensor - no special dependency handling needed
wait_for_tests_to_run = ExternalTaskSensor(
    task_id='wait_for_tests_to_run',
    external_dag_id='run_e2e_tests',  # Name of the workflow we wait for
    external_task_id='tests_finished', # Name of the task we wait for
    allowed_states=['success'],
    execution_date_fn=lambda execution_date, **kwargs: execution_date_after_self(execution_date, dag_id="run_e2e_tests"),  # ✅ Ensures we ignore past runs
    mode='reschedule',  # ✅ Releases worker slot while waiting
    poke_interval=5,  # ✅ Checks every 5 seconds
    timeout=86400,  # ✅ Waits up to 24 hours
    dag=dag,
)

deploy_stack = PythonOperator(
    task_id='deploy_stack',
    python_callable=deploy_stack_fn,
    dag=dag,
)

finish_download = PythonOperator(
    task_id='finish_download',
    python_callable=finish_download_fn,
    dag=dag,
)

# Set task dependencies and order
pre_deployment_checks >> download_stack >> run_pre_check >> wait_for_tests_to_run >> deploy_stack >> finish_download 