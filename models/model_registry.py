import joblib
import os

MODEL_PATH = os.getenv("MODEL_PATH", "models/risk_model.joblib")

_model = None

def get_model():
    global _model

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Model not found at {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)

    return _model