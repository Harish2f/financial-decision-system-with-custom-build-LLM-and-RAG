import pandas as pd
import sqlalchemy
import config

class FeatureStore:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(
            f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
        )

    def load_features(self):
        return pd.read_sql("SELECT * FROM customer_finance_features", self.engine)