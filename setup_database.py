#!/usr/bin/env python3
"""
Database setup script for Retail Data Warehouse (MySQL)
Creates database, schema, and initial tables
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the retail_warehouse database if it doesn't exist"""
    
    # Connect to MySQL server (not specific database)
    conn_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password')
    }
    
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SHOW DATABASES LIKE 'retail_warehouse'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute('CREATE DATABASE retail_warehouse')
            print("Database 'retail_warehouse' created successfully")
        else:
            print("Database 'retail_warehouse' already exists")
            
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error creating database: {e}")
        return False
    
    return True

def setup_schema():
    """Execute the schema creation SQL"""
    
    conn_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'database': 'retail_warehouse',
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password')
    }
    
    try:
        conn = mysql.connector.connect(**conn_params)
        cursor = conn.cursor()
        
        # Read and execute schema SQL
        with open('sql/create_schema_simple.sql', 'r') as file:
            schema_sql = file.read()
        
        # Execute multiple statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        for statement in statements:
            cursor.execute(statement)
        
        conn.commit()
        
        print("Database schema created successfully")
        print("Tables created: raw_transactions, transactions, customers, products, monthly_summary")
        print("Views created: top_customers, top_products")
        print("Indexes created for performance optimization")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error setting up schema: {e}")
        return False
    
    return True

def verify_setup():
    """Verify the database setup"""
    
    conn_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'database': 'retail_warehouse',
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password')
    }
    
    try:
        conn = mysql.connector.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\nFound {len(tables)} tables in retail_warehouse database:")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error verifying setup: {e}")
        return False

if __name__ == "__main__":
    print("Setting up Retail Data Warehouse (MySQL)...")
    print("=" * 50)
    
    # Step 1: Create database
    if create_database():
        # Step 2: Setup schema
        if setup_schema():
            # Step 3: Verify setup
            if verify_setup():
                print("\nDatabase setup completed successfully!")
                print("\nNext steps:")
                print("1. Copy .env.example to .env and update with your credentials")
                print("2. Run the ETL pipeline: python etl_pipeline.py")
            else:
                print("\nSetup verification failed")
        else:
            print("\nSchema setup failed")
    else:
        print("\nDatabase creation failed")
