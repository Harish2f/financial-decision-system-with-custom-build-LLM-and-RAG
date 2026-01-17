import pandas as pd
from decision.baseline import BaselineRiskModel


def test_baseline_high_delay():
    df = pd.DataFrame([{
        "avg_days_late": 20,
        "total_billed": 1000,
        "total_paid": 950,
    }])

    model = BaselineRiskModel()
    assert model.predict(df)[0] == 1


def test_baseline_high_unpaid_balance():
    df = pd.DataFrame([{
        "avg_days_late": 5,
        "total_billed": 20000,
        "total_paid": 0,
    }])

    model = BaselineRiskModel()
    assert model.predict(df)[0] == 1


def test_baseline_safe_customer():
    df = pd.DataFrame([{
        "avg_days_late": 5,
        "total_billed": 1000,
        "total_paid": 950,
    }])

    model = BaselineRiskModel()
    assert model.predict(df)[0] == 0