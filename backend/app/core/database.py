import logging
import re
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import Config

logger = logging.getLogger(__name__)

def ensure_database_exists():
    """Create the database if it doesn't exist (MSSQL only)."""
    if "sqlite" in Config.DATABASE_URL:
        return  # SQLite doesn't need database creation
    
    # Use print for visibility even before logging is set up
    print("[DATABASE] Ensuring database exists...")
    
    # Extract database name and connection details from connection string
    # Format: mssql+pyodbc://user:pass@host:port/dbname?params
    match = re.search(r'@([^/]+)/([^?]+)', Config.DATABASE_URL)
    if not match:
        error_msg = "Could not extract database name from DATABASE_URL"
        print(f"[DATABASE] ERROR: {error_msg}")
        logger.warning(error_msg)
        raise ValueError(error_msg)
    
    host_port = match.group(1)  # e.g., "db:1433" or "localhost:1433"
    db_name = match.group(2)  # e.g., "weather_app"
    
    # Extract user:pass from URL
    user_pass_match = re.search(r'://([^@]+)@', Config.DATABASE_URL)
    if not user_pass_match:
        error_msg = "Could not extract credentials from DATABASE_URL"
        print(f"[DATABASE] ERROR: {error_msg}")
        logger.warning(error_msg)
        raise ValueError(error_msg)
    
    user_pass = user_pass_match.group(1)  # e.g., "sa:password"
    
    # Construct master database URL
    master_url = f"mssql+pyodbc://{user_pass}@{host_port}/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    
    try:
        print(f"[DATABASE] Checking if database '{db_name}' exists...")
        logger.info(f"Checking if database '{db_name}' exists...")
        master_engine = create_engine(master_url, pool_pre_ping=True)
        
        # Check if database exists (in transaction)
        with master_engine.connect() as conn:
            result = conn.execute(text(f"SELECT name FROM sys.databases WHERE name = '{db_name}'"))
            db_exists = result.fetchone() is not None
        
        # Create database if needed (must be in autocommit mode)
        if not db_exists:
            print(f"[DATABASE] Creating database '{db_name}'...")
            logger.info(f"Creating database '{db_name}'...")
            # CREATE DATABASE must be executed in autocommit mode (outside transaction)
            with master_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                conn.execute(text(f"CREATE DATABASE [{db_name}]"))
            print(f"[DATABASE] Database '{db_name}' created successfully")
            logger.info(f"Database '{db_name}' created successfully")
        else:
            print(f"[DATABASE] Database '{db_name}' already exists")
            logger.info(f"Database '{db_name}' already exists")
        
        master_engine.dispose()
    except Exception as e:
        error_msg = f"Failed to ensure database exists: {str(e)}"
        print(f"[DATABASE] ERROR: {error_msg}")
        logger.error(error_msg)
        logger.error(f"Master URL: {master_url.replace(user_pass, '***')}")  # Log without password
        raise  # Fail fast - no retries


# Ensure database exists before creating engine (for MSSQL)
if "sqlite" not in Config.DATABASE_URL:
    ensure_database_exists()

# Create engine - database should exist now
engine = create_engine(
    Config.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in Config.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def get_session():
    """
    Request-scoped session context manager.
    Handles commit on success, rollback on error, and guaranteed closing.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(f"Database session error, rolling back: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

def init_db():
    """Explicitly create tables."""
    import app.models.user
    import app.models.zone
    print(f"Creating tables in: {Config.DATABASE_URL}")
    Base.metadata.create_all(bind=engine)
