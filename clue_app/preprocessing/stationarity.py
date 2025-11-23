"""
Stationarity Module for CLUE Financial Forecasting
Handles ADF test and automatic differencing logic
for univariate financial time series (Close price).
"""

import pandas as pd
from statsmodels.tsa.stattools import adfuller


class StationarityChecker:
    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level

    # -------------------- PUBLIC METHODS --------------------

    def adf_test(self, series: pd.Series) -> dict:
        """Performs Augmented Dickey-Fuller test."""
        result = adfuller(series.dropna())

        return {
            "adf_statistic": result[0],
            "p_value": result[1],
            "used_lag": result[2],
            "n_obs": result[3],
            "critical_values": result[4],
            "is_stationary": result[1] < self.significance_level,
        }

    def make_stationary(self, df: pd.DataFrame, target_column: str = "Close") -> pd.DataFrame:
        """Applies differencing until stationarity is achieved."""
        series = df[target_column]
        differenced = series.copy()
        diff_count = 0

        while True:
            test_result = self.adf_test(differenced)
            if test_result["is_stationary"]:
                break
            differenced = differenced.diff().dropna()
            diff_count += 1

        stationary_df = differenced.to_frame(name=target_column)
        stationary_df.attrs["differencing_order"] = diff_count

        return stationary_df


# -------------------- GUI FRIENDLY FUNCTION --------------------

def check_stationarity(df: pd.DataFrame, column: str = "Close") -> dict:
    checker = StationarityChecker()
    return checker.adf_test(df[column])


def transform_to_stationary(df: pd.DataFrame, column: str = "Close") -> pd.DataFrame:
    checker = StationarityChecker()
    return checker.make_stationary(df, column)