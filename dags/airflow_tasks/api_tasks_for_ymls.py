import requests
import logging
import os
import time
import json 
from pathlib import Path

def fetch_universities_fn(**kwargs):
    """
    Makes an HTTP GET request to the specified API endpoint and pushes the response to XCom.
    country param should be given in the DAG run configuration. Default to 'romania'.
    """
    country_from_input_data = kwargs.get('dag_run').conf.get('country', 'romania')
    url = f"http://universities.hipolabs.com/search?country={country_from_input_data}"
    try:
        logging.info(f"Making GET request to {url}")
        # Set the NO_PROXY environment variable
        os.environ['NO_PROXY'] = '*'
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        universities_data = response.json()  # This converts the response to a list/dict
        logging.info(f"Received response: {universities_data}")
        # Push the entire JSON response to XCom
        ti = kwargs['ti']
        ti.xcom_push(key="universities", value=universities_data)
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")
        # Push an empty dict to indicate failure or absence of 'message'
        kwargs['ti'].xcom_push(key='universities', value=[])

    """
    Access version from the DAG run configuration
    Default to '1.0.0'.
    """
    version_to_run = kwargs.get('dag_run').conf.get('version', '1.0.0')
    logging.info(f"Workflow started with version: {version_to_run}")
    
    if version_to_run == '1.0.0':
        return 'save_response_v1'
    elif version_to_run == '2.0.0':
        return 'save_response_v2'
    else:
        return 'save_response_v1'


def save_response_v1_fn(**kwargs):
    country_from_input_data = kwargs.get('dag_run').conf.get('country', 'romania')
    AIRFLOW_DATA_DIR = Path('/opt/airflow/data')
    FILE_NAME = f"{country_from_input_data}_universities.txt"
    FILE_PATH = AIRFLOW_DATA_DIR / FILE_NAME

    ti = kwargs['ti']
    universities_saved_from_last_task = ti.xcom_pull(task_ids='fetch_universities', key='universities')
    logging.info(f"Save API response to: {FILE_PATH}")
    with open(FILE_PATH, 'w') as f:
        json.dump(universities_saved_from_last_task, f, indent=2)

    logging.info(f"Succesfully saved to file.")
    

def save_response_v2_fn(**kwargs):
    country_from_input_data = kwargs.get('dag_run').conf.get('country', 'romania')
    AIRFLOW_DATA_DIR = Path('/opt/airflow/data')
    FILE_NAME = f"{country_from_input_data}_colleges.txt"
    FILE_PATH = AIRFLOW_DATA_DIR / FILE_NAME

    ti = kwargs['ti']
    universities_saved_from_last_task = ti.xcom_pull(task_ids='fetch_universities', key='universities')
    logging.info(f"Save API response to: {FILE_PATH}")
    with open(FILE_PATH, 'w') as f:
        json.dump(universities_saved_from_last_task, f, indent=2)

    logging.info(f"Succesfully saved to file.")


class SimulatedFailure(Exception):
    def __init__(self, message: str, error_code: str, severity: str):
        self.error_code = error_code
        self.severity = severity
        super().__init__(f"{message} (Code: {error_code}, Severity: {severity})")


def failing_task_fn():
    logging.info("Starting failing task...")
    time.sleep(5)   
    raise SimulatedFailure(
        "Task execution timeout",
        "TIMEOUT_001",
        "FATAL"
    )
        