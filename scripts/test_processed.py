import os
import duckdb

# caminho do arquivo tratado (camada processed)
FILE_PATH = "data/processed/yellow_tripdata_2026-01_clean.parquet"

print("Iniciando teste do arquivo tratado...")

# verifica se o arquivo existe antes de tentar ler
# evita erro caso o caminho esteja errado
if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(f"Arquivo não encontrado: {FILE_PATH}")

print("Arquivo encontrado com sucesso.")

# cria conexão com DuckDB para leitura do parquet
con = duckdb.connect()

# consulta simples para validar leitura do arquivo
# COUNT(*) é eficiente e não carrega todos os dados na memória
resultado = con.execute(f"""
    SELECT COUNT(*) AS total_linhas
    FROM read_parquet('{FILE_PATH}')
""").fetchone()[0]

# exibe o total de linhas do dataset tratado
print(f"Total de linhas no arquivo tratado: {resultado}")

print("Teste concluído com sucesso.")