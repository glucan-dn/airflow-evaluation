import os
import glob
from datetime import timedelta
import dagfactory

# Path to YAML configuration file
config_folder = os.path.abspath("/opt/airflow/dags/yamls/")
tasks_folder = os.path.abspath("/opt/airflow/dags/airflow_tasks/")
yaml_files = glob.glob(os.path.join(config_folder, "*.yaml"))

# Load and generate DAGs dynamically from each YAML file
for yaml_file in yaml_files:
    print(f"Processing DAG from: {yaml_file}")
    
    # Ensure the YAML contains absolute paths for `python_callable_file`
    with open(yaml_file, "r") as file:
        yaml_content = file.read().replace("python_callable_file: ", f"python_callable_file: {tasks_folder}/")

    # Temporarily rewrite YAML with absolute paths
    temp_yaml_file = yaml_file + ".tmp"
    with open(temp_yaml_file, "w") as file:
        file.write(yaml_content)

    # Load the modified YAML file into dag-factory
    dag_factory = dagfactory.DagFactory(temp_yaml_file)
    for dag_name, dag_config in dag_factory.config.items():
        if "retry_delay" in dag_config["default_args"]:
            dag_config["default_args"]["retry_delay"] = timedelta(seconds=int(dag_config["default_args"]["retry_delay"]))
    dag_factory.generate_dags(globals())  # Registers DAGs in Airflow

    # Remove the temporary YAML file
    os.remove(temp_yaml_file)