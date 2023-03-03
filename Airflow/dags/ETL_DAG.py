
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta
from PythonScript.Load import load_func



# dag_default_args={
#     'owner': 'Sadichhya',
#     'depends_on_past': False,
#     'start_date': days_ago(2),
#     'email': ['sadichhya.maharjan@gmail.com'],
#     'email_on_failure': True,
#     'email_on_retry': True,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),

# }

# dag_defination=DAG(
#     'spotify_dag',
#     default_args=dag_default_args,
#     description="Spotify ETL",
#     schedule_interval='0 14 * * *'
    
# )

# etl_run= PythonOperator(
#     task_id='spotify_etl_postgres',
#     dag=dag_default_args,
#     python_callable=load_func
# )

my_args = {
    'owner': 'airflow',
    'depends_on_past':False,
    'start_date': datetime(2023,2,18),
    'email':['sadichhya.maharjan@gmail.com'],
    'email_on_failure':True,
    'email_on_retry':True,
    'retries':1,
    'retry_delay':timedelta(minutes=5)
}

my_dag = DAG(
    'spotify_dag',
    default_args=my_args,
    description='Spotify ETL',
    schedule='0 14 * * *'
)
run_etl = PythonOperator(
    task_id = 'spotify_etl_postgresql',
    python_callable=load_func,
    dag=my_dag
)
run_etl



# etl_run