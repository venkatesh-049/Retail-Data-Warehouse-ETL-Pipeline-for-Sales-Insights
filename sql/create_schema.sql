-- Create retail warehouse database schema
CREATE SCHEMA IF NOT EXISTS sales;

-- Raw sales transactions table
CREATE TABLE IF NOT EXISTS sales.raw_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    transaction_date DATE,
    transaction_time TIME,
    store_id VARCHAR(50),
    store_location VARCHAR(200),
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cleaned and processed transactions
CREATE TABLE IF NOT EXISTS sales.transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    transaction_date DATE,
    transaction_time TIME,
    store_id VARCHAR(50),
    store_location VARCHAR(200),
    payment_method VARCHAR(50),
    revenue DECIMAL(10,2),
    profit_margin DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer dimension table
CREATE TABLE IF NOT EXISTS sales.customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_transaction_date DATE,
    last_transaction_date DATE,
    total_transactions INTEGER DEFAULT 0,
    total_revenue DECIMAL(12,2) DEFAULT 0,
    avg_order_value DECIMAL(10,2) DEFAULT 0,
    customer_segment VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product dimension table
CREATE TABLE IF NOT EXISTS sales.products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    total_quantity_sold INTEGER DEFAULT 0,
    total_revenue DECIMAL(12,2) DEFAULT 0,
    avg_unit_price DECIMAL(10,2) DEFAULT 0,
    first_sale_date DATE,
    last_sale_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Monthly sales summary
CREATE TABLE IF NOT EXISTS sales.monthly_summary (
    year_month VARCHAR(7) PRIMARY KEY, -- Format: YYYY-MM
    total_transactions INTEGER,
    total_revenue DECIMAL(12,2),
    total_quantity INTEGER,
    unique_customers INTEGER,
    unique_products INTEGER,
    avg_order_value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Top customers view
CREATE OR REPLACE VIEW sales.top_customers AS
SELECT 
    customer_id,
    total_revenue,
    total_transactions,
    avg_order_value,
    customer_segment,
    RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
FROM sales.customers
ORDER BY total_revenue DESC;

-- Top products view
CREATE OR REPLACE VIEW sales.top_products AS
SELECT 
    product_id,
    product_name,
    category,
    total_revenue,
    total_quantity_sold,
    avg_unit_price,
    RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
FROM sales.products
ORDER BY total_revenue DESC;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_transactions_date ON sales.transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_customer ON sales.transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_product ON sales.transactions(product_id);
CREATE INDEX IF NOT EXISTS idx_customers_revenue ON sales.customers(total_revenue DESC);
CREATE INDEX IF NOT EXISTS idx_products_revenue ON sales.products(total_revenue DESC);
