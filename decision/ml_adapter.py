from models.model_registry import get_model
from decision.feature_builder import build_ml_features

class MLAdapter:
    def __init__(self):
        self.model = get_model()

    def predict(self, df):
        X = X[self.model.feature_names_]
        return self.model.predict(X)