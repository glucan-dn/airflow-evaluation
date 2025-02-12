# Reusable imports
import time 
import logging

def download_stack_new_version_fn():
    import logging
    import pandas as pd
    from datetime import datetime
    import time 
    import json 
    from pathlib import Path

    AIRFLOW_DATA_DIR = Path('/opt/airflow/data')
    FILE_NAME = 'download_report_from_v2.0.0.json'
    FILE_PATH = AIRFLOW_DATA_DIR / FILE_NAME

    logging.info("Starting download stack...")
    download_data = [
        {"stack": "baseos", "size_mb": 1000, "status": "completed", "time": 180},
        {"stack": "gi", "size_mb": 200, "status": "completed", "time": 60}
    ]
    time.sleep(10)
    df = pd.DataFrame(download_data)
    download_report = {
        'stacks': df['stack'].tolist(),
        'total_size_mb': float(df['size_mb'].sum()),
        'total_time_seconds': int(df['time'].sum()),
        'download_speed_mbs': round(float(df['size_mb'].sum() / df['time'].sum()), 2),
        'status': 'success',
        'details': df.to_dict('records'),
        'timestamp': datetime.now().isoformat()
    }
    logging.info(f"Writing download report to to: {FILE_PATH}")
    with open(FILE_PATH, 'w') as f:
        json.dump(download_report, f, indent=2)

    logging.info(f"Download stack completed:\n"
                f"Total size: {download_report['total_size_mb']}MB\n"
                f"Total time: {download_report['total_time_seconds']}s\n"
                f"Download speed: {download_report['download_speed_mbs']}MB/s")
    
    return download_report

def decide_version_fn(**kwargs):
    # Access version from the DAG run configuration
    version_to_run = kwargs.get('dag_run').conf.get('version', '1.0.0')
    logging.info(f"Workflow started with version: {version_to_run}")
    
    if version_to_run == '1.0.0':
        return 'download_stack_v1.0.0'
    elif version_to_run == '2.0.0':
        return 'download_stack_v2.0.0'
    else:
        return 'unknown_version'
    
