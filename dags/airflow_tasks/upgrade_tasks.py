def group_by_city_fn():
    import logging
    import pandas as pd

    logging.info("Executing task_1...")

    # Test data
    test_data = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Alice", "age": 25, "city": "London"},
        {"name": "Bob", "age": 35, "city": "Paris"}
    ]

    df = pd.DataFrame(test_data)
    result = df.groupby('city').agg({'age': 'mean'}).round(2)
    json_data = result.to_json()

    logging.info(f"Task 1 result:\n{result}")

    return json_data 


def read_from_xcom_fn(xcom_data):
    import logging
    import pandas as pd
    from io import StringIO

    logging.info("Executing task_2...")

    if not xcom_data:
        logging.error("No data received from task_1!")
        return

    # Load JSON into DataFrame
    previous_results = pd.read_json(StringIO(xcom_data))
    logging.info(f"Previous results from task_1:\n{previous_results}")


    # New test data
    test_data = [
        {"name": "Sarah", "age": 28, "city": "London"},
        {"name": "Mike", "age": 32, "city": "Paris"}
    ]

    df = pd.DataFrame(test_data)
    result = df.groupby('city').agg({'age': 'mean'}).round(2)

    logging.info(f"Task 2 results:\n{result}")


def resume_task():
    print("Resuming the workflow...")

def task_added_in_newer_version_fn():
    print("This task was added in a newer version...")
    print("Task from newer version ran successfully...")


def final_task():
    print("Completing the workflow...")
    
    
def waiting_task():
    logging.info("Waiting for external signal")
    # This task will wait for an external signal
    # The actual wait is handled by the ExternalTaskSensor

def resume_task():
    logging.info("Resuming after external signal")
    # Task logic after receiving the signal

def final_task():
    logging.info("Completing workflow")

