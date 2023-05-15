from datetime import datetime

from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator


EXECUTION_DATE_INIT = "{{ dag_run.logical_date.strftime('%Y_%m_%d') }}"


with DAG(
    dag_id="airbyte_vendas_example",
    default_args={"owner": "airflow"},
    schedule_interval="@daily",
    start_date=datetime(2023, 5, 11),
) as dag:

    async_money_to_json = AirbyteTriggerSyncOperator(
        task_id="airbyte_async_data_vendas",
        airbyte_conn_id="airbyte_conn_example",
        connection_id="1e3b5a72-7bfd-4808-a13c-204505490110",
        asynchronous=True,
    )

    airbyte_sensor = AirbyteJobSensor(
        task_id="airbyte_sensor_data_vendas",
        airbyte_conn_id="airbyte_conn_example",
        airbyte_job_id=async_money_to_json.output,
    )
    tb_vendas_bronze = GCSToBigQueryOperator(
        task_id="gcs_to_bq_job_bronze_tb_vendas",
        bucket="lucas-datalake-transient",
        source_objects=f"shopping/tb_vendas/{EXECUTION_DATE_INIT}*.parquet",
        destination_project_dataset_table="shopping_bronze.tb_vendas",
        source_format="PARQUET",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
        autodetect=True,
    )
    tb_customer_bronze = GCSToBigQueryOperator(
        task_id="gcs_to_bq_job_bronze_tb_customer",
        bucket="lucas-datalake-transient",
        source_objects=f"shopping/tb_customer/{EXECUTION_DATE_INIT}*.parquet",
        destination_project_dataset_table="shopping_bronze.tb_customer",
        source_format="PARQUET",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
        autodetect=True,
    )

    async_money_to_json >> airbyte_sensor >> [tb_vendas_bronze, tb_customer_bronze]
