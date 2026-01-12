import pandas as pd
import sqlalchemy
import config

engine = sqlalchemy.create_engine(
    f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
)

df = pd.read_sql("SELECT * FROM customer_finance_features", engine)

# Drop identifiers
X = df.drop(columns=["customer_id", "risk_label", "baseline_risk"])
y = df["risk_label"]

df.to_csv("models/training_data.csv", index=False)
print("Training data exported")