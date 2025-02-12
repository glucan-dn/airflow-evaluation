from airflow import DAG
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from datetime import timedelta
from airflow_tasks.multiple_conditions_workflow_tasks import process_sales, process_inventory, process_marketing, unknown_data_type, start_task, decide_branch, end_task

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'multiple_conditions_workflow',
    default_args=default_args,
    description='Workflow with multiple conditional branches, where configuration input is needed.',
    schedule_interval=None,
    catchup=False,
) as dag:

    task_start = PythonOperator(
        task_id='start_task',
        python_callable=start_task,
    )

    branch_decision = BranchPythonOperator(
        task_id='branch_decision',
        python_callable=decide_branch,
    )

    task_process_sales = PythonOperator(
        task_id='process_sales',
        python_callable=process_sales,
    )

    task_process_inventory = PythonOperator(
        task_id='process_inventory',
        python_callable=process_inventory,
    )

    task_process_marketing = PythonOperator(
        task_id='process_marketing',
        python_callable=process_marketing,
    )

    task_unknown = PythonOperator(
        task_id='unknown_data_type',
        python_callable=unknown_data_type,
    )

    join = DummyOperator(
        task_id='join',
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    task_end = PythonOperator(
        task_id='end_task',
        python_callable=end_task,
    )

    # Define Task Dependencies
    task_start >> branch_decision
    branch_decision >> task_process_sales >> join
    branch_decision >> task_process_inventory >> join
    branch_decision >> task_process_marketing >> join
    branch_decision >> task_unknown >> join
    join >> task_end
