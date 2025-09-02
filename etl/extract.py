#!/usr/bin/env python3
"""
Data Extraction module for Retail ETL Pipeline
Handles reading CSV files and initial data validation
"""

import pandas as pd
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataExtractor:
    """Handles data extraction from various sources"""
    
    def __init__(self, data_path='./raw/'):
        self.data_path = data_path
        
    def extract_csv(self, filename='retail_sales_transactions.csv'):
        """Extract data from CSV file"""
        
        file_path = os.path.join(self.data_path, filename)
        
        try:
            logger.info(f"Extracting data from {file_path}")
            
            # Read CSV with proper data types
            df = pd.read_csv(file_path, dtype={
                'transaction_id': 'string',
                'customer_id': 'string',
                'product_id': 'string',
                'product_name': 'string',
                'category': 'string',
                'quantity': 'int64',
                'unit_price': 'float64',
                'total_amount': 'float64',
                'transaction_date': 'string',
                'transaction_time': 'string',
                'store_id': 'string',
                'store_location': 'string',
                'payment_method': 'string'
            })
            
            logger.info(f"✅ Successfully extracted {len(df):,} records")
            return df
            
        except FileNotFoundError:
            logger.error(f"❌ File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"❌ Error extracting data: {e}")
            raise
    
    def validate_raw_data(self, df):
        """Perform initial validation on raw data"""
        
        logger.info("🔍 Validating raw data...")
        
        validation_results = {
            'total_records': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_transactions': df['transaction_id'].duplicated().sum(),
            'date_range': {
                'min_date': df['transaction_date'].min(),
                'max_date': df['transaction_date'].max()
            },
            'negative_quantities': (df['quantity'] < 0).sum(),
            'zero_prices': (df['unit_price'] <= 0).sum(),
            'categories': df['category'].unique().tolist(),
            'stores': df['store_id'].unique().tolist()
        }
        
        # Log validation results
        logger.info(f"📊 Validation Results:")
        logger.info(f"   Total records: {validation_results['total_records']:,}")
        logger.info(f"   Missing values: {sum(validation_results['missing_values'].values())}")
        logger.info(f"   Duplicate transactions: {validation_results['duplicate_transactions']}")
        logger.info(f"   Negative quantities: {validation_results['negative_quantities']}")
        logger.info(f"   Zero/negative prices: {validation_results['zero_prices']}")
        logger.info(f"   Date range: {validation_results['date_range']['min_date']} to {validation_results['date_range']['max_date']}")
        logger.info(f"   Categories: {len(validation_results['categories'])}")
        logger.info(f"   Stores: {len(validation_results['stores'])}")
        
        return validation_results
    
    def extract_and_validate(self, filename='retail_sales_transactions.csv'):
        """Extract data and perform validation"""
        
        df = self.extract_csv(filename)
        validation_results = self.validate_raw_data(df)
        
        return df, validation_results

if __name__ == "__main__":
    # Test the extractor
    extractor = DataExtractor()
    
    try:
        df, validation = extractor.extract_and_validate()
        print(f"\n🎉 Extraction completed successfully!")
        print(f"Extracted {len(df):,} records for processing")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        print("Make sure to generate sample data first: python data/generate_sample_data.py")
