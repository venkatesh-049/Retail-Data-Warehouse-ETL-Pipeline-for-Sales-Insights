-- Useful SQL queries for Retail Data Warehouse analysis

-- 1. Monthly Sales Trend
SELECT 
    year_month,
    total_revenue,
    total_transactions,
    avg_order_value,
    unique_customers,
    LAG(total_revenue) OVER (ORDER BY year_month) as prev_month_revenue,
    ROUND(
        ((total_revenue - LAG(total_revenue) OVER (ORDER BY year_month)) / 
         LAG(total_revenue) OVER (ORDER BY year_month)) * 100, 2
    ) as revenue_growth_pct
FROM sales.monthly_summary
ORDER BY year_month;

-- 2. Top 10 Customers by Revenue
SELECT 
    customer_id,
    total_revenue,
    total_transactions,
    avg_order_value,
    customer_segment,
    ROUND((total_revenue / (SELECT SUM(total_revenue) FROM sales.customers)) * 100, 2) as revenue_share_pct
FROM sales.customers
ORDER BY total_revenue DESC
LIMIT 10;

-- 3. High Revenue Products Analysis
SELECT 
    product_name,
    category,
    total_revenue,
    total_quantity_sold,
    avg_unit_price,
    ROUND((total_revenue / (SELECT SUM(total_revenue) FROM sales.products)) * 100, 2) as revenue_share_pct
FROM sales.products
ORDER BY total_revenue DESC
LIMIT 10;

-- 4. Category Performance Analysis
SELECT 
    category,
    COUNT(*) as product_count,
    SUM(total_revenue) as category_revenue,
    AVG(total_revenue) as avg_product_revenue,
    SUM(total_quantity_sold) as total_quantity,
    ROUND(AVG(avg_unit_price), 2) as avg_category_price
FROM sales.products
GROUP BY category
ORDER BY category_revenue DESC;

-- 5. Customer Segmentation Analysis
SELECT 
    customer_segment,
    COUNT(*) as customer_count,
    SUM(total_revenue) as segment_revenue,
    AVG(total_revenue) as avg_customer_revenue,
    AVG(total_transactions) as avg_transactions_per_customer,
    AVG(avg_order_value) as avg_order_value
FROM sales.customers
GROUP BY customer_segment
ORDER BY segment_revenue DESC;

-- 6. Daily Sales Pattern
SELECT 
    EXTRACT(DOW FROM transaction_date) as day_of_week,
    CASE EXTRACT(DOW FROM transaction_date)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as day_name,
    COUNT(*) as transaction_count,
    SUM(revenue) as daily_revenue,
    AVG(revenue) as avg_transaction_value
FROM sales.transactions
GROUP BY EXTRACT(DOW FROM transaction_date)
ORDER BY day_of_week;

-- 7. Store Performance Comparison
SELECT 
    store_id,
    store_location,
    COUNT(*) as transaction_count,
    SUM(revenue) as store_revenue,
    AVG(revenue) as avg_transaction_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales.transactions
GROUP BY store_id, store_location
ORDER BY store_revenue DESC;

-- 8. Product Performance by Category
WITH category_stats AS (
    SELECT 
        category,
        product_name,
        total_revenue,
        total_quantity_sold,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_revenue DESC) as rank_in_category
    FROM sales.products
)
SELECT 
    category,
    product_name,
    total_revenue,
    total_quantity_sold,
    rank_in_category
FROM category_stats
WHERE rank_in_category <= 3
ORDER BY category, rank_in_category;

-- 9. Customer Lifetime Value Analysis
SELECT 
    customer_id,
    total_revenue as lifetime_value,
    total_transactions,
    EXTRACT(DAYS FROM (last_transaction_date - first_transaction_date)) as customer_lifespan_days,
    CASE 
        WHEN EXTRACT(DAYS FROM (last_transaction_date - first_transaction_date)) > 0 
        THEN ROUND(total_revenue / EXTRACT(DAYS FROM (last_transaction_date - first_transaction_date)), 2)
        ELSE total_revenue
    END as daily_value
FROM sales.customers
WHERE total_transactions > 1
ORDER BY lifetime_value DESC
LIMIT 20;

-- 10. Revenue Trend by Payment Method
SELECT 
    payment_method,
    COUNT(*) as transaction_count,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_transaction_value,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales.transactions)), 2) as usage_percentage
FROM sales.transactions
GROUP BY payment_method
ORDER BY total_revenue DESC;

-- 11. Seasonal Analysis (Monthly Comparison)
SELECT 
    EXTRACT(MONTH FROM transaction_date) as month_num,
    TO_CHAR(transaction_date, 'Month') as month_name,
    COUNT(*) as transaction_count,
    SUM(revenue) as monthly_revenue,
    AVG(revenue) as avg_transaction_value
FROM sales.transactions
GROUP BY EXTRACT(MONTH FROM transaction_date), TO_CHAR(transaction_date, 'Month')
ORDER BY month_num;

-- 12. Customer Retention Analysis
WITH customer_months AS (
    SELECT 
        customer_id,
        TO_CHAR(transaction_date, 'YYYY-MM') as year_month,
        SUM(revenue) as monthly_spend
    FROM sales.transactions
    GROUP BY customer_id, TO_CHAR(transaction_date, 'YYYY-MM')
),
customer_activity AS (
    SELECT 
        year_month,
        COUNT(DISTINCT customer_id) as active_customers,
        SUM(monthly_spend) as monthly_revenue
    FROM customer_months
    GROUP BY year_month
)
SELECT 
    year_month,
    active_customers,
    monthly_revenue,
    LAG(active_customers) OVER (ORDER BY year_month) as prev_month_customers,
    CASE 
        WHEN LAG(active_customers) OVER (ORDER BY year_month) > 0 
        THEN ROUND(((active_customers - LAG(active_customers) OVER (ORDER BY year_month)) * 100.0 / LAG(active_customers) OVER (ORDER BY year_month)), 2)
        ELSE 0
    END as customer_growth_pct
FROM customer_activity
ORDER BY year_month;
