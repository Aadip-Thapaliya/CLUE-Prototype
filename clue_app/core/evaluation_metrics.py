import numpy as np
from sklearn.metrics import r2_score


def calculate_evaluation_metrics(y_true, y_pred):
    """
    Comprehensive evaluation metrics for forecasting models.
    Returns 15 professional-grade performance indicators.
    """

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    residuals = y_true - y_pred

    # ---------- Core Error Metrics ----------
    mae = np.mean(np.abs(residuals))
    mse = np.mean(residuals ** 2)
    rmse = np.sqrt(mse)

    # Prevent divide by zero
    safe_true = np.where(y_true == 0, 1e-8, y_true)

    mape = np.mean(np.abs(residuals / safe_true)) * 100
    smape = np.mean(2.0 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred) + 1e-8)) * 100
    wape = np.sum(np.abs(residuals)) / (np.sum(np.abs(y_true)) + 1e-8) * 100

    # ---------- Goodness of Fit ----------
    r2 = r2_score(y_true, y_pred)

    # ---------- Forecast Stability ----------
    bias = np.mean(residuals)

    # MASE
    if len(y_true) > 1:
        naive_forecast = np.roll(y_true, 1)
        naive_errors = np.abs(y_true[1:] - naive_forecast[1:])
        mase = mae / (np.mean(naive_errors) + 1e-8)
    else:
        mase = np.nan

    # ---------- Residual Distribution ----------
    residual_mean = np.mean(residuals)
    residual_std = np.std(residuals) + 1e-8

    skewness = np.mean((residuals - residual_mean) ** 3) / residual_std ** 3
    kurtosis = np.mean((residuals - residual_mean) ** 4) / residual_std ** 4

    # ---------- Direction Accuracy ----------
    if len(y_true) > 1:
        direction_actual = np.sign(np.diff(y_true))
        direction_pred = np.sign(np.diff(y_pred))
        directional_accuracy = np.mean(direction_actual == direction_pred) * 100
    else:
        directional_accuracy = np.nan

    # ---------- Confidence Score ----------
    confidence_score = max(0, 100 - mape)

    # ---------- Volatility Error Ratio ----------
    actual_volatility = np.std(np.diff(y_true))
    pred_volatility = np.std(np.diff(y_pred))
    volatility_error_ratio = pred_volatility / (actual_volatility + 1e-8)

    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "MAPE": mape,
        "SMAPE": smape,
        "WAPE": wape,
        "R2": r2,
        "MASE": mase,
        "Bias": bias,
        "Skewness": skewness,
        "Kurtosis": kurtosis,
        "Directional Accuracy": directional_accuracy,
        "Confidence Score": confidence_score,
        "Volatility Error Ratio": volatility_error_ratio
    }
