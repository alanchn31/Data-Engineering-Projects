from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.sparkify_plugin import (StageToRedshiftOperator, LoadFactOperator,
                               LoadDimensionOperator, DataQualityOperator)
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from helpers import SqlQueries

# /opt/airflow/start.sh

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': True
}

with DAG(dag_id='sparkify_music_dwh_dag', default_args=default_args,
         description='Load and transform data in Redshift \
                      Data Warehouse with Airflow',
         schedule_interval='@hourly') as dag:

    start_operator = DummyOperator(task_id='begin_execution', dag=dag)

    create_tables = PostgresOperator(
        task_id='create_tables',
        postgres_conn_id="redshift",
        sql="create_tables.sql"
    )

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='load_stage_events',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket="udacity-dend",
        s3_key="log_data",
        jsonpath="log_json_path.json",
        table_name="public.staging_events",
        ignore_headers=1
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='load_stage_songs',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket="udacity-dend",
        s3_key="song_data",
        table_name="public.staging_songs",
        ignore_headers=1
    )

    load_songplays_table = LoadFactOperator(
        task_id='load_songplays_fact_table',
        redshift_conn_id="redshift",
        load_sql=SqlQueries.songplay_table_insert,
        table_name="public.songplays"
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='load_user_dim_table',
        redshift_conn_id="redshift",
        load_sql=SqlQueries.user_table_insert,
        table_name="public.users",
        append_only=False
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='load_song_dim_table',
        redshift_conn_id="redshift",
        load_sql=SqlQueries.song_table_insert,
        table_name="public.songs",
        append_only=False
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='load_artist_dim_table',
        redshift_conn_id="redshift",
        load_sql=SqlQueries.artist_table_insert,
        table_name="public.artists",
        append_only=False
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='load_time_dim_table',
        redshift_conn_id="redshift",
        load_sql=SqlQueries.time_table_insert,
        table_name="public.time",
        append_only=False
    )

    run_quality_checks = DataQualityOperator(
        task_id='run_data_quality_checks',
        redshift_conn_id="redshift",
        table_names=["public.staging_events", "public.staging_songs",
                    "public.songplays", "public.artists",
                    "public.songs", "public.time", "public.users"]
    )

    end_operator = DummyOperator(task_id='stop_execution', dag=dag)

    start_operator               >> create_tables
    create_tables                >> [stage_events_to_redshift,
                                     stage_songs_to_redshift]

    [stage_events_to_redshift, 
     stage_songs_to_redshift]    >> load_songplays_table

    load_songplays_table         >> [load_user_dimension_table,
                                     load_song_dimension_table,
                                     load_artist_dimension_table,
                                     load_time_dimension_table]
    [load_user_dimension_table,
     load_song_dimension_table,
     load_artist_dimension_table,
     load_time_dimension_table]   >> run_quality_checks
             
    run_quality_checks            >> end_operator