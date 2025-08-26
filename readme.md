# Retail Demand Optimizer: Sales Analytics & Forecasting Dashboard

## Overview

Retail Demand Optimizer is a comprehensive analytics and forecasting dashboard for retail sales data, designed to help businesses optimize inventory, detect anomalies, and forecast future demand. The solution supports two major datasets—Superstore and Walmart—and provides interactive visualizations, advanced analytics, and machine learning-based forecasting.

## Features

- **Interactive Dashboard**: Built with Streamlit for real-time data exploration and visualization.
- **Multi-Dataset Support**: Analyze both Superstore and Walmart sales data.
- **Exploratory Data Analysis (EDA)**: Automated summary statistics, distribution plots, and top product/category insights.
- **Sales Forecasting**: Uses Prophet and rolling average models for weekly sales prediction.
- **Anomaly Detection**: Identifies outliers in sales trends using statistical and ML methods.
- **Database Integration**: MySQL backend for scalable data storage and querying.
- **Custom Charts**: Dynamic line and bar charts with anomaly highlighting (Plotly).
- **Insight Generation**: Automated business insights for sales, profit, discount impact, and feature correlations.

## Project Structure

```
RetailDemandOptimizer/
│
├── app/                  # Streamlit dashboard and core modules
│   ├── app.py            # Main dashboard logic
│   ├── analytics.py      # Forecasting and anomaly detection
│   ├── charts.py         # Custom chart functions (Plotly)
│   ├── data_access.py    # Database connection and query helpers
│   ├── insights.py       # Automated business insights
│
├── data/                 # Raw CSV datasets
│   ├── superstore.csv
│   ├── stores.csv
│   ├── features.csv
│   ├── train.csv
│   ├── test.csv
│   ├── sampleSubmission.csv
│
├── scripts/              # Data loading scripts
│   └── load_data.py      # Bulk import to MySQL
│
├── notebooks/            # Jupyter notebooks for EDA & modeling
│   ├── eda.ipynb
│   └── anomaly_forecasting.ipynb
│
├── sql/                  # SQL schema and analysis queries
│   ├── schema.sql
│   └── analysis_queries.sql
│
├── PowerBi - SalesReport.pdf
├── SalesReport.pbix
├── readme.md
└── ...
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- MySQL Server
- [Streamlit](https://streamlit.io/)
- [Prophet](https://facebook.github.io/prophet/)
- [Plotly](https://plotly.com/python/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- Other Python packages: pandas, numpy, matplotlib, seaborn, scipy, mysql-connector-python

### 2. Install Python Dependencies

```powershell
pip install streamlit pandas numpy matplotlib seaborn scipy plotly prophet sqlalchemy mysql-connector-python
```

### 3. Database Setup

- Create a MySQL database named `retail_optimizer`.
- Run the schema in `sql/schema.sql` to create required tables.
- Update database credentials in `app/data_access.py` and `scripts/load_data.py` as needed.

### 4. Load Data

Run the data loading script to import CSVs into MySQL:

```powershell
python scripts/load_data.py
```

### 5. Launch the Dashboard

```powershell
streamlit run app/app.py
```

## Usage

- **Dataset Selection**: Choose between Superstore and Walmart datasets in the sidebar.
- **Actions**:
  - *View Data*: Explore raw data tables.
  - *EDA*: View summary statistics, distributions, and top products/categories.
  - *Forecast & Anomaly Detection*: Run sales forecasts and highlight anomalies for selected stores.

## Notebooks

- `notebooks/eda.ipynb`: In-depth exploratory analysis of both datasets.
- `notebooks/anomaly_forecasting.ipynb`: Advanced anomaly detection and forecasting experiments.

## Key Modules

- **app.py**: Orchestrates dashboard UI, dataset selection, and action routing.
- **analytics.py**: Implements rolling average and Prophet-based forecasting, anomaly detection.
- **charts.py**: Generates interactive Plotly charts for sales and forecasts.
- **data_access.py**: Handles MySQL connections and query execution via SQLAlchemy.
- **insights.py**: Extracts actionable insights from sales, profit, discount, and feature correlations.

## Data Sources

- **Superstore**: Sample retail sales data with order, product, and customer details.
- **Walmart**: Weekly sales, store features, and holiday indicators for multiple stores.

## Business Insights

- Top categories and products by sales and profit.
- Impact of discounts on profitability.
- Regional and store-level performance analysis.
- Feature correlations (e.g., fuel price, CPI, markdowns) with sales.
- Detection of sales anomalies for operational investigation.
- Forecasting for inventory and demand planning.

## Power BI Integration

- `PowerBi - SalesReport.pdf` and `SalesReport.pbix` provide additional business intelligence dashboards for executive reporting.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact [project owner](mailto:ishansurdi@gmail.com).
