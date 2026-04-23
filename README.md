# Taxi Data Pipeline

Pipeline de dados para processamento e análise de corridas de táxi, utilizando Python, DuckDB, Airflow, Docker e integração com AWS S3.

---

## Objetivo

Construir um pipeline de dados completo que realiza:

- Extração de dados brutos (local e S3)
- Validação de estrutura e volume
- Transformação e limpeza dos dados
- Geração de amostra para análise
- Criação de métricas analíticas
- Orquestração com Airflow

---

## Arquitetura do Pipeline

S3 / Arquivo bruto  
↓  
Extract & Validate (script 01)  
↓  
Transform & Clean (script 02)  
↓  
Create Sample (script 03)  
↓  
Analytics (script 04)  
↓  
Dataset pronto para análise  

---

## Tecnologias utilizadas

- Python  
- DuckDB  
- Apache Airflow  
- Docker  
- AWS S3  
- SQL  

---

## Estrutura do projeto

taxi-data-pipeline/  
│  
├── airflow/  
│   ├── dags/  
│   │   └── taxi_pipeline_dag.py  
│   └── docker-compose.yml  
│  
├── scripts/  
│   ├── 01_extract_validate.py  
│   ├── 02_transform_clean.py  
│   ├── 03_create_sample.py  
│   └── 04_analytics_hourly.py  
│  
├── notebooks/  
│   └── analysis_taxi_clean.ipynb  
│  
├── data/ (ignorado no git)  
│  
├── README.md  
└── .gitignore  

---

## Etapas do Pipeline

### 1. Extract & Validate
- Leitura do dataset (local ou S3)
- Validação de existência
- Contagem de registros
- Verificação de schema

### 2. Transform & Clean
- Remoção de valores inválidos
- Criação de variáveis derivadas:
  - duração da corrida
  - data
  - hora da corrida

### 3. Create Sample
- Geração de amostra reduzida para análise
- Otimização de performance para notebooks

### 4. Analytics
- Criação de métricas agregadas
- Análise de volume por horário
- Base para visualizações e insights

---

## Integração com AWS S3

O pipeline permite leitura direta de arquivos armazenados no S3 utilizando DuckDB:

- Leitura via read_parquet
- Autenticação via AWS CLI (aws configure)
- Uso da extensão httpfs

---

## Orquestração com Airflow

O pipeline é orquestrado com Apache Airflow via Docker, permitindo:

- Execução sequencial das etapas
- Monitoramento de tarefas
- Reprocessamento controlado

---

## Análise de Dados

O notebook `analysis_taxi_clean.ipynb` contém:

- Exploração inicial dos dados
- Cálculo de métricas médias
- Análise de distribuição de corridas por horário

---

## Evolução do Projeto

- v1: Pipeline local com DuckDB  
- v2: Orquestração com Airflow  
- v3: Integração com AWS S3  

---

## Como executar

### 1. Clonar repositório
```bash
git clone https://github.com/alinebbrasil/taxi-data-pipeline.git
cd taxi-data-pipeline