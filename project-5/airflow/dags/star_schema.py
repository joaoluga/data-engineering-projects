import time
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import boto3


def get_parameter_value(parameter):

    ssm = boto3.client("ssm", "us-east-1")
    param = ssm.get_parameter(Name=parameter, WithDecryption=True)
    return param['Parameter']['Value']


def get_glue_operator(entity_name, etl_phase):

    def start_job(entity_name, etl_phase):

        bucket_name = get_parameter_value("/glue/glue_bucket_name")

        print("Starting Job")
        glue = boto3.client("glue", "us-east-1")
        job_response = glue.start_job_run(
            JobName='etl_job',
            Arguments={
                '--entity_name': entity_name,
                '--etl_phase': etl_phase,
                '--bucket_name': bucket_name
            },
            Timeout=10,
            WorkerType='Standard',
            NumberOfWorkers=1
        )

        job_run_id = job_response['JobRunId']

        print("Starting handling process")
        job_status = None
        while job_status != 'SUCCEEDED':
            print("Poking glue...")
            job_info = glue.get_job_run(
                JobName='etl_job',
                RunId=job_run_id,
                PredecessorsIncluded=False
            )

            job_status = job_info['JobRun']['JobRunState']
            print(f"Current JobRunState: {job_status}")
            if job_status in ("FAILED"):
                raise Exception("Job stopped!")
            print("Poking again in 30 seconds...\n")
            time.sleep(30)
        print(f"Job terminated with status: {job_status}")

    run_job = PythonOperator(
        task_id=f"run_job-{etl_phase}_{entity_name}",
        python_callable=start_job,
        op_kwargs={
            'entity_name': entity_name,
            'etl_phase': etl_phase
        }
    )

    return run_job


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
        start_date=datetime(2022, 8, 1),
        catchup=False,
        tags=["project5", "glue"],
) as dag:
    t1 = get_glue_operator('bancos', 'extract')
    t2 = get_glue_operator('lista_tarifas', 'extract')
    t3 = get_glue_operator('bancos', 'transform')
    t4 = get_glue_operator('lista_tarifas', 'transform')
    t5 = get_glue_operator('star_schema', 'transform')

    t1 >> t2 >> t3 >> t5
    t2 >> t4 >> t5
