#!/usr/bin/env python3
"""
Main ETL Pipeline for Retail Data Warehouse
Orchestrates the complete Extract, Transform, Load process
"""

import sys
import os
from datetime import datetime
import logging

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from etl.extract import DataExtractor
from etl.transform import DataTransformer
from etl.load import DataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RetailETLPipeline:
    """Main ETL Pipeline orchestrator"""
    
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
        self.start_time = None
        self.end_time = None
    
    def run_pipeline(self, source_file='retail_sales_transactions.csv'):
        """Run the complete ETL pipeline"""
        
        self.start_time = datetime.now()
        logger.info("🚀 Starting Retail Data Warehouse ETL Pipeline")
        logger.info("=" * 60)
        
        try:
            # EXTRACT
            logger.info("📥 EXTRACT Phase")
            logger.info("-" * 30)
            raw_data, validation_results = self.extractor.extract_and_validate(source_file)
            
            # TRANSFORM
            logger.info("\n🔄 TRANSFORM Phase")
            logger.info("-" * 30)
            transformed_data = self.transformer.transform_data(raw_data)
            
            # Add raw data for audit trail
            transformed_data['raw_data'] = raw_data
            
            # LOAD
            logger.info("\n📤 LOAD Phase")
            logger.info("-" * 30)
            self.loader.load_all_data(transformed_data)
            
            # Pipeline completion
            self.end_time = datetime.now()
            duration = self.end_time - self.start_time
            
            logger.info("\n" + "=" * 60)
            logger.info("🎉 ETL PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info(f"⏱️  Total execution time: {duration}")
            logger.info(f"📊 Records processed: {len(raw_data):,}")
            logger.info(f"🏪 Data warehouse updated: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Print summary statistics
            self._print_summary_stats(transformed_data)
            
            return True
            
        except Exception as e:
            self.end_time = datetime.now()
            logger.error(f"❌ ETL Pipeline failed: {e}")
            logger.error(f"⏱️  Failed after: {self.end_time - self.start_time}")
            raise
    
    def _print_summary_stats(self, transformed_data):
        """Print summary statistics from the pipeline"""
        
        logger.info("\n📈 PIPELINE SUMMARY STATISTICS")
        logger.info("-" * 40)
        
        # Transaction stats
        transactions = transformed_data['transactions']
        total_revenue = transactions['revenue'].sum()
        avg_order_value = transactions['revenue'].mean()
        
        logger.info(f"💰 Total Revenue: ${total_revenue:,.2f}")
        logger.info(f"🛒 Average Order Value: ${avg_order_value:.2f}")
        logger.info(f"👥 Unique Customers: {len(transformed_data['customers']):,}")
        logger.info(f"📦 Unique Products: {len(transformed_data['products']):,}")
        logger.info(f"🏪 Stores: {transactions['store_id'].nunique()}")
        logger.info(f"📅 Date Range: {transactions['transaction_date'].min().date()} to {transactions['transaction_date'].max().date()}")
        
        # Top performers
        logger.info(f"\n🏆 TOP PERFORMERS")
        logger.info(f"   Top Customer Revenue: ${transformed_data['customers']['total_revenue'].max():,.2f}")
        logger.info(f"   Top Product Revenue: ${transformed_data['products']['total_revenue'].max():,.2f}")
        
        # Category breakdown
        category_revenue = transactions.groupby('category')['revenue'].sum().sort_values(ascending=False)
        logger.info(f"\n🏷️  CATEGORY PERFORMANCE")
        for category, revenue in category_revenue.head(3).items():
            logger.info(f"   {category}: ${revenue:,.2f}")

def main():
    """Main function to run the ETL pipeline"""
    
    pipeline = RetailETLPipeline()
    
    try:
        # Check if sample data exists, generate if not
        data_file = './data/raw/retail_sales_transactions.csv'
        if not os.path.exists(data_file):
            logger.info("📁 Sample data not found. Generating sample dataset...")
            os.system('python data/generate_sample_data.py')
        
        # Run the pipeline
        success = pipeline.run_pipeline()
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 SUCCESS! Your retail data warehouse is ready!")
            print("=" * 60)
            print("\n📋 NEXT STEPS:")
            print("1. 🗄️  Connect to PostgreSQL to view your data")
            print("2. 📊 Set up Metabase for data visualization")
            print("3. ⏰ Configure Airflow for automated scheduling")
            print("4. 🔍 Explore the sales insights and KPIs")
            print("\n💡 TIP: Check the 'sql/' folder for useful queries!")
            
    except Exception as e:
        print(f"\n❌ Pipeline execution failed: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Ensure PostgreSQL is running")
        print("2. Check database credentials in .env file")
        print("3. Run setup_database.py to initialize the schema")
        sys.exit(1)

if __name__ == "__main__":
    main()
