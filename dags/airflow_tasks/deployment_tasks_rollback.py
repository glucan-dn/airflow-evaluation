import time 

def pre_deployment_checks_rollback():
    print("Start rollback on pre-deployment...")
    time.sleep(10)
    print("Rollback on pre-deployment completed successfully...")


def download_stack_rollback():
    print("Start rollback on download stack...")
    time.sleep(10)
    print("Rollback on download stack completed successfully...")

def run_pre_check_rollback():
    print("Start rollback on pre-check...")
    time.sleep(10)
    print("Rollback on pre-check completed successfully...")


def deploy_stack_rollback():
    print("Start rollback on deploy stack...")
    time.sleep(10)
    print("Rollback on deploy stack completed successfully...")


def finish_download_rollback():
    print("Start rollback on finish download...")
    time.sleep(10)
    print("Rollback on finish download completed successfully...")

# Map each task_id to its rollback function
rollback_map = {
    "pre_deployment_checks": pre_deployment_checks_rollback,
    "download_stack": download_stack_rollback,
    "run_pre_check": run_pre_check_rollback,
    "deploy_stack": deploy_stack_rollback,
    "finish_download": finish_download_rollback,
}
