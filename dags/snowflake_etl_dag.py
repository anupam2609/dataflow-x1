from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/spark/work-dir/src')
from src.orchestrator import  run_etl_pipeline

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'snowflake_config_driven_etl',
    default_args=default_args,
    description='A modular ETL pipeline using Snowflake',
    schedule_interval='@daily',
    catchup=False
) as dag:

    run_etl_task = PythonOperator(
        task_id='run_snowflake_etl',
        python_callable=run_etl_pipeline,
    )

    run_etl_task