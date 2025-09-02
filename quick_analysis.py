#!/usr/bin/env python3
"""
Quick Data Analysis Script for Retail Data Warehouse
Generates summary reports and exports data for external visualization
"""

import pandas as pd
import mysql.connector
from config.database_config import get_connection_params
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def connect_to_db():
    """Connect to MySQL database"""
    return mysql.connector.connect(**get_connection_params())

def generate_summary_report():
    """Generate comprehensive summary report"""
    conn = connect_to_db()
    
    print("=" * 60)
    print("RETAIL DATA WAREHOUSE ANALYSIS REPORT")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Overall metrics
    cursor = conn.cursor()
    
    # Total revenue
    cursor.execute("SELECT SUM(total_revenue) FROM monthly_summary")
    total_revenue = cursor.fetchone()[0]
    print(f"Total Revenue: ${total_revenue:,.2f}")
    
    # Customer metrics
    cursor.execute("SELECT COUNT(*), AVG(total_revenue), MAX(total_revenue) FROM customers")
    customer_stats = cursor.fetchone()
    print(f"Total Customers: {customer_stats[0]:,}")
    print(f"Average Customer Value: ${customer_stats[1]:.2f}")
    print(f"Top Customer Value: ${customer_stats[2]:,.2f}")
    
    # Product metrics
    cursor.execute("SELECT COUNT(*), AVG(total_revenue), MAX(total_revenue) FROM products")
    product_stats = cursor.fetchone()
    print(f"Total Products: {product_stats[0]:,}")
    print(f"Average Product Revenue: ${product_stats[1]:.2f}")
    print(f"Top Product Revenue: ${product_stats[2]:,.2f}")
    
    print("\n" + "=" * 60)
    print("CUSTOMER SEGMENTATION ANALYSIS")
    print("=" * 60)
    
    # Customer segmentation
    cursor.execute("""
        SELECT customer_segment, 
               COUNT(*) as customer_count,
               ROUND(AVG(total_revenue), 2) as avg_revenue,
               ROUND(SUM(total_revenue), 2) as total_segment_revenue
        FROM customers 
        GROUP BY customer_segment 
        ORDER BY avg_revenue DESC
    """)
    
    segments = cursor.fetchall()
    for segment in segments:
        print(f"{segment[0]:>10}: {segment[1]:>5} customers | "
              f"Avg: ${segment[2]:>8,.2f} | Total: ${segment[3]:>12,.2f}")
    
    print("\n" + "=" * 60)
    print("TOP PERFORMERS")
    print("=" * 60)
    
    # Top customers
    print("\nTOP 5 CUSTOMERS BY REVENUE:")
    cursor.execute("""
        SELECT customer_id, total_revenue, customer_segment 
        FROM customers 
        ORDER BY total_revenue DESC 
        LIMIT 5
    """)
    
    top_customers = cursor.fetchall()
    for i, customer in enumerate(top_customers, 1):
        print(f"{i}. {customer[0]} - ${customer[1]:,.2f} ({customer[2]})")
    
    # Top products
    print("\nTOP 5 PRODUCTS BY REVENUE:")
    cursor.execute("""
        SELECT product_name, category, total_revenue 
        FROM products 
        ORDER BY total_revenue DESC 
        LIMIT 5
    """)
    
    top_products = cursor.fetchall()
    for i, product in enumerate(top_products, 1):
        print(f"{i}. {product[0]} ({product[1]}) - ${product[2]:,.2f}")
    
    print("\n" + "=" * 60)
    print("MONTHLY TRENDS")
    print("=" * 60)
    
    # Monthly performance
    cursor.execute("""
        SELECT `year_month`, total_transactions, total_revenue, unique_customers
        FROM monthly_summary 
        ORDER BY `year_month`
    """)
    
    monthly_data = cursor.fetchall()
    print(f"{'Month':<10} {'Transactions':<12} {'Revenue':<15} {'Customers':<10}")
    print("-" * 50)
    for month in monthly_data:
        print(f"{month[0]:<10} {month[1]:<12,} ${month[2]:<14,.0f} {month[3]:<10}")
    
    conn.close()
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)

def export_data_for_excel():
    """Export data to CSV files for Excel analysis"""
    conn = connect_to_db()
    
    # Create exports directory
    os.makedirs('exports', exist_ok=True)
    
    tables = {
        'customers': 'SELECT * FROM customers',
        'products': 'SELECT * FROM products LIMIT 1000',
        'monthly_summary': 'SELECT * FROM monthly_summary',
        'transactions_sample': 'SELECT * FROM transactions LIMIT 5000'
    }
    
    print("Exporting data to CSV files...")
    
    for table_name, query in tables.items():
        df = pd.read_sql(query, conn)
        filename = f'exports/{table_name}_{datetime.now().strftime("%Y%m%d")}.csv'
        df.to_csv(filename, index=False)
        print(f"Exported: {filename} ({len(df)} records)")
    
    conn.close()
    print("\nFiles exported to 'exports/' directory")
    print("You can now open these CSV files in Excel for further analysis!")

if __name__ == "__main__":
    print("Starting Retail Data Warehouse Analysis...")
    print("\n1. Generating Summary Report...")
    generate_summary_report()
    
    print("\n2. Exporting Data for Excel...")
    export_data_for_excel()
    
    print("\nAnalysis Complete!")
    print("\nNext steps:")
    print("- Check the 'exports/' folder for CSV files")
    print("- Run 'python quick_analysis.py' anytime for updated reports")
    print("- Use 'run_dashboard.bat' to launch the web dashboard")
