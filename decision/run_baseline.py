"""
Baseline financial risk decision logic.

This file implements the FINANCE-APPROVED baseline used as a
governance gate before any ML model is allowed into production.

Design principles:
- Pure functions for testability
- No implicit globals
- Single source of truth for business logic
"""

from sqlalchemy import create_engine
import pandas as pd
from config import DATABASE_URL


# ============================================================
# Baseline decision logic (PURE FUNCTION)
# ============================================================

def is_risky_baseline(avg_days_late: float, unpaid_balance: float) -> bool:
    """
    Finance-approved baseline risk rule.

    A customer is considered risky if:
    - Average payment delay > 15 days
      OR
    - Unpaid balance > 10,000 €

    Parameters
    ----------
    avg_days_late : float
        Average number of days invoices are paid late
    unpaid_balance : float
        Total outstanding unpaid balance

    Returns
    -------
    bool
        True if customer is risky, False otherwise
    """
    return avg_days_late > 15 or unpaid_balance > 10_000


# ============================================================
# Baseline execution (PIPELINE / BATCH)
# ============================================================

def run_baseline():
    """
    Executes baseline risk decision on customer features
    stored in PostgreSQL.

    Writes baseline predictions back to the database.
    """
    engine = create_engine(DATABASE_URL)

    query = """
        SELECT
            customer_id,
            avg_days_late,
            unpaid_balance
        FROM customer_features
    """

    df = pd.read_sql(query, engine)

    df["baseline_risk"] = df.apply(
        lambda r: int(
            is_risky_baseline(
                avg_days_late=r.avg_days_late,
                unpaid_balance=r.unpaid_balance
            )
        ),
        axis=1
    )

    df[["customer_id", "baseline_risk"]].to_sql(
        "baseline_predictions",
        engine,
        if_exists="replace",
        index=False
    )

    print("Baseline risk decisions written to baseline_predictions")


# ============================================================
# CLI ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    run_baseline()