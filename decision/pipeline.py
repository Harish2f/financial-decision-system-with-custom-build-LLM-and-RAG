from decision.drift_monitor import DriftMonitor
from decision.feature_store import FeatureStore
from decision.baseline import BaselineRiskModel
from decision.evaluator import Evaluator
from decision.ml_adapter import MLAdapter
from decision.inference_guard import InferenceGuard

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

    def run_ml(self):
        df = self.store.load_features()
        y_true = df["risk_label"]

        X = df.drop(columns=["risk_label"])

        guard = InferenceGuard(
         expected_features=EXPECTED_FEATURES,
            feature_bounds=FEATURE_BOUNDS,
    )

        # HARD GATE
        X = guard.validate(X)
        reference_df = self.store.load_reference_features()
        reference_df = reference_df[EXPECTED_FEATURES]

    
        monitor = DriftMonitor(reference_df)
        monitor.check(X)

        ml = MLAdapter()
        y_pred = ml.predict(X)

        return self.evaluator.evaluate(y_true, y_pred)