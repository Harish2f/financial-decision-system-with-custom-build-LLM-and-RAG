import joblib
import pandas as pd

def test_model_feature_alignment():
    model = joblib.load("models/risk_model.joblib")
    df = pd.read_csv("models/training_data.csv")

    X = df.drop(columns=["risk_label"])

    assert X.shape[1] == model.n_features_in_