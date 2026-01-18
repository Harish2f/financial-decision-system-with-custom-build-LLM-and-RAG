import numpy as np

class InferenceGuard:
    def __init__(self, expected_features, feature_bounds=None):
        self.expected_features = expected_features
        self.feature_bounds = feature_bounds or {}

    def validate(self, df):
        # 1. Column check
        missing = set(self.expected_features) - set(df.columns)
        if missing:
            raise RuntimeError(f"Missing features at inference: {missing}")

        # 2. Order check
        df = df[self.expected_features]

        # 3. Null check
        if df.isnull().any().any():
            raise RuntimeError("Null values detected at inference")

        # 4. Numeric check
        for col in df.columns:
            if not np.issubdtype(df[col].dtype, np.number):
                raise RuntimeError(f"Non-numeric feature at inference: {col}")

        # 5. Range checks (optional but powerful)
        for col, (low, high) in self.feature_bounds.items():
            if ((df[col] < low) | (df[col] > high)).any():
                raise RuntimeError(f"Out-of-range values in feature {col}")

        return df