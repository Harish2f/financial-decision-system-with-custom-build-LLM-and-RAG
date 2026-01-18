import numpy as np
import warnings

class DriftMonitor:
    def __init__(self, reference_df, threshold=0.2):
        self.reference = reference_df
        self.threshold = threshold

    def psi(self, expected, actual, bins=10):
        eps = 1e-6
        quantiles = np.linspace(0, 1, bins + 1)
        cuts = np.quantile(expected, quantiles)

        expected_hist, _ = np.histogram(expected, cuts)
        actual_hist, _ = np.histogram(actual, cuts)

        expected_pct = expected_hist / (expected_hist.sum() + eps)
        actual_pct = actual_hist / (actual_hist.sum() + eps)

        return np.sum(
            (actual_pct - expected_pct)
            * np.log((actual_pct + eps) / (expected_pct + eps))
        )

    def check(self, df):
        drift_report = {}

        for col in self.reference.columns:
            psi_value = self.psi(
                self.reference[col].values,
                df[col].values,
            )
            drift_report[col] = psi_value

            warnings.warn(
    f"[DRIFT WARNING] {col} PSI={psi_value:.3f}",
    UserWarning
)

        return drift_report