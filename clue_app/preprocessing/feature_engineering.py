"""
Feature Engineering Module for CLUE Financial Forecasting
Handles generation of features for univariate financial time series.
Designed for AutoML pipeline and GUI integration.
"""

import pandas as pd


class FeatureEngineer:
    def __init__(self, target_column: str = "Close"):
        self.target_column = target_column

    # -------------------- PUBLIC METHODS --------------------

    def generate_features(
        self,
        df: pd.DataFrame,
        lags: int = 5,
        rolling_windows: list = [7, 14, 30],
        include_time_features: bool = True,
    ) -> pd.DataFrame:
        """Main entry point for feature generation."""
        df = df.copy()
        df = self._create_lag_features(df, lags)
        df = self._create_rolling_features(df, rolling_windows)

        if include_time_features:
            df = self._create_time_features(df)

        df = df.dropna()
        return df

    # -------------------- LAG FEATURES --------------------

    def _create_lag_features(self, df: pd.DataFrame, lags: int) -> pd.DataFrame:
        for lag in range(1, lags + 1):
            df[f"lag_{lag}"] = df[self.target_column].shift(lag)
        return df

    # -------------------- ROLLING FEATURES --------------------

    def _create_rolling_features(self, df: pd.DataFrame, windows: list) -> pd.DataFrame:
        for window in windows:
            df[f"rolling_mean_{window}"] = df[self.target_column].rolling(window).mean()
            df[f"rolling_std_{window}"] = df[self.target_column].rolling(window).std()
        return df

    # -------------------- TIME FEATURES --------------------

    def _create_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("DataFrame index must be DatetimeIndex for time features")

        df["day"] = df.index.day
        df["month"] = df.index.month
        df["year"] = df.index.year
        df["day_of_week"] = df.index.dayofweek
        df["quarter"] = df.index.quarter

        return df


# -------------------- GUI FRIENDLY FUNCTION --------------------

def create_features(
    df: pd.DataFrame,
    lags: int = 5,
    rolling_windows: list = [7, 14, 30],
    include_time_features: bool = True,
    target_column: str = "Close",
) -> pd.DataFrame:
    engineer = FeatureEngineer(target_column)
    return engineer.generate_features(df, lags, rolling_windows, include_time_features)
