import pandas as pd

def build_ml_features(df):
    drop_cols = ["customer_id", "risk_label", "baseline_risk"]
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])

    for col in X.select_dtypes(include=["object"]).columns:
        try:
            X[col] = pd.to_numeric(X[col])
        except Exception:
            X[col] = X[col].astype("category").cat.codes

    return X