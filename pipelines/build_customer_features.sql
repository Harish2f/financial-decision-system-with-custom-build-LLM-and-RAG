DROP TABLE IF EXISTS customer_finance_features;

CREATE TABLE customer_finance_features AS
SELECT
    c.customer_id,
    COUNT(i.invoice_id) AS total_invoices,
    SUM(CASE WHEN p.payment_date > i.due_date THEN 1 ELSE 0 END) AS late_invoices,
    AVG(
        CASE
            WHEN p.payment_date IS NOT NULL THEN (p.payment_date - i.due_date)
            ELSE 0
        END
    ) AS avg_days_late,
    SUM(i.amount) AS total_billed,
    SUM(COALESCE(p.amount_paid, 0)) AS total_paid
FROM customers c
LEFT JOIN invoices i ON c.customer_id = i.customer_id
LEFT JOIN payments p ON i.invoice_id = p.invoice_id
GROUP BY c.customer_id;