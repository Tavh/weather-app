import os

class Config:
    # Default to SQLite for local testing if no MSSQL URL provided
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///./weather.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'dev_salt_change_in_production')
    
    # JWT Settings
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
