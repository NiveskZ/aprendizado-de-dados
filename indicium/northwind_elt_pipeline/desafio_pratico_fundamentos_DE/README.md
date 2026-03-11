# Northwind ELT Pipeline com Apache Airflow

Atividade prática implementando um pipeline simples de ELT orquestrado com Apache Airflow. O fluxo extrai dados de um banco PostgreSQL de origem, salva localmente em CSV e carrega em um banco de destino.

## Stack

- Apache Airflow (via Astronomer CLI)
- PostgreSQL 12 (via Docker)
- Python — `PostgresHook` para conexão com os bancos

## Estrutura do pipeline

```
extract_customers → save_customers_locally → load_customers_to_target → validate_load
```

| Etapa | O que faz |
|---|---|
| `extract_customers` | Conecta no `source_db` e lê a tabela `customers` |
| `save_customers_locally` | Salva os dados extraídos em `/tmp/customers.csv` |
| `load_customers_to_target` | Cria a tabela no `target_db` e insere os dados do CSV |
| `validate_load` | Confirma que os registros chegaram no destino |

## Como executar

```bash
# 1. Sobe os bancos PostgreSQL
docker compose up -d

# 2. Sobe o Airflow localmente
astro dev start

# 3. Acessa localhost:8080 e cadastra as conexões em Admin > Connections
# 4. Dispara a DAG "northwind_customers_elt" manualmente
```

## Conexões necessárias no Airflow

| Campo | source_db | target_db |
|---|---|---|
| Conn Type | Postgres | Postgres |
| Host | `<gateway da rede Docker>` | `<gateway da rede Docker>` |
| Port | 5433 | 5434 |
| Schema | source_db | target_db |
| Login / Password | postgres / postgres | postgres / postgres |

> No Linux, `host.docker.internal` não resolve. Use o IP do gateway Docker: `docker network inspect bridge | grep Gateway`