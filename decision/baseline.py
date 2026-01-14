import numpy as np

class BaselineRiskModel:
    """
    Finance-approved baseline.
    This must be mathematically reproducible even if SQL changes.
    """

    def predict(self, df):
        avg_days_late = df["avg_days_late"].fillna(0).astype(float)
        total_billed = df["total_billed"].fillna(0).astype(float)
        total_paid = df["total_paid"].fillna(0).astype(float)

        unpaid = total_billed - total_paid

        risk = (avg_days_late > 15) | (unpaid > 10000)
        return risk.astype(np.int8)