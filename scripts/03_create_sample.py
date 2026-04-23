import os
import duckdb

# arquivo bruto de entrada
INPUT_PATH = "data/raw/yellow_tripdata_2026-01.parquet"

# arquivo de saída com amostra tratada
OUTPUT_PATH = "data/processed/yellow_tripdata_2026-01_sample.parquet"


def main():
    print("Iniciando criação da amostra tratada...")

    # valida se o arquivo bruto existe
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_PATH}")

    print("Arquivo de entrada encontrado.")

    con = duckdb.connect()

    # cria uma amostra tratada a partir do raw
    # isso evita depender do arquivo clean grande, que está com problema de leitura
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

        USING SAMPLE 100000 ROWS
    )
    TO '{OUTPUT_PATH}' (FORMAT PARQUET);
    """)

    print("Amostra tratada criada com sucesso.")


if __name__ == "__main__":
    main()