import numpy as np

class InferenceGuard:
    def __init__(self, expected_features, feature_bounds):
        # KEEP ORDER — DO NOT USE SET
        self.expected_features = list(expected_features)
        self.expected_feature_set = set(expected_features)
        self.feature_bounds = feature_bounds

    def validate(self, df):
        incoming_features = set(df.columns)

        missing = self.expected_feature_set - incoming_features
        extra = incoming_features - self.expected_feature_set

        if missing:
            raise RuntimeError(f"Missing features: {sorted(missing)}")

        if extra:
            raise RuntimeError(f"Unexpected features: {sorted(extra)}")

        # --- VALUE VALIDATION ---
        for col, (low, high) in self.feature_bounds.items():
            if ((df[col] < low) | (df[col] > high)).any():
                raise RuntimeError(f"Feature {col} out of bounds")

        # --- RETURN IN TRAINING ORDER ---
        return df[self.expected_features]
    