from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime,timedelta

# Define the Python function to be executed
def print_hello():
    print("Hello, Airflow!")


# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 22),  # Set your start date
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

with DAG(
    'hello_airflow',
    default_args=default_args,
    description='spotify_pipeline_DAG',
    schedule_interval='@weekly',  # Set to None to trigger manually or set a cron expression
    catchup=False,
) as dag:

    # Create a task using PythonOperator
    hello_task = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello,
    )
    etl_task = BashOperator(
        task_id='etl_task',
        bash_command='python /opt/airflow/dags/etl.py'
)
    ml_task = BashOperator(
        task_id='ml_task',
        bash_command='python /opt/airflow/dags/ml.py'
)
    hello_task >> etl_task >> ml_task  # Set the task to run
