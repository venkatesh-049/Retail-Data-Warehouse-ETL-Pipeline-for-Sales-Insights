#!/usr/bin/env python3
"""
Data Transformation module for Retail ETL Pipeline
Handles data cleaning, validation, and KPI calculations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataTransformer:
    """Handles data transformation and cleaning"""
    
    def __init__(self):
        self.profit_margins = {
            'Electronics': 0.15,
            'Clothing': 0.45,
            'Home & Garden': 0.35,
            'Food & Beverage': 0.25,
            'Books & Media': 0.40,
            'Sports & Outdoors': 0.30
        }
    
    def clean_data(self, df):
        """Clean and validate the raw data"""
        
        logger.info("🧹 Cleaning data...")
        
        df_clean = df.copy()
        initial_count = len(df_clean)
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates(subset=['transaction_id'])
        logger.info(f"   Removed {initial_count - len(df_clean)} duplicate transactions")
        
        # Handle missing values
        missing_customers = df_clean['customer_id'].isnull().sum()
        df_clean = df_clean.dropna(subset=['customer_id'])
        logger.info(f"   Removed {missing_customers} records with missing customer_id")
        
        # Fix data quality issues
        # Remove negative quantities
        negative_qty = (df_clean['quantity'] < 0).sum()
        df_clean = df_clean[df_clean['quantity'] > 0]
        logger.info(f"   Removed {negative_qty} records with negative quantities")
        
        # Remove zero or negative prices
        invalid_prices = (df_clean['unit_price'] <= 0).sum()
        df_clean = df_clean[df_clean['unit_price'] > 0]
        logger.info(f"   Removed {invalid_prices} records with invalid prices")
        
        # Convert date columns
        df_clean['transaction_date'] = pd.to_datetime(df_clean['transaction_date'])
        df_clean['transaction_time'] = pd.to_datetime(df_clean['transaction_time'], format='%H:%M:%S').dt.time
        
        # Remove future dates
        today = datetime.now().date()
        future_dates = (df_clean['transaction_date'].dt.date > today).sum()
        df_clean = df_clean[df_clean['transaction_date'].dt.date <= today]
        logger.info(f"   Removed {future_dates} records with future dates")
        
        # Recalculate total_amount to ensure consistency
        df_clean['total_amount'] = df_clean['quantity'] * df_clean['unit_price']
        
        logger.info(f"✅ Data cleaning completed. {len(df_clean):,} records remaining")
        
        return df_clean
    
    def add_calculated_fields(self, df):
        """Add calculated fields and KPIs"""
        
        logger.info("📊 Adding calculated fields...")
        
        df_enhanced = df.copy()
        
        # Add revenue (same as total_amount for this case)
        df_enhanced['revenue'] = df_enhanced['total_amount']
        
        # Add profit margin based on category
        df_enhanced['profit_margin'] = df_enhanced['category'].map(self.profit_margins)
        
        # Add date components
        df_enhanced['year'] = df_enhanced['transaction_date'].dt.year
        df_enhanced['month'] = df_enhanced['transaction_date'].dt.month
        df_enhanced['day_of_week'] = df_enhanced['transaction_date'].dt.day_name()
        df_enhanced['year_month'] = df_enhanced['transaction_date'].dt.strftime('%Y-%m')
        
        # Add hour from transaction_time
        df_enhanced['hour'] = pd.to_datetime(df_enhanced['transaction_time'].astype(str)).dt.hour
        
        logger.info("✅ Calculated fields added successfully")
        
        return df_enhanced
    
    def calculate_customer_metrics(self, df):
        """Calculate customer-level metrics"""
        
        logger.info("👥 Calculating customer metrics...")
        
        customer_metrics = df.groupby('customer_id').agg({
            'transaction_date': ['min', 'max', 'count'],
            'revenue': ['sum', 'mean'],
            'quantity': 'sum'
        }).round(2)
        
        # Flatten column names
        customer_metrics.columns = [
            'first_transaction_date', 'last_transaction_date', 'total_transactions',
            'total_revenue', 'avg_order_value', 'total_quantity'
        ]
        
        # Add customer segmentation
        customer_metrics['customer_segment'] = pd.cut(
            customer_metrics['total_revenue'],
            bins=[0, 100, 500, 1000, float('inf')],
            labels=['Bronze', 'Silver', 'Gold', 'Platinum']
        )
        
        customer_metrics = customer_metrics.reset_index()
        
        logger.info(f"✅ Customer metrics calculated for {len(customer_metrics):,} customers")
        
        return customer_metrics
    
    def calculate_product_metrics(self, df):
        """Calculate product-level metrics"""
        
        logger.info("📦 Calculating product metrics...")
        
        product_metrics = df.groupby(['product_id', 'product_name', 'category']).agg({
            'quantity': 'sum',
            'revenue': 'sum',
            'unit_price': 'mean',
            'transaction_date': ['min', 'max']
        }).round(2)
        
        # Flatten column names
        product_metrics.columns = [
            'total_quantity_sold', 'total_revenue', 'avg_unit_price',
            'first_sale_date', 'last_sale_date'
        ]
        
        product_metrics = product_metrics.reset_index()
        
        logger.info(f"✅ Product metrics calculated for {len(product_metrics):,} products")
        
        return product_metrics
    
    def calculate_monthly_summary(self, df):
        """Calculate monthly summary metrics"""
        
        logger.info("📅 Calculating monthly summary...")
        
        monthly_summary = df.groupby('year_month').agg({
            'transaction_id': 'count',
            'revenue': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique',
            'product_id': 'nunique'
        }).round(2)
        
        monthly_summary.columns = [
            'total_transactions', 'total_revenue', 'total_quantity',
            'unique_customers', 'unique_products'
        ]
        
        # Calculate average order value
        monthly_summary['avg_order_value'] = (
            monthly_summary['total_revenue'] / monthly_summary['total_transactions']
        ).round(2)
        
        monthly_summary = monthly_summary.reset_index()
        
        logger.info(f"✅ Monthly summary calculated for {len(monthly_summary)} months")
        
        return monthly_summary
    
    def get_top_customers(self, customer_metrics, top_n=10):
        """Get top N customers by revenue"""
        
        top_customers = customer_metrics.nlargest(top_n, 'total_revenue')
        
        logger.info(f"🏆 Top {top_n} customers by revenue:")
        for idx, customer in top_customers.iterrows():
            logger.info(f"   {customer['customer_id']}: ${customer['total_revenue']:,.2f}")
        
        return top_customers
    
    def get_high_revenue_products(self, product_metrics, top_n=10):
        """Get top N products by revenue"""
        
        top_products = product_metrics.nlargest(top_n, 'total_revenue')
        
        logger.info(f"🏆 Top {top_n} products by revenue:")
        for idx, product in top_products.iterrows():
            logger.info(f"   {product['product_name']}: ${product['total_revenue']:,.2f}")
        
        return top_products
    
    def transform_data(self, df):
        """Main transformation pipeline"""
        
        logger.info("🔄 Starting data transformation pipeline...")
        
        # Step 1: Clean data
        df_clean = self.clean_data(df)
        
        # Step 2: Add calculated fields
        df_enhanced = self.add_calculated_fields(df_clean)
        
        # Step 3: Calculate aggregated metrics
        customer_metrics = self.calculate_customer_metrics(df_enhanced)
        product_metrics = self.calculate_product_metrics(df_enhanced)
        monthly_summary = self.calculate_monthly_summary(df_enhanced)
        
        # Step 4: Get top performers
        top_customers = self.get_top_customers(customer_metrics)
        top_products = self.get_high_revenue_products(product_metrics)
        
        logger.info("✅ Data transformation completed successfully")
        
        return {
            'transactions': df_enhanced,
            'customers': customer_metrics,
            'products': product_metrics,
            'monthly_summary': monthly_summary,
            'top_customers': top_customers,
            'top_products': top_products
        }

if __name__ == "__main__":
    # Test the transformer
    from extract import DataExtractor
    
    try:
        # Extract data
        extractor = DataExtractor()
        df, _ = extractor.extract_and_validate()
        
        # Transform data
        transformer = DataTransformer()
        transformed_data = transformer.transform_data(df)
        
        print(f"\n🎉 Transformation completed successfully!")
        print(f"Processed {len(transformed_data['transactions']):,} transactions")
        print(f"Generated metrics for {len(transformed_data['customers']):,} customers")
        print(f"Generated metrics for {len(transformed_data['products']):,} products")
        
    except Exception as e:
        print(f"❌ Transformation failed: {e}")
        print("Make sure to generate sample data first: python data/generate_sample_data.py")
