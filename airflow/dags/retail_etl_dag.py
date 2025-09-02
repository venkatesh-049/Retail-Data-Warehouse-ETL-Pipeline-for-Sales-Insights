#!/usr/bin/env python3
"""
Apache Airflow DAG for Retail Data Warehouse ETL Pipeline
Schedules daily execution of the ETL process
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import sys
import os

# Add project root to Python path
sys.path.append('/path/to/your/project')  # Update this path

# Default arguments for the DAG
default_args = {
    'owner': 'data-engineering-team',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'retail_etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline for retail sales data warehouse',
    schedule_interval='0 2 * * *',  # Run daily at 2 AM
    catchup=False,
    tags=['retail', 'etl', 'data-warehouse'],
)

def extract_data(**context):
    """Extract data from source"""
    from etl.extract import DataExtractor
    
    extractor = DataExtractor()
    df, validation_results = extractor.extract_and_validate()
    
    # Store results in XCom for next task
    context['task_instance'].xcom_push(key='raw_data_count', value=len(df))
    context['task_instance'].xcom_push(key='validation_results', value=validation_results)
    
    return f"Extracted {len(df):,} records"

def transform_data(**context):
    """Transform the extracted data"""
    from etl.extract import DataExtractor
    from etl.transform import DataTransformer
    
    # Extract data
    extractor = DataExtractor()
    df, _ = extractor.extract_and_validate()
    
    # Transform data
    transformer = DataTransformer()
    transformed_data = transformer.transform_data(df)
    
    # Store results in XCom
    context['task_instance'].xcom_push(key='transactions_count', value=len(transformed_data['transactions']))
    context['task_instance'].xcom_push(key='customers_count', value=len(transformed_data['customers']))
    context['task_instance'].xcom_push(key='products_count', value=len(transformed_data['products']))
    
    return f"Transformed {len(transformed_data['transactions']):,} transactions"

def load_data(**context):
    """Load transformed data into the data warehouse"""
    from etl.extract import DataExtractor
    from etl.transform import DataTransformer
    from etl.load import DataLoader
    
    # Extract and transform data
    extractor = DataExtractor()
    df, _ = extractor.extract_and_validate()
    
    transformer = DataTransformer()
    transformed_data = transformer.transform_data(df)
    transformed_data['raw_data'] = df
    
    # Load data
    loader = DataLoader()
    loader.load_all_data(transformed_data)
    
    return f"Loaded data successfully to warehouse"

def send_success_notification(**context):
    """Send success notification"""
    raw_count = context['task_instance'].xcom_pull(key='raw_data_count', task_ids='extract_task')
    transactions_count = context['task_instance'].xcom_pull(key='transactions_count', task_ids='transform_task')
    
    print(f"✅ ETL Pipeline completed successfully!")
    print(f"📊 Processed {raw_count:,} raw records")
    print(f"🔄 Generated {transactions_count:,} clean transactions")
    print(f"⏰ Completed at: {datetime.now()}")
    
    return "Success notification sent"

# Define tasks
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data,
    dag=dag,
)

# Data quality check task
quality_check_task = BashOperator(
    task_id='data_quality_check',
    bash_command="""
    python -c "
from config.database_config import get_db_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    conn = get_db_connection()
    
    # Check record counts
    result = conn.execute('SELECT COUNT(*) FROM sales.transactions')
    transaction_count = result.fetchone()[0]
    
    result = conn.execute('SELECT COUNT(*) FROM sales.customers')
    customer_count = result.fetchone()[0]
    
    result = conn.execute('SELECT SUM(total_revenue) FROM sales.monthly_summary')
    total_revenue = result.fetchone()[0]
    
    logger.info(f'Quality Check Results:')
    logger.info(f'  Transactions: {transaction_count:,}')
    logger.info(f'  Customers: {customer_count:,}')
    logger.info(f'  Total Revenue: ${total_revenue:,.2f}')
    
    # Basic quality checks
    if transaction_count == 0:
        raise ValueError('No transactions found in database')
    if customer_count == 0:
        raise ValueError('No customers found in database')
    if total_revenue <= 0:
        raise ValueError('Invalid total revenue')
    
    logger.info('✅ All quality checks passed')
    conn.close()
    
except Exception as e:
    logger.error(f'❌ Quality check failed: {e}')
    raise
"
    """,
    dag=dag,
)

notification_task = PythonOperator(
    task_id='send_notification',
    python_callable=send_success_notification,
    dag=dag,
)

# Define task dependencies
extract_task >> transform_task >> load_task >> quality_check_task >> notification_task
