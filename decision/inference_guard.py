import numpy as np

class InferenceGuard:
    def __init__(self, expected_features, feature_bounds):
        self.expected_features = set(expected_features)
        self.feature_bounds = feature_bounds

    def validate(self, df):
        # --- SCHEMA VALIDATION MUST HAPPEN FIRST ---
        incoming_features = set(df.columns)

        missing = self.expected_features - incoming_features
        extra = incoming_features - self.expected_features

        if missing:
            raise RuntimeError(f"Missing features: {sorted(missing)}")

        if extra:
            raise RuntimeError(f"Unexpected features: {sorted(extra)}")

        # --- VALUE VALIDATION ---
        for col, (low, high) in self.feature_bounds.items():
            if ((df[col] < low) | (df[col] > high)).any():
                raise RuntimeError(f"Feature {col} out of bounds")

        # --- ONLY NOW subset & order ---
        return df[list(self.expected_features)]
    