@echo off
echo ========================================
echo Retail Data Warehouse ETL Pipeline
echo ========================================

echo.
echo Step 1: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Setting up database...
python setup_database.py

echo.
echo Step 3: Generating sample data...
cd data
python generate_sample_data.py
cd ..

echo.
echo Step 4: Running ETL pipeline...
python etl_pipeline.py

echo.
echo ========================================
echo Pipeline execution completed!
echo ========================================
echo.
echo Next steps:
echo 1. Start Airflow: airflow standalone
echo 2. Setup Metabase for visualization
echo 3. Explore your data warehouse!
echo.
pause
