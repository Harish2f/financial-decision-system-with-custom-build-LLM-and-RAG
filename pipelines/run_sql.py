# pipelines/run_sql.py
import os
from sqlalchemy import create_engine, text


def get_engine() -> str:
    """
    Build a SQLAlchemy engine from the DB connection variables that are injected
    into the CI environment.  Using `engine.begin()` later guarantees a
    transaction that is automatically rolled back on error.
    """
    return create_engine(
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
    )


def run() -> None:
    """Create the denormalised feature table used by downstream models."""
    engine = get_engine()

    # NOTE:
    # The payments table stores the amount that was actually paid in the column
    # `amount`.  An earlier version of the script mistakenly used `paid_amount`,
    # which does not exist and caused a `psycopg2.errors.UndefinedColumn` error.
    # All references have been updated to `p.amount`.
    sql = """
    DROP TABLE IF EXISTS customer_finance_features;

    CREATE TABLE customer_finance_features AS
    SELECT
        c.customer_id,

        /* ---------- invoice counts ---------- */
        COUNT(i.invoice_id) AS total_invoices,

        /* ---------- late invoices ---------- */
        COALESCE(
            SUM(
                CASE
                    WHEN p.payment_date IS NOT NULL
                     AND i.due_date IS NOT NULL
                     AND p.payment_date::date > i.due_date::date
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ) AS late_invoices,

        /* ---------- avg days late ---------- */
        COALESCE(
            AVG(
                CASE
                    WHEN p.payment_date IS NOT NULL
                     AND i.due_date IS NOT NULL
                     AND p.payment_date::date > i.due_date::date
                    THEN (p.payment_date::date - i.due_date::date)
                    ELSE 0
                END
            ),
            0
        ) AS avg_days_late,

        /* ---------- money ---------- */
        COALESCE(SUM(i.amount), 0)                     AS total_billed,
        COALESCE(SUM(p.amount), 0)                     AS total_paid,

        /* ---------- risk / governance label ---------- */
        CASE
            WHEN
                COALESCE(
                    AVG(
                        CASE
                            WHEN p.payment_date IS NOT NULL
                             AND i.due_date IS NOT NULL
                             AND p.payment_date::date > i.due_date::date
                            THEN (p.payment_date::date - i.due_date::date)
                            ELSE 0
                        END
                    ),
                    0
                ) > 15
                OR
                (COALESCE(SUM(i.amount), 0) - COALESCE(SUM(p.amount), 0)) > 10000
            THEN 1
            ELSE 0
        END AS risk_label

    FROM customers c
    LEFT JOIN invoices i
        ON c.customer_id = i.customer_id
    LEFT JOIN payments p
        ON i.invoice_id = p.invoice_id

    GROUP BY c.customer_id;
    """

    # Execute the whole batch in a single transaction
    with engine.begin() as conn:
        conn.execute(text(sql))

    print("customer_finance_features built successfully.")


if __name__ == "__main__":
    run()
