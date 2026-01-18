import pandas as pd
from decision.baseline import BaselineRiskModel
from decision.ml_adapter import MLAdapter


def test_ml_agrees_with_extreme_baseline_cases():
    df = pd.DataFrame({
        "total_invoices": [10],
        "late_invoices": [10],
        "avg_days_late": [90],
        "total_billed": [50000],
        "total_paid": [0],
    })

    baseline = BaselineRiskModel()
    ml = MLAdapter()

    baseline_pred = baseline.predict(df).iloc[0]
    ml_pred = ml.predict(df)[0]

    # ML may be probabilistic, but should never mark this safe
    assert baseline_pred == 1
    assert ml_pred == 1