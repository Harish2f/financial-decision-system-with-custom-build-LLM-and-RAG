from decision.feature_store import FeatureStore
from decision.baseline import BaselineRiskModel
from decision.evaluator import Evaluator
from decision.ml_adapter import MLAdapter

class DecisionPipeline:
    def __init__(self):
        self.store = FeatureStore()
        self.evaluator = Evaluator()

    def run_baseline(self):
        df = self.store.load_features()
        y_true = df["risk_label"]

        baseline = BaselineRiskModel()
        y_pred = baseline.predict(df)

        return self.evaluator.evaluate(y_true, y_pred)

    def run_ml(self):
        df = self.store.load_features()
        y_true = df["risk_label"]

        ml = MLAdapter()
        y_pred = ml.predict(df)

        return self.evaluator.evaluate(y_true, y_pred)