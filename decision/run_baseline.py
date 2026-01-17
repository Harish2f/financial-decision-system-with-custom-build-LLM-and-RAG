import os
import pandas as pd
from sqlalchemy import create_engine, inspect

from decision.baseline import BaselineRiskModel


# -----------------------------
# Database connection
# -----------------------------
def get_engine():
    return create_engine(
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
    )


# -----------------------------
# Safety check (governance)
# -----------------------------
def assert_feature_table_exists(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "customer_finance_features" not in tables:
        raise RuntimeError(
            "Required table 'customer_finance_features' not found. "
            "Ensure pipelines.run_sql executed successfully.\n"
            f"Available tables: {tables}"
        )


# -----------------------------
# Pipeline entrypoint
# -----------------------------
def run():
    engine = get_engine()
    assert_feature_table_exists(engine)

    query = """
        SELECT
            customer_id,
            avg_days_late,
            total_billed,
            total_paid
        FROM customer_finance_features
    """

    df = pd.read_sql(query, engine)

    model = BaselineRiskModel()
    df["baseline_risk"] = model.predict(df)

    risky = int(df["baseline_risk"].sum())
    total = len(df)

    print(f"[BASELINE] Flagged {risky}/{total} customers as risky")


if __name__ == "__main__":
    run()