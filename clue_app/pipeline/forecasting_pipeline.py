from typing import Dict

from core.data_loader import load_financial_data
from forecasting.auto_arima import train_auto_arima
from forecasting.xgboost_model import train_xgboost_model, predict_xgboost
from preprocessing.feature_engineering import create_features


def run_forecast(model_type: str, source_config: Dict, forecast_periods: int = 30):
    df = load_financial_data(**source_config)
    close_series = df["Close"]

    if model_type == "AUTO_ARIMA":
        model = train_auto_arima(close_series)
        forecast, conf_int = model.forecast(forecast_periods)

        return {
            "model_type": model_type,
            "forecast": forecast,
            "confidence_intervals": conf_int,
        }

    elif model_type == "XGBOOST":
        df_features = create_features(df)
        model = train_xgboost_model(df_features)
        forecast = predict_xgboost(model, df_features, forecast_periods)

        return {
            "model_type": model_type,
            "forecast": forecast,
            "confidence_intervals": None,
        }

    else:
        raise ValueError(f"Unsupported model: {model_type}")
