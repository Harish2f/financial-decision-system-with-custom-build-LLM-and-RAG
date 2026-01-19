from decision.drift_monitor import DriftMonitor
from decision.feature_store import FeatureStore
from decision.baseline import BaselineRiskModel
from decision.evaluator import Evaluator
from decision.ml_adapter import MLAdapter
from decision.inference_guard import InferenceGuard
from decision.feature_contract import FEATURES

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

    from decision.feature_contract import FEATURES

    def run_ml(self):
       df = self.store.load_features()
       y_true = df["risk_label"]

       X = df.drop(columns=["risk_label", "customer_id"])

       guard = InferenceGuard(
           expected_features=FEATURES,
           feature_bounds=FEATURE_BOUNDS,
       )
       X = guard.validate(X)

       reference_df = self.store.load_reference_features()[FEATURES]
       DriftMonitor(reference_df).check(X)

       y_pred = MLAdapter().predict(X)
       return self.evaluator.evaluate(y_true, y_pred)
      