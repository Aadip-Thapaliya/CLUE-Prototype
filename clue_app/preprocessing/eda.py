# preprocessing/eda.py
from typing import Dict, Any
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
    plt.close("all")

    fig, axes = plt.subplots(
        4, 1,
        figsize=(14, 18),
        constrained_layout=True
    )

    # Price + Rolling Mean
    df["Close"].plot(ax=axes[0], label="Close", color="cyan")
    df["Close"].rolling(20).mean().plot(ax=axes[0], label="Rolling Mean (20)", color="magenta")
    axes[0].set_title("Price with Rolling Mean")
    axes[0].legend()
    axes[0].grid(True)

    # Returns Histogram
    returns = df["Close"].pct_change().dropna()
    axes[1].hist(returns, bins=60, color="purple", alpha=0.7)
    axes[1].set_title("Distribution of Daily Returns")
    axes[1].grid(True)

    # Rolling Volatility
    volatility = returns.rolling(20).std()
    axes[2].plot(volatility, color="orange")
    axes[2].set_title("Rolling Volatility (20)")
    axes[2].grid(True)

    # Cumulative Returns
    cumulative = (1 + returns).cumprod()
    axes[3].plot(cumulative, color="lime")
    axes[3].set_title("Cumulative Returns")
    axes[3].grid(True)

    for ax in axes:
        ax.set_xlabel("Date")

    fig.tight_layout(pad=4)
    return fig
def generate_preview_charts(df):
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))

    ax.plot(df["Close"], label="Close Price")
    ax.plot(df["Close"].rolling(20).mean(), label="Rolling Mean (20)")
    ax.set_title("Raw Price Preview (Before Cleaning)")
    ax.legend()
    ax.grid(True)

    return fig
