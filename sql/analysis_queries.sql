USE retail_optimizer;


-- ============================================
-- Retail Demand Optimizer: Analysis Queries
-- Author: Ishan Rahul Surdi
-- ============================================

-- =====================================================
-- 1. Top 10 Products by Revenue (Superstore)
-- =====================================================
WITH product_revenue AS (
    SELECT 
        product_id,
        product_name,
        category,
        sub_category,
        SUM(sales) AS total_sales,
        SUM(profit) AS total_profit,
        COUNT(DISTINCT order_id) AS order_count
    FROM superstore_sales
    GROUP BY product_id, product_name, category, sub_category
)
SELECT *
FROM product_revenue
ORDER BY total_sales DESC
LIMIT 10;

-- =====================================================
-- 2. Revenue Contribution per Region (Superstore)
-- =====================================================
WITH region_revenue AS (
    SELECT
        region,
        SUM(sales) AS total_sales,
        SUM(profit) AS total_profit
    FROM superstore_sales
    GROUP BY region
)
SELECT region, total_sales, total_profit,
       ROUND(total_sales / SUM(total_sales) OVER() * 100, 2) AS sales_pct
FROM region_revenue
ORDER BY total_sales DESC;

-- =====================================================
-- 3. Monthly Sales Trend (Superstore)
-- =====================================================
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS yearmonth,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    COUNT(DISTINCT order_id) AS order_count
FROM superstore_sales
GROUP BY yearmonth
ORDER BY yearmonth;

-- =====================================================
-- 4. Customer Segmentation: Top 10 High-Value Customers (Superstore)
-- =====================================================
WITH customer_revenue AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        SUM(sales) AS total_sales,
        SUM(profit) AS total_profit,
        COUNT(DISTINCT order_id) AS order_count
    FROM superstore_sales
    GROUP BY customer_id, customer_name, segment
)
SELECT *
FROM customer_revenue
ORDER BY total_sales DESC
LIMIT 10;

-- =====================================================
-- 5. Detect Anomalous Sales Weeks (Walmart)
-- =====================================================
-- Using Z-score method on weekly sales per store & dept
WITH stats AS (
    SELECT 
        store,
        dept,
        AVG(weekly_sales) AS avg_sales,
        STDDEV(weekly_sales) AS std_sales
    FROM walmart_sales_train
    GROUP BY store, dept
)
SELECT 
    w.store,
    w.dept,
    w.date,
    w.weekly_sales,
    s.avg_sales,
    s.std_sales,
    ROUND((w.weekly_sales - s.avg_sales)/s.std_sales, 2) AS z_score
FROM walmart_sales_train w
JOIN stats s
ON w.store = s.store AND w.dept = s.dept
WHERE ABS((w.weekly_sales - s.avg_sales)/s.std_sales) > 2 -- threshold for anomaly
ORDER BY store, dept, date;

-- =====================================================
-- 6. Holiday Impact Analysis (Walmart)
-- =====================================================
SELECT 
    WEEK(date, 1) AS week_number,
    SUM(weekly_sales) AS total_weekly_sales,
    SUM(CASE WHEN is_holiday = 1 THEN weekly_sales ELSE 0 END) AS holiday_sales,
    ROUND(SUM(CASE WHEN is_holiday = 1 THEN weekly_sales ELSE 0 END) / SUM(weekly_sales) * 100, 2) AS holiday_pct
FROM walmart_sales_train
GROUP BY week_number
ORDER BY week_number;

-- =====================================================
-- 7. Store-Level Sales Performance (Walmart)
-- =====================================================
SELECT 
    s.store,
    st.type AS store_type,
    SUM(w.weekly_sales) AS total_sales,
    AVG(w.weekly_sales) AS avg_weekly_sales,
    COUNT(DISTINCT w.date) AS weeks_count
FROM walmart_sales_train w
JOIN walmart_stores st ON w.store = st.store
GROUP BY s.store, st.type
ORDER BY total_sales DESC;

-- =====================================================
-- 8. Category-Level Insights (Superstore)
-- =====================================================
SELECT 
    category,
    sub_category,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2) AS profit_margin_pct
FROM superstore_sales
GROUP BY category, sub_category
ORDER BY total_sales DESC;

-- =====================================================
-- 9. Product Performance by Region (Superstore)
-- =====================================================
SELECT 
    region,
    product_id,
    product_name,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM superstore_sales
GROUP BY region, product_id, product_name
ORDER BY region, total_sales DESC;

-- =====================================================
-- 10. Forecast-Ready Aggregation: Weekly Walmart Sales per Store
-- =====================================================
SELECT 
    store,
    DATE_FORMAT(date, '%Y-%u') AS year_week,
    SUM(weekly_sales) AS total_weekly_sales,
    MAX(is_holiday) AS has_holiday
FROM walmart_sales_train
GROUP BY store, year_week
ORDER BY store, year_week;
