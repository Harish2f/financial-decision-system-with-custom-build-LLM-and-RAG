import numpy as np

class InferenceGuard:
    def __init__(self, expected_features, feature_bounds):
        self.expected_features = list(expected_features)  # ORDERED
        self.feature_bounds = feature_bounds

    def validate(self, df):
        incoming_features = set(df.columns)
        expected_set = set(self.expected_features)

        missing = expected_set - incoming_features
        extra = incoming_features - expected_set

        if missing:
            raise RuntimeError(f"Missing features: {sorted(missing)}")

        if extra:
            raise RuntimeError(f"Unexpected features: {sorted(extra)}")

        for col, (low, high) in self.feature_bounds.items():
            if ((df[col] < low) | (df[col] > high)).any():
                raise RuntimeError(f"Feature {col} out of bounds")

        # RETURN IN TRAINING ORDER
        return df[self.expected_features]