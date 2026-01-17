import os
from sqlalchemy import create_engine, text


def get_engine():
    return create_engine(
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
    )


def run():
    engine = get_engine()

    sql = """
    DROP TABLE IF EXISTS customer_finance_features;

    CREATE TABLE customer_finance_features AS
    SELECT
        c.customer_id,

        /* ---------- invoice-based features ---------- */
        COUNT(i.invoice_id) AS total_invoices,

        COALESCE(
            SUM(CASE WHEN i.days_late > 0 THEN 1 ELSE 0 END),
            0
        ) AS late_invoices,

        COALESCE(
            AVG(i.days_late),
            0
        ) AS avg_days_late,

        COALESCE(
            SUM(i.amount),
            0
        ) AS total_billed,

        /* ---------- payment-based features ---------- */
        COALESCE(
            SUM(p.amount),
            0
        ) AS total_paid,

        /* ---------- governance label (baseline-aligned) ---------- */
        CASE
            WHEN
                COALESCE(AVG(i.days_late), 0) > 15
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

    with engine.begin() as conn:
        conn.execute(text(sql))

    print("customer_finance_features rebuilt successfully (schema-correct, NULL-safe).")


if __name__ == "__main__":
    run()