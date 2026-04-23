import duckdb
import os

# caminho do dataset bruto (entrada)
INPUT_PATH = "data/raw/yellow_tripdata_2026-01.parquet"

# caminho do dataset tratado (saída)
OUTPUT_PATH = "data/processed/yellow_tripdata_2026-01_clean.parquet"


def salvar_dados(con: duckdb.DuckDBPyConnection):
    """
    Realiza a transformação dos dados e salva o resultado em parquet.

    Etapas:
    - limpeza de registros inválidos
    - criação de novas colunas analíticas
    - persistência dos dados tratados
    """

    con.execute(f"""
    COPY (
        SELECT
            *,
            
            -- cálculo da duração da corrida em minutos
            date_diff('minute', tpep_pickup_datetime, tpep_dropoff_datetime) AS trip_duration_min,

            -- extração da data da corrida
            DATE(tpep_pickup_datetime) AS pickup_date,

            -- extração da hora da corrida
            EXTRACT(hour FROM tpep_pickup_datetime) AS pickup_hour

        FROM read_parquet('{INPUT_PATH}')

        -- remoção de corridas inválidas:
        -- - distância negativa ou zero
        -- - valores monetários negativos ou zero
        -- - dropoff anterior ao pickup
        WHERE
            trip_distance > 0
            AND fare_amount > 0
            AND total_amount > 0
            AND tpep_dropoff_datetime >= tpep_pickup_datetime
    )
    TO '{OUTPUT_PATH}' (FORMAT 'parquet');
    """)

    print("Dados transformados e salvos com sucesso.")


def main():
    """
    Etapa de transformação:
    - valida existência do dataset de entrada
    - executa limpeza e transformação
    - salva resultado na camada processed
    """

    print("Iniciando transformação dos dados...")

    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError("Arquivo de entrada não encontrado.")

    con = duckdb.connect()

    salvar_dados(con)

    print("Transformação concluída.")


if __name__ == "__main__":
    main()