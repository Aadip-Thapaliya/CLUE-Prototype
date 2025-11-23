"""
Data Loader for CLUE Financial Forecasting Application
Handles:
- CSV file loading
- Yahoo Finance data fetching
- Column validation (Date & Close)
- Standardized DataFrame output for GUI + ML pipelines
"""

import pandas as pd
import yfinance as yf
from pathlib import Path
from typing import Optional


class DataLoader:
    def __init__(self, date_column: str = "Date", target_column: str = "Close"):
        self.date_column = date_column
        self.target_column = target_column

    # -------------------- PUBLIC METHODS --------------------

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load and validate local CSV file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(path)
        return self._process_dataframe(df)

    def load_yahoo_finance(self, ticker: str, start: str, end: Optional[str] = None) -> pd.DataFrame:
        df = yf.download(ticker, start=start, end=end, auto_adjust=True)

        if df.empty:
            raise ValueError("No data returned from Yahoo Finance")

        # Fix MultiIndex column issue from Yahoo Finance
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        if self.target_column not in df.columns:
            raise ValueError("Close column not found in Yahoo Finance data")

        return self._process_dataframe(df)



    # -------------------- CORE PROCESSING --------------------

    def _process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardizes dataframe for univariate financial forecasting."""
        df = self._validate_required_columns(df)
        df = self._format_datetime(df)
        df = self._sort_by_date(df)
        df = self._clean_missing_values(df)
        df = self._set_datetime_index(df)

        return df[[self.target_column]]

    # -------------------- VALIDATION --------------------

    def _validate_required_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.date_column not in df.columns or self.target_column not in df.columns:
            raise ValueError(
                f"Required columns missing. Expected: '{self.date_column}' and '{self.target_column}'"
            )
        return df

    # -------------------- CLEANING --------------------

    def _format_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.date_column] = pd.to_datetime(df[self.date_column], errors="coerce")
        if df[self.date_column].isnull().any():
            raise ValueError("Invalid date values detected")
        return df

    def _sort_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.sort_values(by=self.date_column)

    def _clean_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[[self.date_column, self.target_column]]
        df.loc[:, self.target_column] = pd.to_numeric(df[self.target_column].astype(float), errors="coerce")
        df = df.dropna()
        return df

    def _set_datetime_index(self, df: pd.DataFrame) -> pd.DataFrame:
        df.set_index(self.date_column, inplace=True)
        df.index.name = "Date"
        return df


# -------------------- GUI FRIENDLY FUNCTION --------------------

def load_financial_data(
    source: str,
    file_path: Optional[str] = None,
    ticker: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> pd.DataFrame:
    """
    Unified loader for GUI use.
    source: 'csv' or 'yahoo'
    """
    loader = DataLoader()

    if source == "csv":
        if not file_path:
            raise ValueError("file_path is required for CSV source")
        return loader.load_csv(file_path)

    elif source == "yahoo":
        if not ticker or not start:
            raise ValueError("ticker and start date required for Yahoo Finance")
        return loader.load_yahoo_finance(ticker, start, end)

    else:
        raise ValueError("Invalid source type. Use 'csv' or 'yahoo'")
