import os
import duckdb

# caminho do arquivo bruto no S3
FILE_PATH = "s3://taxi-data-aline-2026/yellow_tripdata_2026-01.parquet"


def conectar_duckdb() -> duckdb.DuckDBPyConnection:
    """
    Cria conexão com DuckDB para leitura e execução de queries em arquivos parquet.
    """
    return duckdb.connect()


def configurar_s3(con: duckdb.DuckDBPyConnection) -> None:
    """
    Habilita leitura de arquivos no S3 usando DuckDB.

    - httpfs: extensão para acesso a arquivos remotos
    - aws: integração com credenciais AWS
    - SECRET: usa a cadeia de credenciais configurada no aws configure
    """
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")

    con.execute("INSTALL aws;")
    con.execute("LOAD aws;")

    con.execute("""
        CREATE OR REPLACE SECRET (
            TYPE s3,
            PROVIDER credential_chain,
            REGION 'sa-east-1'
        );
    """)


def validar_arquivo_local(path: str) -> None:
    """
    Verifica se um arquivo local existe antes de iniciar o pipeline.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    print("Arquivo local encontrado com sucesso.")


def validar_arquivo_s3(con: duckdb.DuckDBPyConnection, path: str) -> None:
    """
    Valida acesso ao arquivo no S3 tentando ler uma linha.

    Se conseguir executar a consulta, significa que:
    - o arquivo existe
    - o caminho está correto
    - as credenciais AWS estão funcionando
    """
    query = f"""
        SELECT 1
        FROM read_parquet('{path}')
        LIMIT 1
    """

    con.execute(query).fetchone()

    print("Arquivo no S3 acessado com sucesso.")


def contar_linhas(con: duckdb.DuckDBPyConnection, path: str) -> int:
    """
    Conta o número total de registros no dataset.
    Útil para validação inicial do volume de dados.
    """
    query = f"""
        SELECT COUNT(*) AS total_linhas
        FROM read_parquet('{path}')
    """

    total_linhas = con.execute(query).fetchone()[0]

    print(f"Total de linhas: {total_linhas}")

    return total_linhas


def validar_schema(con: duckdb.DuckDBPyConnection, path: str):
    """
    Retorna a estrutura do dataset (colunas e tipos).
    Importante para entender o formato dos dados antes da transformação.
    """
    query = f"""
        DESCRIBE
        SELECT *
        FROM read_parquet('{path}')
    """

    schema = con.execute(query).df()

    print("\nSchema do dataset:")
    print(schema)

    return schema


def main() -> None:
    """
    Etapa de extração e validação:
    - cria conexão com DuckDB
    - configura acesso ao S3
    - valida existência e acesso ao arquivo
    - valida volume e estrutura dos dados
    """

    print("Iniciando etapa de extração e validação...")

    con = conectar_duckdb()

    # se o arquivo estiver no S3, configura acesso remoto
    if FILE_PATH.startswith("s3://"):
        configurar_s3(con)
        validar_arquivo_s3(con, FILE_PATH)
    else:
        validar_arquivo_local(FILE_PATH)

    contar_linhas(con, FILE_PATH)
    validar_schema(con, FILE_PATH)

    print("\nExtração e validação concluídas com sucesso.")


if __name__ == "__main__":
    main()