from xgboost import XGBClassifier

class RiskModel:
    def __init__(self):
        self.model = None
        self.feature_names_ = None

    def train(self, X, y):
        self.feature_names_ = list(X.columns)
        self.model.fit(X, y)

    def predict(self, X):
        X = X[self.feature_names_]
        return self.model.predict(X)