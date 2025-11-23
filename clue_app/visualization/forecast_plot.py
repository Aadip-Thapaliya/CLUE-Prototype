"""
Forecast Visualization for CLUE
Compatible with all pandas versions
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_forecast(df: pd.DataFrame, forecast: pd.Series, conf_int: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot historical prices
    ax.plot(df.index, df["Close"], label="History")

    # Create future index safely (no 'closed' argument)
    future_index = pd.date_range(
        start=df.index[-1] + pd.Timedelta(days=1),
        periods=len(forecast),
        freq="D"
    )

    # Plot forecast
    ax.plot(future_index, forecast.values, label="Forecast")

    # Confidence interval shading
    if conf_int is not None:
        ax.fill_between(
            future_index,
            conf_int["Lower CI"].values,
            conf_int["Upper CI"].values,
            alpha=0.3,
            label="Confidence Interval"
        )

    ax.set_title("Forecast with Confidence Interval")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)

    return fig
