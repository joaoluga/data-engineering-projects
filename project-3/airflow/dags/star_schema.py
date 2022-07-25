from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import requests


def run_jupyter_notebook():
    endpoint = "http://jupyter_api:9999/star_schema"
    response = requests.get(endpoint)
    for line in response.text.split("\n"):
        print(line)


with DAG(
    "bancos_star_schema",
    default_args={
        "depends_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A dag that generates the 'Bancos Tarifas' star_schema",
    schedule_interval=None,
    start_date=datetime(2022, 7, 24),
    catchup=False,
    tags=["project3", "dbt", "jupyter"],
) as dag:

    t1 = PythonOperator(
        task_id="run_jupyter_notebook", python_callable=run_jupyter_notebook
    )

    t2 = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run --project-dir /usr/local/airflow/dbt/star_schema",
    )

    t3 = BashOperator(
        task_id="dbt_docs_generate",
        bash_command="dbt docs generate --project-dir /usr/local/airflow/dbt/star_schema",
    )

    t1 >> t2 >> t3
