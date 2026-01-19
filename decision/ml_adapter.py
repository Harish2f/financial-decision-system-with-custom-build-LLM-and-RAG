from models.model_registry import get_model

class MLAdapter:
    def __init__(self):
        self.model = get_model()

    def predict(self, df):
        X = df[self.model.feature_names_]
        return self.model.predict(X)