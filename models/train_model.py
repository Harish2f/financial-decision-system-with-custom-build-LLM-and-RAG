import pandas as pd
from sklearn.model_selection import train_test_split
from models.risk_model import RiskModel
import joblib
import os

df = pd.read_csv("models/training_data.csv")

# Prepare features: drop identifier/label/baseline columns if present
drop_cols = ["customer_id", "risk_label", "baseline_risk"]
X = df.drop(columns=[c for c in drop_cols if c in df.columns])

# Coerce object columns to numeric where possible, otherwise encode as categorical codes
for col in X.select_dtypes(include=["object"]).columns:
    try:
        X[col] = pd.to_numeric(X[col])
    except Exception:
        X[col] = X[col].astype("category").cat.codes

y = df["risk_label"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RiskModel()
model.train(X_train, y_train)

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/risk_model.joblib")

print("Model trained and saved")