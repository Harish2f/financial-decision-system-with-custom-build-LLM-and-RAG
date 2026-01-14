import pandas as pd
import sqlalchemy
import config

_ENGINE = None

def get_engine():
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = sqlalchemy.create_engine(
            f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}"
            f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
            f"?sslmode={config.DB_SSLMODE}"
        )
    return _ENGINE

class FeatureStore:
    def __init__(self, engine=None):
        self.engine = engine or get_engine()

    def load_features(self):
        return pd.read_sql("SELECT * FROM customer_finance_features", self.engine)