from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore

# === DEFAULT ARGUMENTS (Production) ===
default_args = {
    "owner": "finance-ai-platform",
    "depends_on_past": False,
    "retries": 2,                            # Retry twice on transient failures
    "retry_delay": timedelta(minutes=5),     # Wait 5 minutes between retries
    "execution_timeout": timedelta(hours=1), # Kill tasks running >1h
    "start_date": datetime(2026, 1, 1),
}

# === DAG SPECIFICATION ===
with DAG(
    dag_id="finance_ai_daily_pipeline",
    default_args=default_args,
    schedule_interval="0 2 * * *",   # 02:00 UTC daily
    catchup=False,                   # Do not backfill automatically
    max_active_runs=1,              # Only one run at a time
    tags=["finance", "risk", "production"],
) as dag:

    def generate_data(**context):
        """Generate synthetic finance data."""
        from ingestion.generate_data import main as gen_main
        gen_main()

    def ingest_customers(**context):
        from ingestion.load_customers import main as load_customers
        load_customers()

    def ingest_contracts(**context):
        from ingestion.load_contracts import main as load_contracts
        load_contracts()

    def ingest_invoices(**context):
        from ingestion.load_invoices import main as load_invoices
        load_invoices()

    def ingest_payments(**context):
        from ingestion.load_payments import main as load_payments
        load_payments()

    def build_features(**context):
        from pipelines.run_sql import main as run_sql
        run_sql()

    def run_baseline(**context):
        from decision.run_baseline import main as baseline
        baseline()

    def train_and_run_ml(**context):
        from models.train_model import main as train
        train()
        from decision.run_ml import main as run_ml
        run_ml()

    # === TASKS ===
    t_generate_data = PythonOperator(
        task_id="generate_data",
        python_callable=generate_data,
        executor_config={
            "KubernetesExecutor": {
                "request_cpu": "250m",
                "limit_cpu": "500m",
                "request_memory": "768Mi",
                "limit_memory": "1Gi",
            }
        },
    )

    t_ingest_customers = PythonOperator(
        task_id="ingest_customers",
        python_callable=ingest_customers,
        executor_config={
            "KubernetesExecutor": {
                "request_cpu": "250m",
                "limit_cpu": "500m",
                "request_memory": "768Mi",
                "limit_memory": "1Gi",
            }
        },
    )

    t_ingest_contracts = PythonOperator(
        task_id="ingest_contracts",
        python_callable=ingest_contracts,
        executor_config={
            "KubernetesExecutor": {
                "request_cpu": "250m",
                "limit_cpu": "500m",
                "request_memory": "768Mi",
                "limit_memory": "1Gi",
            }
        },
    )

    t_ingest_invoices = PythonOperator(
        task_id="ingest_invoices",
        python_callable=ingest_invoices,
        executor_config={
            "KubernetesExecutor": {
                "request_cpu": "250m",
                "limit_cpu": "500m",
                "request_memory": "768Mi",
                "limit_memory": "1Gi",
            }
        },
    )

    t_ingest_payments = PythonOperator(
        task_id="ingest_payments",
        python_callable=ingest_payments,
        executor_config={
            "KubernetesExecutor": {
                "request_cpu": "250m",
                "limit_cpu": "500m",
                "request_memory": "768Mi",
                "limit_memory": "1Gi",
            }
        },
    )

    t_build_features = PythonOperator(
        task_id="build_features",
        python_callable=build_features,
        executor_config={
            "KubernetesExecutor": {
                "request_cpu": "500m",
                "limit_cpu": "1",
                "request_memory": "1Gi",
                "limit_memory": "2Gi",
            }
        },
    )

    t_run_baseline = PythonOperator(
        task_id="run_baseline",
        python_callable=run_baseline,
        executor_config={
            "KubernetesExecutor": {
                "request_cpu": "500m",
                "limit_cpu": "1",
                "request_memory": "1Gi",
                "limit_memory": "2Gi",
            }
        },
    )

    t_train_and_run_ml = PythonOperator(
        task_id="train_and_run_ml",
        python_callable=train_and_run_ml,
        executor_config={
            "KubernetesExecutor": {
                "request_cpu": "1",
                "limit_cpu": "2",
                "request_memory": "2Gi",
                "limit_memory": "4Gi",
            }
        },
    )

    # === DEPENDENCIES ===
    t_generate_data >> [
        t_ingest_customers,
        t_ingest_contracts,
        t_ingest_invoices,
        t_ingest_payments,
    ]

    [
        t_ingest_customers,
        t_ingest_contracts,
        t_ingest_invoices,
        t_ingest_payments,
    ] >> t_build_features >> t_run_baseline >> t_train_and_run_ml