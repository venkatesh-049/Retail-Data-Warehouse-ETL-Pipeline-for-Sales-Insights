import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

def get_database_engine():
    """Create and return database engine"""
    
    # Database connection parameters
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '3306'),
        'database': os.getenv('DB_NAME', 'retail_warehouse'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password')
    }
    
    # Create connection string for MySQL
    connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    
    # Create engine
    engine = create_engine(
        connection_string,
        echo=False,  # Set to True for SQL debugging
        pool_pre_ping=True,
        pool_recycle=300
    )
    
    return engine

def get_connection_string():
    """Get connection string for pandas operations"""
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '3306'),
        'database': os.getenv('DB_NAME', 'retail_warehouse'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password')
    }
    
    return f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

def get_connection_params():
    """Get connection parameters for direct database connections"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'database': os.getenv('DB_NAME', 'retail_warehouse'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password')
    }

def get_db_connection():
    """Get database connection"""
    engine = get_database_engine()
    return engine.connect()

def get_db_session():
    """Get database session"""
    engine = get_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

Base = declarative_base()
