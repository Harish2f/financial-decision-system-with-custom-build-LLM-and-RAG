import joblib
import pandas as pd
from models.features import DROP_COLUMNS


def test_model_feature_alignment():
    model = joblib.load("models/risk_model.joblib")
    df = pd.read_csv("models/training_data.csv")

    X = df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns])

    assert X.shape[1] == model.n_features_in_