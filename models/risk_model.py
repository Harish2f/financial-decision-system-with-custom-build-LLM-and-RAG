import pandas as pd
from xgboost import XGBClassifier

class RiskModel:
    """
    ML-Modell für Finanzrisiko.
    Dieses Modell darf nur verwendet werden, wenn es die Baseline schlägt.
    """

    def __init__(self):
        self.model = XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            eval_metric="logloss"
        )

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)