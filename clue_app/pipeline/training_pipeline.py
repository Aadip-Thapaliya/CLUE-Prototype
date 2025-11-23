from typing import Dict

from core.data_loader import load_financial_data
from preprocessing.feature_engineering import create_features
from preprocessing.split import time_series_train_test_split
from models.evaluation import evaluate_model

from forecasting.auto_arima import train_auto_arima
from forecasting.xgboost_model import train_xgboost_model, predict_xgboost


def run_training(model_type: str, source_config: Dict, forecast_periods: int = 30) -> Dict:
    """
    Trains selected model and returns training results.
    """

    df = load_financial_data(**source_config)
    close_series = df["Close"]

    result = {"model_type": model_type}

    # ================= AUTO ARIMA =================
    if model_type == "AUTO_ARIMA":

        model = train_auto_arima(close_series)

        in_sample_pred = model.predict_in_sample()
        y_true = close_series[-len(in_sample_pred):]

        metrics = evaluate_model(y_true, in_sample_pred)

        result.update({
            "model_order": model.order,
            "metrics": metrics
        })

    # ================= XGBOOST =================
    elif model_type == "XGBOOST":

        featured_df = create_features(df)
        X_train, X_test, y_train, y_test = time_series_train_test_split(featured_df)

        model = train_xgboost_model(X_train, y_train)
        predictions = predict_xgboost(model, X_test)

        metrics = evaluate_model(y_test, predictions)

        result.update({
            "model_params": model.get_params(),
            "metrics": metrics
        })

    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    return result
