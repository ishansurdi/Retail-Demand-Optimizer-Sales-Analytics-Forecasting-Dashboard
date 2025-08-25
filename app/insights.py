# insights.py
import streamlit as st
import pandas as pd

def show_superstore_insights(df_superstore):
    st.subheader("📊 Superstore Dataset Insights")

    # Top categories by sales
    top_categories = df_superstore.groupby('category')['sales'].sum().sort_values(ascending=False)
    st.markdown(f"**Top Categories by Sales:** {top_categories.index[0]} leads with total sales ${top_categories.iloc[0]:,.2f}")

    # Profitability vs Discount
    discount_profit = df_superstore.groupby(pd.cut(df_superstore['discount'], bins=[-0.01,0.1,0.2,0.3,1]))['profit'].mean()
    st.markdown("**Discount Impact on Profit:**")
    st.table(discount_profit.reset_index().rename(columns={'discount':'Discount Range', 'profit':'Average Profit'}))

    # Regional performance
    region_sales = df_superstore.groupby('region')[['sales', 'profit']].sum()
    st.markdown("**Regional Performance:**")
    st.table(region_sales)

    st.markdown("**Insights:**")
    st.markdown("""
    - Furniture generates highest revenue, but Office Supplies sell in the highest quantity.
    - Orders with discount > 20% often show negative profit, indicating over-discounting may hurt margins.
    - West region generates highest sales but with lower margins than East region.
    """)


def show_walmart_insights(df_walmart_sales, df_walmart_features):
    st.subheader("📊 Walmart Dataset Insights")

    # Weekly sales overview
    weekly_sales_summary = df_walmart_sales.groupby('date')['weekly_sales'].sum()
    st.markdown("**Weekly Sales Summary:**")
    st.line_chart(weekly_sales_summary)

    # Store performance
    store_sales_summary = df_walmart_sales.groupby('store')['weekly_sales'].sum().sort_values(ascending=False)
    st.markdown(f"**Top Performing Store:** Store {store_sales_summary.index[0]} with total sales ${store_sales_summary.iloc[0]:,.2f}")

    # Correlation with numeric features
    numeric_features = ['temperature', 'fuel_price', 'cpi', 'unemployment', 
                        'markdown1', 'markdown2', 'markdown3', 'markdown4', 'markdown5']
    corr = df_walmart_features[numeric_features].corrwith(df_walmart_sales.groupby('date')['weekly_sales'].sum())
    st.markdown("**Correlation of Features with Weekly Sales:**")
    st.table(corr.reset_index().rename(columns={0:'Correlation', 'index':'Feature'}))

    st.markdown("**Insights:**")
    st.markdown("""
    - Sales spike during holidays like Thanksgiving and Christmas.
    - Store 1 consistently outperforms other stores, indicating location or size advantages.
    - Fuel prices and CPI slightly negatively correlate with weekly sales.
    - Markdown promotions increase short-term sales but need careful planning to avoid profit loss.
    - Anomalies detected in sales highlight unexpected dips or spikes which require operational investigation.
    """)


def show_forecast_insights(forecast_df, store_id):
    st.subheader(f"📈 Forecast & Anomalies - Store {store_id}")

    # Anomalies
    anomalies = forecast_df[forecast_df['Anomaly']]
    st.markdown(f"**Detected Anomalies:** {len(anomalies)} weeks flagged as anomalies.")
    st.dataframe(anomalies[['ds','yhat','yhat_lower','yhat_upper']])

    st.markdown("**Insights:**")
    st.markdown("""
    - Weeks where actual sales fall outside predicted confidence intervals are flagged as anomalies.
    - Forecast indicates expected sales trend; deviations may suggest supply chain issues, local events, or promotional impacts.
    - Rolling average fallback ensures short-term planning even if Prophet optimization fails.
    """)
