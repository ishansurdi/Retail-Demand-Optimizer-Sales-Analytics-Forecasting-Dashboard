# charts.py
import plotly.graph_objects as go
import pandas as pd

def line_forecast_chart(df: pd.DataFrame, date_col="Date", y_col="Forecast", anomaly_col="Anomaly"):
    """
    Create a line chart for forecast and highlight anomalies.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=df[y_col], mode='lines', name='Forecast'))

    if anomaly_col in df.columns:
        anomalies = df[df[anomaly_col]]
        fig.add_trace(go.Scatter(
            x=anomalies[date_col],
            y=anomalies[y_col] if y_col in anomalies else anomalies[y_col],
            mode='markers',
            marker=dict(color='red', size=8),
            name='Anomalies'
        ))

    fig.update_layout(title="Forecast with Anomalies", xaxis_title="Date", yaxis_title=y_col)
    return fig

def bar_sales_chart(df: pd.DataFrame, x_col="Date", y_col="Weekly_Sales"):
    """
    Simple bar chart for weekly sales.
    """
    fig = go.Figure([go.Bar(x=df[x_col], y=df[y_col])])
    fig.update_layout(title="Weekly Sales", xaxis_title=x_col, yaxis_title=y_col)
    return fig
