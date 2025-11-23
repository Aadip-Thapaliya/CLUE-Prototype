# preprocessing/eda.py
import pandas as pd
from typing import Dict, Any


def basic_stats(df: pd.DataFrame, target_column: str = "Close") -> Dict[str, Any]:
    series = df[target_column]

    return {
        "start_date": df.index.min(),
        "end_date": df.index.max(),
        "n_observations": len(df),
        "min": float(series.min()),
        "max": float(series.max()),
        "mean": float(series.mean()),
        "median": float(series.median()),
        "std": float(series.std()),
    }


def missing_values_summary(df: pd.DataFrame) -> Dict[str, int]:
    return df.isna().sum().to_dict()


def returns_stats(df: pd.DataFrame, target_column: str = "Close") -> Dict[str, Any]:
    series = df[target_column]
    returns = series.pct_change().dropna()

    if returns.empty:
        return {
            "mean_daily_return": None,
            "volatility": None,
            "min_return": None,
            "max_return": None,
        }

    return {
        "mean_daily_return": float(returns.mean()),
        "volatility": float(returns.std()),
        "min_return": float(returns.min()),
        "max_return": float(returns.max()),
    }


def eda_summary(df: pd.DataFrame, target_column: str = "Close") -> Dict[str, Any]:
    """Single call EDA summary for GUI."""
    return {
        "basic_stats": basic_stats(df, target_column),
        "missing_values": missing_values_summary(df),
        "returns_stats": returns_stats(df, target_column),
    }
import matplotlib.pyplot as plt

def generate_eda_charts(df):
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))

    # Price line
    axs[0].plot(df.index, df["Close"])
    axs[0].set_title("Price History")

    # Returns
    returns = df["Close"].pct_change().dropna()
    axs[1].hist(returns, bins=30)
    axs[1].set_title("Daily Returns Distribution")

    # Rolling Mean
    df["RollingMean"] = df["Close"].rolling(20).mean()
    axs[2].plot(df.index, df["Close"], label="Close")
    axs[2].plot(df.index, df["RollingMean"], label="Rolling Mean (20)")
    axs[2].legend()

    plt.tight_layout()
    return fig
