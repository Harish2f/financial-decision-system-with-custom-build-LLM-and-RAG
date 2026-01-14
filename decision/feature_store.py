import pandas as pd
from ingestion.repository import FinanceRepository

class FeatureStore:
    def __init__(self):
        self.repo = FinanceRepository()

    def load_features(self):
        return pd.read_sql("SELECT * FROM customer_finance_features", self.repo.engine)