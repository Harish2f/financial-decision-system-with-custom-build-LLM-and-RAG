import pandas as pd
from sqlalchemy import text
from ingestion.repository import FinanceRepository

repo = FinanceRepository()

engine = repo.engine

df = pd.read_sql(
    text("SELECT * FROM customer_finance_features"),
    engine
)

# Drop identifiers
drop_cols = ["customer_id", "risk_label", "baseline_risk"]
X = df.drop(columns=[c for c in drop_cols if c in df.columns])
y = df["risk_label"]

df.to_csv("models/training_data.csv", index=False)

print("Training data exported")