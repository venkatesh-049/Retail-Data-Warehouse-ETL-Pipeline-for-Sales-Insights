#!/usr/bin/env python3
"""
Data Loading module for Retail ETL Pipeline
Handles loading transformed data into PostgreSQL database
"""

import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import logging
from config.database_config import get_database_engine, get_connection_params

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataLoader:
    """Handles loading data into PostgreSQL database"""
    
    def __init__(self):
        self.engine = get_database_engine()
        self.db_params = get_connection_params()
    
    def load_raw_transactions(self, df):
        """Load raw transactions into the database"""
        
        logger.info("📥 Loading raw transactions...")
        
        try:
            # Prepare data for loading
            df_load = df.copy()
            
            # Ensure proper data types
            df_load['transaction_date'] = pd.to_datetime(df_load['transaction_date'])
            
            # Load to database using direct MySQL connection
            conn = mysql.connector.connect(**self.db_params)
            cursor = conn.cursor()
            
            # Drop and recreate table
            cursor.execute("DROP TABLE IF EXISTS raw_transactions")
            
            # Create table with proper schema
            create_table_sql = """
            CREATE TABLE raw_transactions (
                transaction_id VARCHAR(255),
                customer_id VARCHAR(255),
                product_id VARCHAR(255),
                product_name VARCHAR(255),
                category VARCHAR(255),
                quantity INT,
                unit_price DECIMAL(10,2),
                total_amount DECIMAL(10,2),
                transaction_date DATE,
                transaction_time TIME,
                store_id VARCHAR(255),
                store_location VARCHAR(255),
                payment_method VARCHAR(255)
            )
            """
            cursor.execute(create_table_sql)
            
            # Insert data in batches
            insert_sql = """
            INSERT INTO raw_transactions 
            (transaction_id, customer_id, product_id, product_name, category, 
             quantity, unit_price, total_amount, transaction_date, transaction_time, 
             store_id, store_location, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Convert DataFrame to list of tuples, handling NaN values
            data_tuples = []
            for _, row in df_load.iterrows():
                data_tuples.append((
                    str(row['transaction_id']) if pd.notna(row['transaction_id']) else None,
                    str(row['customer_id']) if pd.notna(row['customer_id']) else None,
                    str(row['product_id']) if pd.notna(row['product_id']) else None,
                    str(row['product_name']) if pd.notna(row['product_name']) else None,
                    str(row['category']) if pd.notna(row['category']) else None,
                    int(row['quantity']) if pd.notna(row['quantity']) else None,
                    float(row['unit_price']) if pd.notna(row['unit_price']) else None,
                    float(row['total_amount']) if pd.notna(row['total_amount']) else None,
                    row['transaction_date'].date() if pd.notna(row['transaction_date']) else None,
                    str(row['transaction_time']) if pd.notna(row['transaction_time']) else None,
                    str(row['store_id']) if pd.notna(row['store_id']) else None,
                    str(row['store_location']) if pd.notna(row['store_location']) else None,
                    str(row['payment_method']) if pd.notna(row['payment_method']) else None
                ))
            
            # Execute batch insert
            cursor.executemany(insert_sql, data_tuples)
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Loaded {len(df_load):,} raw transactions")
            
        except Exception as e:
            logger.error(f"❌ Error loading raw transactions: {e}")
            raise
    
    def load_transactions(self, df):
        """Load processed transactions into the database"""
        
        logger.info("📥 Loading processed transactions...")
        
        try:
            # Prepare data for loading
            df_load = df.copy()
            
            # Select only required columns for the transactions table
            columns_to_load = [
                'transaction_id', 'customer_id', 'product_id', 'product_name',
                'category', 'quantity', 'unit_price', 'total_amount',
                'transaction_date', 'transaction_time', 'store_id', 'store_location',
                'payment_method', 'revenue', 'profit_margin'
            ]
            
            df_load = df_load[columns_to_load]
            
            # Load to database using direct MySQL connection
            conn = mysql.connector.connect(**self.db_params)
            cursor = conn.cursor()
            
            # Drop and recreate table
            cursor.execute("DROP TABLE IF EXISTS transactions")
            
            # Create table with proper schema
            create_table_sql = """
            CREATE TABLE transactions (
                transaction_id VARCHAR(255),
                customer_id VARCHAR(255),
                product_id VARCHAR(255),
                product_name VARCHAR(255),
                category VARCHAR(255),
                quantity INT,
                unit_price DECIMAL(10,2),
                total_amount DECIMAL(10,2),
                transaction_date DATE,
                transaction_time TIME,
                store_id VARCHAR(255),
                store_location VARCHAR(255),
                payment_method VARCHAR(255),
                revenue DECIMAL(10,2),
                profit_margin DECIMAL(10,2)
            )
            """
            cursor.execute(create_table_sql)
            
            # Insert data in batches
            insert_sql = """
            INSERT INTO transactions 
            (transaction_id, customer_id, product_id, product_name, category, 
             quantity, unit_price, total_amount, transaction_date, transaction_time, 
             store_id, store_location, payment_method, revenue, profit_margin)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Convert DataFrame to list of tuples, handling NaN values
            data_tuples = []
            for _, row in df_load.iterrows():
                data_tuples.append((
                    str(row['transaction_id']) if pd.notna(row['transaction_id']) else None,
                    str(row['customer_id']) if pd.notna(row['customer_id']) else None,
                    str(row['product_id']) if pd.notna(row['product_id']) else None,
                    str(row['product_name']) if pd.notna(row['product_name']) else None,
                    str(row['category']) if pd.notna(row['category']) else None,
                    int(row['quantity']) if pd.notna(row['quantity']) else None,
                    float(row['unit_price']) if pd.notna(row['unit_price']) else None,
                    float(row['total_amount']) if pd.notna(row['total_amount']) else None,
                    row['transaction_date'].date() if pd.notna(row['transaction_date']) else None,
                    str(row['transaction_time']) if pd.notna(row['transaction_time']) else None,
                    str(row['store_id']) if pd.notna(row['store_id']) else None,
                    str(row['store_location']) if pd.notna(row['store_location']) else None,
                    str(row['payment_method']) if pd.notna(row['payment_method']) else None,
                    float(row['revenue']) if pd.notna(row['revenue']) else None,
                    float(row['profit_margin']) if pd.notna(row['profit_margin']) else None
                ))
            
            # Execute batch insert
            cursor.executemany(insert_sql, data_tuples)
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Loaded {len(df_load):,} processed transactions")
            
        except Exception as e:
            logger.error(f"❌ Error loading transactions: {e}")
            raise
    
    def load_customers(self, df):
        """Load customer metrics into the database"""
        
        logger.info("👥 Loading customer metrics...")
        
        try:
            df_load = df.copy()
            
            # Load to database using direct MySQL connection
            conn = mysql.connector.connect(**self.db_params)
            cursor = conn.cursor()
            
            # Drop and recreate table
            cursor.execute("DROP TABLE IF EXISTS customers")
            
            # Create table with proper schema
            create_table_sql = """
            CREATE TABLE customers (
                customer_id VARCHAR(255),
                first_transaction_date DATE,
                last_transaction_date DATE,
                total_transactions INT,
                total_revenue DECIMAL(10,2),
                avg_order_value DECIMAL(10,2),
                total_quantity INT,
                customer_segment VARCHAR(50)
            )
            """
            cursor.execute(create_table_sql)
            
            # Insert data in batches
            insert_sql = """
            INSERT INTO customers 
            (customer_id, first_transaction_date, last_transaction_date, total_transactions, 
             total_revenue, avg_order_value, total_quantity, customer_segment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Convert DataFrame to list of tuples, handling NaN values
            data_tuples = []
            for _, row in df_load.iterrows():
                data_tuples.append((
                    str(row['customer_id']) if pd.notna(row['customer_id']) else None,
                    row['first_transaction_date'].date() if pd.notna(row['first_transaction_date']) else None,
                    row['last_transaction_date'].date() if pd.notna(row['last_transaction_date']) else None,
                    int(row['total_transactions']) if pd.notna(row['total_transactions']) else None,
                    float(row['total_revenue']) if pd.notna(row['total_revenue']) else None,
                    float(row['avg_order_value']) if pd.notna(row['avg_order_value']) else None,
                    int(row['total_quantity']) if pd.notna(row['total_quantity']) else None,
                    str(row['customer_segment']) if pd.notna(row['customer_segment']) else None
                ))
            
            # Execute batch insert
            cursor.executemany(insert_sql, data_tuples)
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Loaded {len(df_load):,} customer records")
            
        except Exception as e:
            logger.error(f"❌ Error loading customers: {e}")
            raise
    
    def load_products(self, df):
        """Load product metrics into the database"""
        
        logger.info("📦 Loading product metrics...")
        
        try:
            df_load = df.copy()
            
            # Load to database using direct MySQL connection
            conn = mysql.connector.connect(**self.db_params)
            cursor = conn.cursor()
            
            # Drop and recreate table
            cursor.execute("DROP TABLE IF EXISTS products")
            
            # Create table with proper schema
            create_table_sql = """
            CREATE TABLE products (
                product_id VARCHAR(255),
                product_name VARCHAR(255),
                category VARCHAR(255),
                total_quantity_sold INT,
                total_revenue DECIMAL(10,2),
                avg_unit_price DECIMAL(10,2),
                first_sale_date DATE,
                last_sale_date DATE
            )
            """
            cursor.execute(create_table_sql)
            
            # Insert data in batches
            insert_sql = """
            INSERT INTO products 
            (product_id, product_name, category, total_quantity_sold, total_revenue, 
             avg_unit_price, first_sale_date, last_sale_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Convert DataFrame to list of tuples, handling NaN values
            data_tuples = []
            for _, row in df_load.iterrows():
                data_tuples.append((
                    str(row['product_id']) if pd.notna(row['product_id']) else None,
                    str(row['product_name']) if pd.notna(row['product_name']) else None,
                    str(row['category']) if pd.notna(row['category']) else None,
                    int(row['total_quantity_sold']) if pd.notna(row['total_quantity_sold']) else None,
                    float(row['total_revenue']) if pd.notna(row['total_revenue']) else None,
                    float(row['avg_unit_price']) if pd.notna(row['avg_unit_price']) else None,
                    row['first_sale_date'].date() if pd.notna(row['first_sale_date']) else None,
                    row['last_sale_date'].date() if pd.notna(row['last_sale_date']) else None
                ))
            
            # Execute batch insert
            cursor.executemany(insert_sql, data_tuples)
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Loaded {len(df_load):,} product records")
            
        except Exception as e:
            logger.error(f"❌ Error loading products: {e}")
            raise
    
    def load_monthly_summary(self, df):
        """Load monthly summary into the database"""
        
        logger.info("📅 Loading monthly summary...")
        
        try:
            df_load = df.copy()
            
            # Load to database using direct MySQL connection
            conn = mysql.connector.connect(**self.db_params)
            cursor = conn.cursor()
            
            # Drop and recreate table
            cursor.execute("DROP TABLE IF EXISTS monthly_summary")
            
            # Create table with proper schema
            create_table_sql = """
            CREATE TABLE monthly_summary (
                `year_month` VARCHAR(7),
                total_transactions INT,
                total_revenue DECIMAL(10,2),
                avg_order_value DECIMAL(10,2),
                unique_customers INT
            )
            """
            cursor.execute(create_table_sql)
            
            # Insert data in batches
            insert_sql = """
            INSERT INTO monthly_summary 
            (`year_month`, total_transactions, total_revenue, avg_order_value, unique_customers)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            # Convert DataFrame to list of tuples, handling NaN values
            data_tuples = []
            for _, row in df_load.iterrows():
                data_tuples.append((
                    str(row['year_month']) if pd.notna(row['year_month']) else None,
                    int(row['total_transactions']) if pd.notna(row['total_transactions']) else None,
                    float(row['total_revenue']) if pd.notna(row['total_revenue']) else None,
                    float(row['avg_order_value']) if pd.notna(row['avg_order_value']) else None,
                    int(row['unique_customers']) if pd.notna(row['unique_customers']) else None
                ))
            
            # Execute batch insert
            cursor.executemany(insert_sql, data_tuples)
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Loaded {len(df_load):,} monthly summary records")
            
        except Exception as e:
            logger.error(f"❌ Error loading monthly summary: {e}")
            raise
    
    def verify_load(self):
        """Verify that data was loaded correctly"""
        
        logger.info("🔍 Verifying data load...")
        
        try:
            with self.engine.connect() as conn:
                # Check record counts
                tables = ['raw_transactions', 'transactions', 'customers', 'products', 'monthly_summary']
                
                for table in tables:
                    result = conn.execute(f"SELECT COUNT(*) FROM {table}")
                    count = result.fetchone()[0]
                    logger.info(f"   {table}: {count:,} records")
                
                # Check data quality
                result = conn.execute("SELECT MAX(total_revenue) FROM customers")
                max_customer_revenue = result.fetchone()[0]
                
                result = conn.execute("SELECT MAX(total_revenue) FROM products")
                max_product_revenue = result.fetchone()[0]
                
                result = conn.execute("SELECT SUM(total_revenue) FROM monthly_summary")
                total_revenue = result.fetchone()[0]
                
                logger.info(f"   Max customer revenue: ${max_customer_revenue:,.2f}")
                logger.info(f"   Max product revenue: ${max_product_revenue:,.2f}")
                logger.info(f"   Total revenue: ${total_revenue:,.2f}")
                
                logger.info("✅ Data verification completed successfully")
                
        except Exception as e:
            logger.error(f"❌ Error verifying data load: {e}")
            raise
    
    def load_all_data(self, transformed_data):
        """Load all transformed data into the database"""
        
        logger.info("🚀 Starting data loading process...")
        
        try:
            # Load raw transactions (for audit trail)
            if 'raw_data' in transformed_data:
                self.load_raw_transactions(transformed_data['raw_data'])
            
            # Load processed data
            self.load_transactions(transformed_data['transactions'])
            self.load_customers(transformed_data['customers'])
            self.load_products(transformed_data['products'])
            self.load_monthly_summary(transformed_data['monthly_summary'])
            
            # Verify the load
            self.verify_load()
            
            logger.info("🎉 All data loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Data loading failed: {e}")
            raise

if __name__ == "__main__":
    # Test the loader
    from extract import DataExtractor
    from transform import DataTransformer
    
    try:
        # Extract and transform data
        extractor = DataExtractor()
        df, _ = extractor.extract_and_validate()
        
        transformer = DataTransformer()
        transformed_data = transformer.transform_data(df)
        
        # Add raw data for audit
        transformed_data['raw_data'] = df
        
        # Load data
        loader = DataLoader()
        loader.load_all_data(transformed_data)
        
        print(f"\n🎉 ETL pipeline completed successfully!")
        
    except Exception as e:
        print(f"❌ ETL pipeline failed: {e}")
        print("Make sure PostgreSQL is running and database is set up correctly")
