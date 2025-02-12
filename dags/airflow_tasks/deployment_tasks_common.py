# Reusable imports
import time 


def pre_deployment_checks_fn():
    # Task-level imports
    import logging
    import pandas as pd
    
    logging.info("Starting pre-deployment checks...")
    pre_deployment_data = [
        {"service": "api", "status": "running", "response_time": 150, "error_rate": 0.02},
        {"service": "database", "status": "running", "response_time": 50, "error_rate": 0.01},
        {"service": "cache", "status": "running", "response_time": 20, "error_rate": 0.00},
        {"service": "auth", "status": "running", "response_time": 100, "error_rate": 0.03}
    ]
    
    df = pd.DataFrame(pre_deployment_data)
    pre_deployment_report = {
        'services_status': df['status'].value_counts().to_dict(),
        'deployment_ready': True,
        'timestamp': pd.Timestamp.now().isoformat()
    }
    
    logging.info(f"Pre-deployment checks completed")
    return pre_deployment_report


def download_stack_fn():
    import logging
    import pandas as pd
    from datetime import datetime
    import time 
    import json 
    from pathlib import Path

    AIRFLOW_DATA_DIR = Path('/opt/airflow/data')
    FILE_NAME = 'download_report_from_v1.0.0.json'
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

def run_pre_check_fn(pre_deployment_checks_result):
    import logging
    import pandas as pd
    from datetime import datetime
    
    logging.info("Starting run pre-checks...")
    
    # Get reports from previous tasks
    logging.info(f"Pre Deployment Report: {pre_deployment_checks_result}")
    
    check_data = [
        {"component": "baseos","memory": 512, "status": "healthy"},
        {"component": "gi", "memory": 1024, "status": "healthy"},
    ]
    
    df = pd.DataFrame(check_data)
    precheck_report = {
        'total_memory_usage_mb': int(df['memory'].sum()),
        'checks_passed': True,
        'timestamp': datetime.now().isoformat()
    }
    
    
    logging.info(f"Pre-checks completed:\n"
                f"Total memory usage: {precheck_report['total_memory_usage_mb']}%\n"
                f"Status: {'PASS' if precheck_report['checks_passed'] else 'FAIL'}")
    
    return precheck_report

def deploy_stack_fn():
    print("Deploying the stack...")
    time.sleep(10)
    print("Stack deployed successfully...")

def finish_download_fn():
    print("Finishing download...")
    time.sleep(3)
    print("Download completed successfully...")

