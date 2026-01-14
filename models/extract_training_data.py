import pandas as pd
from ingestion.repository import FinanceRepository

repo = FinanceRepository()
engine = repo.engine

df = pd.read_sql("SELECT * FROM customer_finance_features", engine)

# Drop identifiers
X = df.drop(columns=["customer_id", "risk_label", "baseline_risk"])
y = df["risk_label"]

df.to_csv("models/training_data.csv", index=False)
print("Training data exported")