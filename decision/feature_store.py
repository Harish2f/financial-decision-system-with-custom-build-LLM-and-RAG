import pandas as pd
from decision.run_baseline import get_engine

class FeatureStore:
    def __init__(self):
        self.engine = get_engine()

    def load_features(self) -> pd.DataFrame:
        return pd.read_sql(
            "SELECT * FROM customer_finance_features",
            self.engine
        )

    def load_reference_features(self) -> pd.DataFrame:
        """
        Reference data used for drift detection.
        This must match the distribution used during training.
        """
        return pd.read_csv("models/training_data.csv")