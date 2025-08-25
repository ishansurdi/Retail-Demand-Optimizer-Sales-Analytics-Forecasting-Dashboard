# analytics.py
import pandas as pd
import numpy as np

# -------------------------------
# ROLLING AVERAGE FORECAST
# -------------------------------
def rolling_avg_forecast(df: pd.DataFrame, window: int = 4, col: str = "weekly_sales"):
    """
    Simple rolling average forecasting and anomaly detection.
    """
    df = df.sort_values("date").copy()
    df["Forecast"] = df[col].rolling(window, min_periods=1).mean()
    df["Anomaly"] = df[col] > df["Forecast"] * 1.2  # +20% threshold
    return df

# -------------------------------
# PLACEHOLDER: Prophet Forecast
# -------------------------------
def prophet_forecast(df: pd.DataFrame, periods: int = 12):
    """
    Forecast using Prophet. Return df with predictions and anomaly flags.
    """
    try:
        from prophet import Prophet
        prophet_df = df[["date", "weekly_sales"]].rename(columns={"date": "ds", "weekly_sales": "y"})
        prophet_df = prophet_df.groupby("ds", as_index=False).mean().sort_values("ds")

        m = Prophet(weekly_seasonality=True, daily_seasonality=False, seasonality_mode="multiplicative")
        m.fit(prophet_df)

        future = m.make_future_dataframe(periods=periods, freq='W')
        forecast = m.predict(future)
        forecast['Anomaly'] = (forecast['yhat'] < forecast['yhat_lower']) | (forecast['yhat'] > forecast['yhat_upper'])
        return forecast
    except Exception as e:
        print(f"⚠️ Prophet forecasting failed: {e}")
        return rolling_avg_forecast(df)
