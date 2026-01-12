ALTER TABLE customer_finance_features
ADD COLUMN IF NOT EXISTS baseline_risk INT;

UPDATE customer_finance_features
SET baseline_risk =
    CASE
        WHEN avg_days_late > 15
             OR (total_billed - total_paid) > 10000
        THEN 1
        ELSE 0
    END;