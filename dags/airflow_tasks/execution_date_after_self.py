from airflow.utils.db import provide_session
from airflow.models import DagRun
from sqlalchemy.orm import Session
from datetime import timedelta

@provide_session
def execution_date_after_self(execution_date, dag_id, session: Session = None):
    """
    Finds the latest execution of dag_id AFTER the current DAG started.
    Ensures it does not pick up past runs.
    """
    latest_signal_run = session.query(DagRun).filter(
        DagRun.dag_id == dag_id,
        DagRun.execution_date > execution_date,
        DagRun.state == "success",  # ✅ Ensures only completed runs are considered
    ).order_by(DagRun.execution_date.desc()).first()

    return latest_signal_run.execution_date if latest_signal_run else execution_date + timedelta(seconds=1)