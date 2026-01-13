import pandas as pd
from decision.feature_store import FeatureStore

class DataDriftMonitor:
    def __init__(self):
        self.store = FeatureStore()

    def compute_stats(self):
        df = self.store.load_features()
        return {
            "avg_days_late_mean": df["avg_days_late"].mean(),
            "total_billed_mean": df["total_billed"].mean(),
            "total_paid_mean": df["total_paid"].mean(),
            "risk_rate": df["risk_label"].mean()
        }