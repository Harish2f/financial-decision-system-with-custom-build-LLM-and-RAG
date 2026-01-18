import pandas as pd
import pytest
from decision.drift_monitor import DriftMonitor


def reference_df():
    return pd.DataFrame({
        "total_billed": [100, 200, 150, 180, 170],
        "avg_days_late": [1, 2, 3, 2, 1],
    })


def test_no_drift_passes():
    monitor = DriftMonitor(reference_df())
    current = reference_df()

    # Should not raise
    monitor.check(current)


def test_drift_detected_warns():
    monitor = DriftMonitor(reference_df())
    drifted = pd.DataFrame({
        "total_billed": [10000, 12000, 11000, 15000, 20000],
        "avg_days_late": [50, 60, 45, 70, 80],
    })

    with pytest.warns(UserWarning):
        monitor.check(drifted)