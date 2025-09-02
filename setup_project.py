#!/usr/bin/env python3
"""
Complete project setup script for Retail Data Warehouse ETL Pipeline
Sets up environment, generates data, and runs initial pipeline
"""

import os
import sys
import subprocess
from datetime import datetime

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def print_step(step_num, description):
    """Print formatted step"""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 40)

def run_command(command, description):
    """Run a command and handle errors"""
    try:
        print(f"▶️  {description}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def create_env_file():
    """Create .env file from example"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        
        env_content = """# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_warehouse
DB_USER=postgres
DB_PASSWORD=password

# Airflow Configuration
AIRFLOW_HOME=./airflow
AIRFLOW__CORE__DAGS_FOLDER=./airflow/dags
AIRFLOW__CORE__LOAD_EXAMPLES=False

# Data Configuration
DATA_SOURCE_PATH=./data/raw/
PROCESSED_DATA_PATH=./data/processed/
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created")
        print("⚠️  Please update database credentials in .env file before proceeding")
        return True
    else:
        print("ℹ️  .env file already exists")
        return True

def setup_directories():
    """Create necessary directories"""
    directories = [
        'data/raw',
        'data/processed',
        'airflow/logs',
        'airflow/dags',
        'logs',
        'tests'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def main():
    """Main setup function"""
    print_header("Retail Data Warehouse ETL Pipeline Setup")
    
    # Step 1: Create directories
    print_step(1, "Setting up project directories")
    setup_directories()
    
    # Step 2: Create environment file
    print_step(2, "Setting up environment configuration")
    create_env_file()
    
    # Step 3: Install dependencies
    print_step(3, "Installing Python dependencies")
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("⚠️  Some dependencies may have failed to install. Please check manually.")
    
    # Step 4: Generate sample data
    print_step(4, "Generating sample retail sales data")
    if run_command("python data/generate_sample_data.py", "Generating sample data"):
        print("✅ Sample data generated successfully")
    else:
        print("❌ Failed to generate sample data")
        return False
    
    # Step 5: Setup database (optional - requires PostgreSQL)
    print_step(5, "Database setup (optional)")
    print("⚠️  Database setup requires PostgreSQL to be installed and running")
    print("   To setup database manually, run: python setup_database.py")
    
    # Step 6: Run tests
    print_step(6, "Running unit tests")
    if run_command("python -m pytest tests/ -v", "Running tests"):
        print("✅ All tests passed")
    else:
        print("⚠️  Some tests may have failed. Check test output above.")
    
    # Step 7: Run ETL pipeline (if database is available)
    print_step(7, "ETL Pipeline execution")
    print("⚠️  ETL pipeline requires database to be set up")
    print("   To run ETL pipeline manually, run: python etl_pipeline.py")
    
    # Final summary
    print_header("Setup Complete!")
    print("🎉 Your Retail Data Warehouse ETL Pipeline is ready!")
    print("\n📋 Next Steps:")
    print("1. 🗄️  Install and configure PostgreSQL")
    print("2. 📝 Update database credentials in .env file")
    print("3. 🔧 Run: python setup_database.py")
    print("4. 🚀 Run: python etl_pipeline.py")
    print("5. ⏰ Setup Airflow: airflow standalone")
    print("6. 📊 Configure Metabase for visualization")
    
    print("\n📁 Project Structure:")
    print("├── data/                   # Sample data generated")
    print("├── etl/                   # ETL pipeline modules")
    print("├── sql/                   # Database schemas and queries")
    print("├── airflow/               # Airflow configuration")
    print("├── metabase/              # Dashboard setup guide")
    print("├── tests/                 # Unit tests")
    print("└── logs/                  # Pipeline logs")
    
    print(f"\n⏰ Setup completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
