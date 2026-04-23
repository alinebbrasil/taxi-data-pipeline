import os
import duckdb

# arquivo de entrada: amostra tratada
INPUT_PATH = "data/processed/yellow_tripdata_2026-01_sample.parquet"

# arquivo de saída: camada analítica agregada por hora
OUTPUT_PATH = "data/processed/analytics_hourly.parquet"


def main():
    """
    Cria uma camada analítica resumida por hora.
    
    Objetivo:
    - agregar os dados já tratados
    - gerar métricas prontas para consumo em BI ou dashboard
    """

    print("Iniciando criação da camada analítica por hora...")

    # valida se o arquivo de entrada existe
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_PATH}")

    print("Arquivo de entrada encontrado com sucesso.")

    # conexão com DuckDB para executar a transformação analítica
    con = duckdb.connect()

    # cria um novo parquet com métricas agregadas por hora
    con.execute(f"""
    COPY (
        SELECT
            pickup_hour,

            -- total de corridas por hora
            COUNT(*) AS total_corridas,

            -- distância média das corridas
            ROUND(AVG(trip_distance), 2) AS distancia_media,

            -- valor médio pago por corrida
            ROUND(AVG(total_amount), 2) AS valor_medio,

            -- duração média das corridas em minutos
            ROUND(AVG(trip_duration_min), 2) AS duracao_media

        FROM read_parquet('{INPUT_PATH}')
        GROUP BY pickup_hour
        ORDER BY pickup_hour
    )
    TO '{OUTPUT_PATH}' (FORMAT PARQUET);
    """)

    print("Camada analítica criada com sucesso.")


if __name__ == "__main__":
    main()