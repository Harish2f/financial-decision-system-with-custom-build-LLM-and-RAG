import pandas as pd

def test_customer_features_no_nulls():
    df = pd.read_csv("models/training_data.csv")

    critical_cols = [
        "total_invoices",
        "late_invoices",
        "avg_days_late",
        "total_billed",
        "total_paid",
        "risk_label"
    ]

    for col in critical_cols:
        assert col in df.columns, f"Missing feature: {col}"
        assert df[col].isnull().sum() == 0, f"Nulls found in {col}"


def test_feature_value_ranges():
    df = pd.read_csv("models/training_data.csv")

    assert (df["total_invoices"] >= 0).all()
    assert (df["late_invoices"] >= 0).all()
    assert (df["avg_days_late"] >= 0).all()
    assert (df["total_billed"] >= 0).all()
    assert (df["total_paid"] >= 0).all()