# airflow/dags/commission_pipeline_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner":           "data-engineering",
    "retries":         2,
    "retry_delay":     timedelta(minutes=5),
    "email_on_failure": True,
    "email":           ["de-alerts@company.com"],
}

with DAG(
    dag_id="broker_commission_pipeline",
    description="Daily broker commission ETL + anomaly detection",
    schedule_interval="0 6 * * *",   # 6 AM every day
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["commissions", "finance"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=lambda: __import__(
            "ingestion.batch_ingestor", fromlist=["run"]
        ).run(),
    )

    clean_and_transform = PythonOperator(
        task_id="clean_and_calculate_commissions",
        python_callable=lambda: __import__(
            "etl.calculate_commissions", fromlist=["main"]
        ).main(),
    )

    run_dbt = BashOperator(
        task_id="run_dbt_models",
        bash_command="cd /opt/dbt && dbt run --models marts --target prod",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/dbt && dbt test --models marts",
    )

    anomaly_check = PythonOperator(
        task_id="anomaly_detection_and_alerts",
        python_callable=lambda: __import__(
            "alerts.anomaly_detector", fromlist=["run"]
        ).run(),
    )

    # DAG dependency chain
    # ingest >> clean_and_transform >> run_dbt >> dbt_test >> anomaly_check