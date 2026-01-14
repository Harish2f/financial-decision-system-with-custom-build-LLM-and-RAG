from sqlalchemy import create_engine
from config import DATABASE_URL
import pandas as pd

class FeatureStore:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def load_features(self):
        return pd.read_sql("SELECT * FROM customer_finance_features", self.engine)