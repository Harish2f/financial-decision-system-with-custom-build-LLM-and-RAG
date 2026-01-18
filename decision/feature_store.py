import pandas as pd
from decision.run_baseline import get_engine

class FeatureStore:
    def __init__(self):
        self.engine = get_engine()

    def load_features(self):
        return pd.read_sql(
            "SELECT * FROM customer_finance_features",
            self.engine
        )