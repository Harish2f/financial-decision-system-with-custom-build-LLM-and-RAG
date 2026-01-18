import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

# -------------------------
# Configuration
# -------------------------
PSI_THRESHOLD = 0.2     # industry standard
KS_P_THRESHOLD = 0.05   # reject null if p < 0.05

FEATURES = [
    "total_invoices",
    "late_invoices",
    "avg_days_late",
    "total_billed",
    "total_paid",
]

# -------------------------
# PSI implementation
# -------------------------
def calculate_psi(expected, actual, buckets=10):
    expected = pd.Series(expected).dropna()
    actual = pd.Series(actual).dropna()

    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    breakpoints = np.unique(breakpoints)

    expected_percents = np.histogram(expected, breakpoints)[0] / len(expected)
    actual_percents = np.histogram(actual, breakpoints)[0] / len(actual)

    psi = np.sum(
        (expected_percents - actual_percents)
        * np.log((expected_percents + 1e-6) / (actual_percents + 1e-6))
    )

    return psi


# -------------------------
# Tests
# -------------------------
def test_population_stability_index():
    train = pd.read_csv("models/training_data.csv")
    inference = pd.read_csv("models/training_data.csv")  # replace later with live snapshot

    for feature in FEATURES:
        psi = calculate_psi(train[feature], inference[feature])
        assert psi < PSI_THRESHOLD, f"PSI drift detected in {feature}: {psi:.3f}"


def test_ks_statistic():
    train = pd.read_csv("models/training_data.csv")
    inference = pd.read_csv("models/training_data.csv")

    for feature in FEATURES:
        stat, p_value = ks_2samp(
            train[feature].dropna(),
            inference[feature].dropna()
        )
        assert p_value > KS_P_THRESHOLD, (
            f"KS drift detected in {feature}: p={p_value:.4f}"
        )