import pandas as pd
import pytest
from decision.inference_guard import InferenceGuard

EXPECTED_FEATURES = [
    "total_invoices",
    "late_invoices",
    "avg_days_late",
    "total_billed",
    "total_paid",
]

FEATURE_BOUNDS = {
    "avg_days_late": (0, 365),
    "total_billed": (0, 1_000_000),
    "total_paid": (0, 1_000_000),
}


def base_df():
    return pd.DataFrame({
        "total_invoices": [10, 5],
        "late_invoices": [2, 0],
        "avg_days_late": [12, 0],
        "total_billed": [5000, 2000],
        "total_paid": [3000, 2000],
    })


def test_guard_accepts_valid_input():
    guard = InferenceGuard(EXPECTED_FEATURES, FEATURE_BOUNDS)
    df = base_df()

    out = guard.validate(df)
    assert out.equals(df)


def test_guard_fails_on_missing_feature():
    guard = InferenceGuard(EXPECTED_FEATURES, FEATURE_BOUNDS)
    df = base_df().drop(columns=["total_paid"])

    with pytest.raises(RuntimeError, match="Missing features"):
        guard.validate(df)


def test_guard_fails_on_extra_feature():
    guard = InferenceGuard(EXPECTED_FEATURES, FEATURE_BOUNDS)
    df = base_df()
    df["unexpected"] = 1

    with pytest.raises(RuntimeError, match="Unexpected features"):
        guard.validate(df)


def test_guard_fails_on_out_of_bounds():
    guard = InferenceGuard(EXPECTED_FEATURES, FEATURE_BOUNDS)
    df = base_df()
    df.loc[0, "avg_days_late"] = 9999

    with pytest.raises(RuntimeError, match="out of bounds"):
        guard.validate(df)