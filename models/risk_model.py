import xgboost as xgb

class RiskModel:
    def __init__(self):
        # MODEL MUST EXIST BEFORE train()
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42,
        )

        self.feature_names_ = None

    def train(self, X, y):
        self.feature_names_ = list(X.columns)
        self.model.fit(X, y)

    def predict(self, X):
        # HARD ALIGNMENT — protects against column drift
        X = X[self.feature_names_]
        return self.model.predict(X)