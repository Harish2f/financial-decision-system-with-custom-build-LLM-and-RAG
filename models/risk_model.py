import xgboost as XGBClassifier

class RiskModel:
    def __init__(self):
        self.model = XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric="logloss",
        )
        self.n_features_in_ = None

    def train(self, X, y):
        self.model.fit(X, y)

        # persist feature contract
        self.n_features_in_ = X.shape[1]
        self.feature_names_ = list(X.columns)

    def predict(self, X):
        # enforce training-time feature order
        X = X[self.feature_names_]
        return self.model.predict(X)