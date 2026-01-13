from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "finance_ai_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

 PROJECT = "/Users/harish/dev/financial_decision_system"

ingest = BashOperator(
    task_id="ingest_data",
    bash_command=f"cd {PROJECT} && python -m ingestion.load_customers && python -m ingestion.load_contracts && python -m ingestion.load_invoices && python -m ingestion.load_payments"
)

features = BashOperator(
    task_id="build_features",
    bash_command=f"cd {PROJECT} && python pipelines/run_sql.py"
)

baseline = BashOperator(
    task_id="baseline_eval",
    bash_command=f"cd {PROJECT} && python decision/run_baseline.py"
)

ml = BashOperator(
    task_id="ml_eval",
    bash_command=f"cd {PROJECT} && python decision/run_ml.py"
)

monitor = BashOperator(
    task_id="monitor",
    bash_command=f"cd {PROJECT} && python monitoring/run_monitoring.py"
)