CREATE DATABASE IF NOT EXISTS retail_warehouse;
USE retail_warehouse;

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
