#!/usr/bin/env python3
"""
Generate sample retail sales data for testing the ETL pipeline
Creates realistic transaction data with various products, customers, and stores
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_sample_data(num_transactions=10000):
    """Generate sample retail sales transaction data"""
    
    # Product categories and names
    categories = {
        'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smart Watch', 'Camera'],
        'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes', 'Hat'],
        'Home & Garden': ['Coffee Maker', 'Vacuum Cleaner', 'Plant Pot', 'Lamp', 'Cushion', 'Rug'],
        'Food & Beverage': ['Coffee Beans', 'Organic Milk', 'Bread', 'Pasta', 'Wine', 'Chocolate'],
        'Books & Media': ['Novel', 'Cookbook', 'Magazine', 'DVD', 'Board Game', 'Puzzle'],
        'Sports & Outdoors': ['Running Shoes', 'Yoga Mat', 'Tennis Racket', 'Bicycle', 'Camping Tent', 'Water Bottle']
    }
    
    # Store locations
    stores = [
        {'store_id': 'ST001', 'location': 'New York, NY'},
        {'store_id': 'ST002', 'location': 'Los Angeles, CA'},
        {'store_id': 'ST003', 'location': 'Chicago, IL'},
        {'store_id': 'ST004', 'location': 'Houston, TX'},
        {'store_id': 'ST005', 'location': 'Phoenix, AZ'},
        {'store_id': 'ST006', 'location': 'Philadelphia, PA'}
    ]
    
    # Payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet', 'Gift Card']
    
    # Generate transactions
    transactions = []
    
    # Generate customer IDs (reuse some customers for realistic patterns)
    customer_pool = [f'CUST{str(i).zfill(4)}' for i in range(1, 2001)]  # 2000 unique customers
    
    for _ in range(num_transactions):
        # Select random category and product
        category = random.choice(list(categories.keys()))
        product_name = random.choice(categories[category])
        
        # Generate product ID
        product_id = f'PROD{random.randint(1000, 9999)}'
        
        # Select customer (with some customers appearing more frequently)
        customer_id = random.choices(
            customer_pool,
            weights=[1 if i < 1500 else 3 for i in range(len(customer_pool))]  # Some customers buy more
        )[0]
        
        # Generate transaction details
        quantity = random.randint(1, 5)
        
        # Price varies by category
        price_ranges = {
            'Electronics': (50, 1500),
            'Clothing': (15, 200),
            'Home & Garden': (20, 300),
            'Food & Beverage': (5, 50),
            'Books & Media': (10, 60),
            'Sports & Outdoors': (25, 400)
        }
        
        unit_price = round(random.uniform(*price_ranges[category]), 2)
        total_amount = round(quantity * unit_price, 2)
        
        # Generate transaction date (last 12 months)
        start_date = datetime.now() - timedelta(days=365)
        random_days = random.randint(0, 365)
        transaction_date = start_date + timedelta(days=random_days)
        
        # Generate transaction time
        transaction_time = f"{random.randint(8, 21):02d}:{random.randint(0, 59):02d}:00"
        
        # Select store and payment method
        store = random.choice(stores)
        payment_method = random.choice(payment_methods)
        
        transaction = {
            'transaction_id': str(uuid.uuid4())[:8].upper(),
            'customer_id': customer_id,
            'product_id': product_id,
            'product_name': product_name,
            'category': category,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_amount': total_amount,
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'transaction_time': transaction_time,
            'store_id': store['store_id'],
            'store_location': store['location'],
            'payment_method': payment_method
        }
        
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def add_data_quality_issues(df, corruption_rate=0.05):
    """Add some data quality issues to make the dataset more realistic"""
    
    df_copy = df.copy()
    num_corruptions = int(len(df_copy) * corruption_rate)
    
    for _ in range(num_corruptions):
        row_idx = random.randint(0, len(df_copy) - 1)
        issue_type = random.choice(['missing_customer', 'negative_quantity', 'zero_price', 'future_date'])
        
        if issue_type == 'missing_customer':
            df_copy.loc[row_idx, 'customer_id'] = None
        elif issue_type == 'negative_quantity':
            df_copy.loc[row_idx, 'quantity'] = -1
        elif issue_type == 'zero_price':
            df_copy.loc[row_idx, 'unit_price'] = 0
        elif issue_type == 'future_date':
            future_date = datetime.now() + timedelta(days=30)
            df_copy.loc[row_idx, 'transaction_date'] = future_date.strftime('%Y-%m-%d')
    
    return df_copy

if __name__ == "__main__":
    print("Generating sample retail sales data...")
    
    # Generate clean dataset
    df_clean = generate_sample_data(10000)
    
    # Add some data quality issues
    df_with_issues = add_data_quality_issues(df_clean, corruption_rate=0.03)
    
    # Create data directories
    import os
    os.makedirs('raw', exist_ok=True)
    os.makedirs('processed', exist_ok=True)
    
    # Save datasets
    df_with_issues.to_csv('raw/retail_sales_transactions.csv', index=False)
    df_clean.to_csv('processed/retail_sales_clean.csv', index=False)
    
    print(f"Generated {len(df_with_issues):,} transactions")
    print(f"Saved to raw/retail_sales_transactions.csv")
    print(f"Clean version saved to processed/retail_sales_clean.csv")
    
    # Display sample data
    print("\nSample data preview:")
    print(df_with_issues.head())
    
    print("\nData summary:")
    print(f"Date range: {df_with_issues['transaction_date'].min()} to {df_with_issues['transaction_date'].max()}")
    print(f"Total revenue: ${df_with_issues['total_amount'].sum():,.2f}")
    print(f"Unique customers: {df_with_issues['customer_id'].nunique():,}")
    print(f"Unique products: {df_with_issues['product_id'].nunique():,}")
    print(f"Categories: {', '.join(df_with_issues['category'].unique())}")
