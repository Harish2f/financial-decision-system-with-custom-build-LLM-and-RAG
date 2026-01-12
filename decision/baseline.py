class BaselineRiskModel:
    """
    Baseline-Regel für Finanzrisiko.
    Diese Logik wird von Finance akzeptiert und dient als Referenz
    für alle ML-Modelle.
    """

    def predict(self, df):
        return (
            (df["avg_days_late"] > 15)
            | ((df["total_billed"] - df["total_paid"]) > 10000)
        ).astype(int)