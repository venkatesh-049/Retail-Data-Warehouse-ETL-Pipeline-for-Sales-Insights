-- Create retail warehouse database schema for MySQL
CREATE DATABASE IF NOT EXISTS retail_warehouse;
USE retail_warehouse;

-- Raw sales transactions table
CREATE TABLE IF NOT EXISTS raw_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    quantity INT,
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
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    quantity INT,
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Customer dimension table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_transaction_date DATE,
    last_transaction_date DATE,
    total_transactions INT DEFAULT 0,
    total_revenue DECIMAL(12,2) DEFAULT 0,
    avg_order_value DECIMAL(10,2) DEFAULT 0,
    customer_segment VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Product dimension table
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    total_quantity_sold INT DEFAULT 0,
    total_revenue DECIMAL(12,2) DEFAULT 0,
    avg_unit_price DECIMAL(10,2) DEFAULT 0,
    first_sale_date DATE,
    last_sale_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Monthly sales summary
CREATE TABLE IF NOT EXISTS monthly_summary (
    year_month VARCHAR(7) PRIMARY KEY,
    total_transactions INT,
    total_revenue DECIMAL(12,2),
    total_quantity INT,
    unique_customers INT,
    unique_products INT,
    avg_order_value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Top customers view
CREATE OR REPLACE VIEW top_customers AS
SELECT 
    customer_id,
    total_revenue,
    total_transactions,
    avg_order_value,
    customer_segment,
    RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
FROM customers
ORDER BY total_revenue DESC;

-- Top products view
CREATE OR REPLACE VIEW top_products AS
SELECT 
    product_id,
    product_name,
    category,
    total_revenue,
    total_quantity_sold,
    avg_unit_price,
    RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
FROM products
ORDER BY total_revenue DESC;

-- Create indexes for better performance
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_product ON transactions(product_id);
CREATE INDEX idx_customers_revenue ON customers(total_revenue DESC);
CREATE INDEX idx_products_revenue ON products(total_revenue DESC);
