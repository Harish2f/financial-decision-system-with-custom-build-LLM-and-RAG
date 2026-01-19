from xgboost import XGBClassifier

class RiskModel:
    def __init__(self):
        self.model = XGBClassifier(
            eval_metric="logloss"
        )
        self.n_features_in_ = None

    def train(self, X, y):
        self.feature_names_ = list(X.columns)

        self.model.fit(X, y)

    def predict(self, X):
        if self.n_features_in_ is None:
            raise RuntimeError("Model is not trained")

        if X.shape[1] != self.n_features_in_:
            raise ValueError(
                f"Feature mismatch: expected {self.n_features_in_}, got {X.shape[1]}"
            )

        return self.model.predict(X)