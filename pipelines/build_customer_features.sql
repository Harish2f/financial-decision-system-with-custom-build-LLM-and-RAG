DROP TABLE IF EXISTS customer_finance_features;

CREATE TABLE customer_finance_features AS
SELECT
    c.customer_id,
    COUNT(i.invoice_id) AS total_invoices,
    SUM(CASE WHEN p.payment_date > i.due_date THEN 1 ELSE 0 END) AS late_invoices,
    AVG(
        CASE
            WHEN p.payment_date IS NOT NULL
            THEN CAST(p.payment_date AS DATE) - CAST(i.due_date AS DATE)
            ELSE 0
        END
    ) AS avg_days_late,
    SUM(CAST(i.amount AS double precision)) AS total_billed,
    SUM(CAST(COALESCE(p.amount_paid, '0') AS double precision)) AS total_paid,

    /* Risk label defined inside the feature table */
    CASE
        WHEN (SUM(CASE WHEN p.payment_date > i.due_date THEN 1 ELSE 0 END)::float 
              / NULLIF(COUNT(i.invoice_id), 0)) > 0.30
             OR (SUM(i.amount) - SUM(COALESCE(p.amount_paid, 0))) > 10000
        THEN 1
        ELSE 0
    END AS risk_label

FROM customers c
LEFT JOIN invoices i ON c.customer_id = i.customer_id
LEFT JOIN payments p ON i.invoice_id = p.invoice_id
GROUP BY c.customer_id;