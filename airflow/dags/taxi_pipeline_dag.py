from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# definição do DAG (pipeline de dados de táxi)
with DAG(
    dag_id="taxi_data_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # execução manual
    catchup=False,
    description="Pipeline de dados de táxi com validação, transformação, amostra e camada analítica"
) as dag:

    # tarefa 1: validação do dataset bruto
    extract_validate = BashOperator(
        task_id="extract_validate",
        bash_command="cd /opt/airflow && python scripts/01_extract_validate.py"
    )

    # tarefa 2: transformação e limpeza dos dados
    transform_clean = BashOperator(
        task_id="transform_clean",
        bash_command="cd /opt/airflow && python scripts/02_transform_clean.py"
    )

    # tarefa 3: criação da amostra tratada
    create_sample = BashOperator(
        task_id="create_sample",
        bash_command="cd /opt/airflow && python scripts/03_create_sample.py"
    )

    # tarefa 4: criação da camada analítica agregada por hora
    analytics = BashOperator(
        task_id="analytics",
        bash_command="cd /opt/airflow && python scripts/04_analytics_hourly.py"
    )

    # definição da ordem de execução
    extract_validate >> transform_clean >> create_sample >> analytics