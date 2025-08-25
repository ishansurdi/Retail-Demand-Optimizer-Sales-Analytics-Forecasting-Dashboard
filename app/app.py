# app.py
import streamlit as st
import pandas as pd

from data_access import fetch_query
from analytics import rolling_avg_forecast, prophet_forecast
from charts import line_forecast_chart, bar_sales_chart
from insights import show_superstore_insights, show_walmart_insights, show_forecast_insights

st.set_page_config(page_title="Retail Demand Optimizer", layout="wide")

st.title("📊 Retail Demand Optimizer Dashboard")

# ===============================
# DATASET SELECTION
# ===============================
dataset_choice = st.sidebar.selectbox("Select Dataset", ["Superstore", "Walmart"])
action_choice = st.sidebar.selectbox("Select Action", ["View Data", "EDA", "Forecast & Anomaly Detection"])

# ===============================
# FETCH DATA
# ===============================
if dataset_choice == "Superstore":
    df = fetch_query("SELECT * FROM superstore_sales LIMIT 5000")  # sample for performance
    show_superstore_insights(df)
else:
    df = fetch_query("SELECT * FROM walmart_train")
    show_walmart_insights(df, df_features)
    show_forecast_insights(forecast, store_id)

# ===============================
# VIEW DATA
# ===============================
if action_choice == "View Data":
    st.subheader(f"{dataset_choice} - Raw Data")
    st.dataframe(df)

# ===============================
# EDA
# ===============================
elif action_choice == "EDA":
    st.subheader(f"{dataset_choice} - Exploratory Data Analysis")

    st.markdown("### Basic Info")
    st.write(df.info())

    st.markdown("### Summary Statistics")
    st.write(df.describe())

    st.markdown("### Top 10 Records")
    st.dataframe(df.head(10))

    if dataset_choice == "Walmart":
        st.markdown("### Weekly Sales Distribution")
        fig = bar_sales_chart(df, x_col="date", y_col="weekly_sales")
        st.plotly_chart(fig)

# ===============================
# FORECAST & ANOMALY DETECTION
# ===============================
elif action_choice == "Forecast & Anomaly Detection":
    st.subheader(f"{dataset_choice} Forecast & Anomaly Detection")

    if dataset_choice == "Superstore":
        st.info("Forecasting is only implemented for Walmart dataset due to weekly sales structure.")
    else:
        store_id = st.selectbox("Select Store for Forecasting", df['store'].unique())
        store_sales = df[df['store'] == store_id].sort_values('date')
        store_sales = store_sales.dropna(subset=['date', 'weekly_sales'])

        if len(store_sales) < 10:
            st.warning(f"Not enough data for forecasting Store {store_id}")
        else:
            # -------------------------------
            # FORECAST
            # -------------------------------
            st.info(f"Running forecast for Store {store_id}...")

            forecast_df = None
            try:
                forecast_df = prophet_forecast(store_sales)
            except Exception as e:
                st.error(f"Prophet forecasting failed for Store {store_id}: {e}")
                forecast_df = rolling_avg_forecast(store_sales)

            # -------------------------------
            # PLOT FORECAST
            # -------------------------------
            st.markdown("### Forecast Plot")
            fig1 = line_forecast_chart(forecast_df, date_col='date' if 'date' in forecast_df else 'ds',
                                       y_col='weekly_sales' if 'weekly_sales' in forecast_df else 'yhat',
                                       anomaly_col='anomaly')
            st.plotly_chart(fig1)

            # -------------------------------
            # SHOW DATA
            # -------------------------------
            st.markdown("### Forecast Data Sample")
            st.dataframe(forecast_df.tail(10))
