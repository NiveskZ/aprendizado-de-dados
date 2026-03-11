from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

import csv
import os
from datetime import datetime

# Caminho onde o CSV será salvo dentro do container do Airflow
FILE_PATH = "/tmp/customers.csv"

# Conecta no source_db e lê todos os registros da tabela customers
def extract_customers():
    # PostgresHook busca as credenciais pelo Conn Id cadastrado no Airflow
    # manualmente no Airflow em Admin > Connections
    hook = PostgresHook(postgres_conn_id="source_db")
    
    # get_records executa o SQL e retorna uma lista de tuplas diretamente
    records = hook.get_records("SELECT * FROM customers;")

    # get_conn().cursor() só para pegar os nomes das colunas
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers LIMIT 0;")  # LIMIT 0 = só metadados, sem dados
    headers = [col[0] for col in cursor.description]
    cursor.close()
    conn.close()

    print(f"{len(records)} registros extraídos.")
    return {"headers": headers, "rows": [list(row) for row in records]}


# Pega os dados extraídos e salva em um arquivo CSV local
def save_customers_locally(**context):
    # task_instance.xcom_pull busca o retorno da tarefa anterior
    ti = context["ti"]
    data = ti.xcom_pull(task_ids="extract_customers")

    headers = data["headers"]
    rows = data["rows"]

    with open(FILE_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Arquivo salvo em {FILE_PATH} com {len(rows)} registros.")


# Lê o CSV salvo e insere os dados no target_db
def load_customers_to_target():
    hook = PostgresHook(postgres_conn_id="target_db")

     # run() executa qualquer SQL diretamente, sem precisar abrir conexão manualmente
    hook.run("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id   VARCHAR(10) PRIMARY KEY,
            company_name  VARCHAR(100),
            contact_name  VARCHAR(100),
            contact_title VARCHAR(100),
            address       VARCHAR(200),
            city          VARCHAR(100),
            region        VARCHAR(100),
            postal_code   VARCHAR(20),
            country       VARCHAR(100),
            phone         VARCHAR(50),
            fax           VARCHAR(50)
        );
    """)

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["customer_id"], row["company_name"], row["contact_name"],
                row["contact_title"], row["address"], row["city"],
                row["region"], row["postal_code"], row["country"],
                row["phone"], row["fax"]
            )
            for row in reader
        ]

    # insert_rows insere uma lista de tuplas de uma vez, sem loop manual
    hook.insert_rows(
        table="customers",
        rows=rows,
        target_fields=[
            "customer_id", "company_name", "contact_name", "contact_title",
            "address", "city", "region", "postal_code", "country", "phone", "fax"
        ],
        replace=True,           # equivalente ao ON CONFLICT DO UPDATE
        replace_index="customer_id"
    )

    print(f"{len(rows)} registros carregados no target_db.")


# Consulta o target_db para confirmar que os dados chegaram
def validate_load():
    hook = PostgresHook(postgres_conn_id="target_db")

    # get_first retorna só a primeira linha do resultado
    result = hook.get_first("SELECT COUNT(*) FROM customers;")
    count = result[0]

    print(f"Validação: {count} registros encontrados no target_db.")

    if count == 0:
        raise ValueError("Nenhum registro encontrado no target_db!")


# Aqui juntamos tudo e definimos a ordem de execução
with DAG(
    dag_id="northwind_customers_elt",   # nome que aparece no Airflow
    start_date=datetime(2024, 1, 1),    # data de referência (não agenda automaticamente)
    schedule=None,                       # None = só roda quando você disparar manualmente
    catchup=False,                       # não tenta "recuperar" execuções passadas
    tags=["elt", "northwind"],          # tags para organizar na interface
) as dag:

    t1 = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_customers,
    )

    t2 = PythonOperator(
        task_id="save_customers_locally",
        python_callable=save_customers_locally,
    )

    t3 = PythonOperator(
        task_id="load_customers_to_target",
        python_callable=load_customers_to_target,
    )

    t4 = PythonOperator(
        task_id="validate_load",
        python_callable=validate_load,
    )

    # >> define a ordem: t1 roda, depois t2, depois t3, depois t4
    t1 >> t2 >> t3 >> t4