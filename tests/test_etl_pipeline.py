#!/usr/bin/env python3
"""
Unit tests for the Retail ETL Pipeline
Tests extraction, transformation, and loading components
"""

import unittest
import pandas as pd
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract import DataExtractor
from etl.transform import DataTransformer
from etl.load import DataLoader

class TestETLPipeline(unittest.TestCase):
    """Test cases for ETL pipeline components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = DataExtractor('./data/raw/')
        self.transformer = DataTransformer()
        
        # Create sample test data
        self.sample_data = pd.DataFrame({
            'transaction_id': ['T001', 'T002', 'T003'],
            'customer_id': ['C001', 'C002', 'C001'],
            'product_id': ['P001', 'P002', 'P003'],
            'product_name': ['Laptop', 'Mouse', 'Keyboard'],
            'category': ['Electronics', 'Electronics', 'Electronics'],
            'quantity': [1, 2, 1],
            'unit_price': [999.99, 25.50, 75.00],
            'total_amount': [999.99, 51.00, 75.00],
            'transaction_date': ['2023-01-15', '2023-01-16', '2023-01-17'],
            'transaction_time': ['10:30:00', '14:15:00', '09:45:00'],
            'store_id': ['ST001', 'ST001', 'ST002'],
            'store_location': ['New York, NY', 'New York, NY', 'Los Angeles, CA'],
            'payment_method': ['Credit Card', 'Debit Card', 'Cash']
        })
    
    def test_data_extraction_validation(self):
        """Test data extraction validation"""
        validation_results = self.extractor.validate_raw_data(self.sample_data)
        
        self.assertEqual(validation_results['total_records'], 3)
        self.assertEqual(validation_results['duplicate_transactions'], 0)
        self.assertIn('Electronics', validation_results['categories'])
    
    def test_data_cleaning(self):
        """Test data cleaning functionality"""
        # Add some dirty data
        dirty_data = self.sample_data.copy()
        dirty_data.loc[3] = ['T004', None, 'P004', 'Monitor', 'Electronics', 
                            -1, 0, 0, '2023-01-18', '11:00:00', 'ST001', 
                            'New York, NY', 'Credit Card']
        
        cleaned_data = self.transformer.clean_data(dirty_data)
        
        # Should remove the dirty record
        self.assertEqual(len(cleaned_data), 3)
        self.assertTrue(all(cleaned_data['quantity'] > 0))
        self.assertTrue(all(cleaned_data['unit_price'] > 0))
    
    def test_calculated_fields(self):
        """Test calculated fields addition"""
        enhanced_data = self.transformer.add_calculated_fields(self.sample_data)
        
        # Check if new fields are added
        self.assertIn('revenue', enhanced_data.columns)
        self.assertIn('profit_margin', enhanced_data.columns)
        self.assertIn('year_month', enhanced_data.columns)
        
        # Check profit margin mapping
        self.assertEqual(enhanced_data.loc[0, 'profit_margin'], 0.15)  # Electronics
    
    def test_customer_metrics_calculation(self):
        """Test customer metrics calculation"""
        enhanced_data = self.transformer.add_calculated_fields(self.sample_data)
        customer_metrics = self.transformer.calculate_customer_metrics(enhanced_data)
        
        # Should have 2 unique customers
        self.assertEqual(len(customer_metrics), 2)
        
        # Customer C001 should have 2 transactions
        c001_metrics = customer_metrics[customer_metrics['customer_id'] == 'C001']
        self.assertEqual(c001_metrics.iloc[0]['total_transactions'], 2)
    
    def test_product_metrics_calculation(self):
        """Test product metrics calculation"""
        enhanced_data = self.transformer.add_calculated_fields(self.sample_data)
        product_metrics = self.transformer.calculate_product_metrics(enhanced_data)
        
        # Should have 3 unique products
        self.assertEqual(len(product_metrics), 3)
        
        # Check if all required columns exist
        required_columns = ['product_id', 'product_name', 'category', 
                          'total_quantity_sold', 'total_revenue']
        for col in required_columns:
            self.assertIn(col, product_metrics.columns)
    
    def test_monthly_summary_calculation(self):
        """Test monthly summary calculation"""
        enhanced_data = self.transformer.add_calculated_fields(self.sample_data)
        monthly_summary = self.transformer.calculate_monthly_summary(enhanced_data)
        
        # Should have 1 month (2023-01)
        self.assertEqual(len(monthly_summary), 1)
        self.assertEqual(monthly_summary.iloc[0]['year_month'], '2023-01')
        self.assertEqual(monthly_summary.iloc[0]['total_transactions'], 3)
    
    def test_data_transformation_pipeline(self):
        """Test complete transformation pipeline"""
        transformed_data = self.transformer.transform_data(self.sample_data)
        
        # Check if all expected keys exist
        expected_keys = ['transactions', 'customers', 'products', 
                        'monthly_summary', 'top_customers', 'top_products']
        for key in expected_keys:
            self.assertIn(key, transformed_data)
        
        # Check data integrity
        self.assertEqual(len(transformed_data['transactions']), 3)
        self.assertEqual(len(transformed_data['customers']), 2)
        self.assertEqual(len(transformed_data['products']), 3)

class TestDataQuality(unittest.TestCase):
    """Test data quality checks"""
    
    def test_revenue_consistency(self):
        """Test revenue calculation consistency"""
        data = pd.DataFrame({
            'quantity': [2, 3, 1],
            'unit_price': [10.0, 15.0, 100.0],
            'total_amount': [20.0, 45.0, 100.0]
        })
        
        # Check if total_amount equals quantity * unit_price
        calculated_total = data['quantity'] * data['unit_price']
        pd.testing.assert_series_equal(data['total_amount'], calculated_total)
    
    def test_date_validation(self):
        """Test date validation"""
        transformer = DataTransformer()
        
        # Create data with future dates
        future_data = pd.DataFrame({
            'transaction_id': ['T001'],
            'customer_id': ['C001'],
            'product_id': ['P001'],
            'product_name': ['Test'],
            'category': ['Electronics'],
            'quantity': [1],
            'unit_price': [100.0],
            'total_amount': [100.0],
            'transaction_date': ['2025-12-31'],  # Future date
            'transaction_time': ['10:00:00'],
            'store_id': ['ST001'],
            'store_location': ['Test Location'],
            'payment_method': ['Credit Card']
        })
        
        cleaned_data = transformer.clean_data(future_data)
        
        # Future dates should be removed
        self.assertEqual(len(cleaned_data), 0)

if __name__ == '__main__':
    # Create test data directory if it doesn't exist
    os.makedirs('./data/raw/', exist_ok=True)
    
    # Run tests
    unittest.main(verbosity=2)
