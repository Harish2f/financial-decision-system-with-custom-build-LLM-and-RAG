import os
import pandas as pd
from sqlalchemy import create_engine


# -----------------------------
# Baseline business rule
# -----------------------------
def is_risky_baseline(avg_days_late: float, unpaid_balance: float) -> bool:
    """
    Business-approved baseline rule.

    Risky if:
    - avg_days_late > 15 days OR
    - unpaid_balance > 10,000 EUR
    """
    return avg_days_late > 15 or unpaid_balance > 10_000


# -----------------------------
# Database connection
# -----------------------------
def get_engine():
    host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    db = os.environ["DB_NAME"]

    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(db_url)


from sqlalchemy import inspect

def assert_customer_features_exist(engine):
    inspector = inspect(engine)
    if "customer_features" not in inspector.get_table_names():
        raise RuntimeError(
            "customer_features table not found. "
            "Ensure pipelines.run_sql executed successfully."
        )

# -----------------------------
# Pipeline entrypoint
# -----------------------------
def run():
    engine = get_engine()

    query = """
        SELECT
            customer_id,
            avg_days_late,
            unpaid_balance
        FROM customer_features
    """

    

    df = pd.read_sql(query, engine)

    df["baseline_risk"] = df.apply(
        lambda r: is_risky_baseline(
            r["avg_days_late"],
            r["unpaid_balance"]
        ),
        axis=1
    )

    risky = df["baseline_risk"].sum()
    total = len(df)

    print(f"Baseline flagged {risky}/{total} customers as risky")


if __name__ == "__main__":
    run()