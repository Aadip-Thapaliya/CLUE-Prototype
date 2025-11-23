"""
Train-Test Split Module for CLUE Financial Forecasting
Ensures time-series safe splitting without data leakage.
Designed for GUI and AutoML pipeline integration.
"""

import pandas as pd
from typing import Tuple


class TimeSeriesSplitter:
    def __init__(self, test_size: float = 0.2):
        if not 0 < test_size < 1:
            raise ValueError("test_size must be between 0 and 1")
        self.test_size = test_size

    # -------------------- PUBLIC METHODS --------------------

    def split(self, df: pd.DataFrame, target_column: str = "Close") -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Splits data into X_train, X_test, y_train, y_test
        preserving time order.
        """
        split_index = int(len(df) * (1 - self.test_size))

        train_df = df.iloc[:split_index]
        test_df = df.iloc[split_index:]

        X_train = train_df.drop(columns=[target_column])
        y_train = train_df[target_column]

        X_test = test_df.drop(columns=[target_column])
        y_test = test_df[target_column]

        return X_train, X_test, y_train, y_test


# -------------------- GUI FRIENDLY FUNCTION --------------------

def time_series_train_test_split(
    df: pd.DataFrame,
    test_size: float = 0.2,
    target_column: str = "Close",
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    splitter = TimeSeriesSplitter(test_size)
    return splitter.split(df, target_column)
