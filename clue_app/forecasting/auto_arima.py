"""
Auto ARIMA Model Module for CLUE Financial Forecasting
Improved version with stronger model search and trend awareness.
"""

import pandas as pd
from typing import Tuple
from pmdarima import auto_arima


class AutoARIMAModel:
    def __init__(self):
        self.model = None
        self.order = None

    # -------------------- TRAINING --------------------

    def fit(self, series: pd.Series):
        """Trains optimized Auto ARIMA model on univariate series."""

        self.model = auto_arima(
            series,
            start_p=0,
            start_q=0,
            max_p=6,
            max_q=6,
            max_d=2,
            seasonal=False,
            trend="t",
            information_criterion="aic",
            stepwise=False,     # deeper search
            suppress_warnings=True,
            error_action="ignore",
            n_jobs=-1
        )

        self.order = self.model.order
        return self

    # -------------------- FORECASTING --------------------

    def forecast(self, periods: int = 30) -> Tuple[pd.Series, pd.DataFrame]:
        """Generates future forecasts with confidence intervals."""
        if self.model is None:
            raise ValueError("Model is not trained yet")

        forecast, conf_int = self.model.predict(
            n_periods=periods,
            return_conf_int=True
        )

        forecast_series = pd.Series(forecast, name="Forecast")
        conf_df = pd.DataFrame(conf_int, columns=["Lower CI", "Upper CI"])

        return forecast_series, conf_df

    # -------------------- EVALUATION --------------------

    def predict_in_sample(self) -> pd.Series:
        """Returns predictions on training data."""
        if self.model is None:
            raise ValueError("Model is not trained yet")

        predictions = self.model.predict_in_sample()
        return pd.Series(predictions, name="Predicted")


# -------------------- GUI FRIENDLY FUNCTIONS --------------------

def train_auto_arima(series: pd.Series) -> AutoARIMAModel:
    model = AutoARIMAModel()
    model.fit(series)
    return model


def generate_forecast(series: pd.Series, periods: int = 30) -> Tuple[pd.Series, pd.DataFrame]:
    model = train_auto_arima(series)
    return model.forecast(periods)
