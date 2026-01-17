import pandas as pd

def test_no_future_information():
    df = pd.read_csv("models/training_data.csv")

    # Avg days late must not be negative (future payment dates)
    assert (df["avg_days_late"] >= 0).all()

    # Late invoices cannot exceed total invoices
    assert (df["late_invoices"] <= df["total_invoices"]).all()