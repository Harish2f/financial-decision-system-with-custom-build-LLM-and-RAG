import pandas as pd

def test_no_direct_target_leakage():
    df = pd.read_csv("models/training_data.csv")

    forbidden_patterns = [
        "risk",
        "label",
        "default",
        "late_ratio"
    ]

    feature_cols = df.drop(columns=["risk_label"]).columns

    for col in feature_cols:
        for pattern in forbidden_patterns:
            assert pattern not in col.lower(), f"Potential leakage feature: {col}"