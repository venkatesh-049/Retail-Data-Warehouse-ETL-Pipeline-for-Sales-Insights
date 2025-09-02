# Retail Data Warehouse ETL Pipeline for Sales Insights

A complete data engineering project that builds an ETL pipeline for retail sales data analysis with automated scheduling and business intelligence dashboards.

## Architecture Overview

```
CSV Data → Extract → Transform → PostgreSQL → Metabase Dashboard
                ↑
            Apache Airflow (Scheduling)
```

## Features

- **Data Extraction**: Automated CSV data ingestion
- **Data Transformation**: Clean data and calculate KPIs
- **Data Warehouse**: PostgreSQL storage with optimized schema
- **Scheduling**: Apache Airflow for daily ETL runs
- **Visualization**: Metabase dashboards for business insights

## Key Metrics Tracked

- Monthly sales trends
- Top 10 customers by revenue
- High revenue products analysis
- Sales performance indicators

## Installation & Setup

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Apache Airflow 2.7+
- Metabase (free version)

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**
   ```bash
   python setup_database.py
   ```

3. **Run ETL Pipeline**
   ```bash
   python etl_pipeline.py
   ```

4. **Start Airflow**
   ```bash
   airflow standalone
   ```

5. **Launch Metabase**
   - Download and run Metabase JAR file
   - Connect to PostgreSQL database
   - Import dashboard templates

## Project Structure

```
├── data/                   # Raw and processed data files
├── etl/                   # ETL pipeline modules
├── airflow/               # Airflow DAGs and configuration
├── sql/                   # Database schemas and queries
├── dashboards/            # Metabase dashboard exports
├── config/                # Configuration files
└── tests/                 # Unit tests
```

## Configuration

Create a `.env` file with your database credentials:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_warehouse
DB_USER=your_username
DB_PASSWORD=your_password
```

## Usage

The pipeline automatically processes retail sales data and generates insights including:

- Revenue trends over time
- Customer segmentation analysis
- Product performance metrics
- Sales forecasting data

## Contributing

This is a learning project demonstrating modern data engineering practices with open-source tools.
