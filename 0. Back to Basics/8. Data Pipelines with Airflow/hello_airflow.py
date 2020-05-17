# Instructions
# Define a function that uses the python logger to log a function. Then finish filling in the details of the DAG down below. Once you’ve done that, run "/opt/airflow/start.sh" command to start the web server. Once the Airflow web server is ready,  open the Airflow UI using the "Access Airflow" button. Turn your DAG “On”, and then Run your DAG. If you get stuck, you can take a look at the solution file or the video walkthrough on the next page.

import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def my_function():
    logging.info("hello airflow")


dag = DAG(
        'mock_airflow_dag',
        start_date=datetime.datetime.now())

greet_task = PythonOperator(
   task_id="hello_airflow_task",
   python_callable=my_function,
   dag=dag
)