from decision.feature_store import FeatureStore
from decision.baseline import BaselineRiskModel
from decision.evaluator import Evaluator

class DecisionPipeline:
    def run_baseline(self):
        store = FeatureStore()
        df = store.load_features()

        y_true = df["risk_label"]
        baseline = BaselineRiskModel()
        y_pred = baseline.predict(df)

        evaluator = Evaluator()
        return evaluator.evaluate(y_true, y_pred)