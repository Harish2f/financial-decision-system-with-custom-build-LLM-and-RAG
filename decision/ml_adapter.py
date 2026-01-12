import joblib

class MLAdapter:
    def __init__(self, path="models/risk_model.joblib"):
        self.model = joblib.load(path)

    def predict(self, df):
        X = df.drop(columns=["customer_id", "risk_label", "baseline_risk"])
        return self.model.predict(X)