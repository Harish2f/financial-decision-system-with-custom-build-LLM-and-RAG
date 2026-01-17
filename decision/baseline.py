import numpy as np
import pandas as pd


class BaselineRiskModel:
    """
    Finance-approved deterministic baseline.

    Rules:
    - Risky if avg_days_late > 15
    - OR unpaid_balance > 10,000

    This model must remain:
    - Stateless
    - Deterministic
    - Schema-validated
    """

    REQUIRED_COLUMNS = {
        "avg_days_late",
        "total_billed",
        "total_paid",
    }

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        self._validate_schema(df)

        avg_days_late = self._safe_float(df["avg_days_late"])
        total_billed = self._safe_float(df["total_billed"])
        total_paid = self._safe_float(df["total_paid"])

        unpaid = total_billed - total_paid

        risk = (avg_days_late > 15) | (unpaid > 10_000)

        # Return int8 for storage efficiency + consistency
        return risk.astype(np.int8)

    @staticmethod
    def _safe_float(series: pd.Series) -> pd.Series:
        """
        Converts input to float safely.
        Non-convertible values become 0.
        """
        return (
            pd.to_numeric(series, errors="coerce")
            .fillna(0.0)
            .astype(float)
        )

    def _validate_schema(self, df: pd.DataFrame) -> None:
        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(
                f"BaselineRiskModel missing required columns: {missing}"
            )