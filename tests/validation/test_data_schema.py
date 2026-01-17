import pandas as pd

EXPECTED_SCHEMA = {
    "customer_id": "int64",
    "total_invoices": "int64",
    "late_invoices": "int64",
    "avg_days_late": "float64",
    "total_billed": "float64",
    "total_paid": "float64",
    "risk_label": "int64"
}

def test_training_schema():
    df = pd.read_csv("models/training_data.csv")

    for col, dtype in EXPECTED_SCHEMA.items():
        assert col in df.columns, f"Missing column {col}"
        assert str(df[col].dtype) == dtype, f"{col} has wrong dtype"