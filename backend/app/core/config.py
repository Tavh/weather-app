import os

class Config:

    # DB
    
    # Default to SQLite for local testing if no MSSQL URL provided
    # Use absolute path for sqlite to avoid issues with relative paths
    basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "weather.db")}')
    
    # Auth & Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'dev_salt_change_in_production')
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # External Weather provider
    WEATHER_PROVIDER_BASE_URL = os.getenv(
        "WEATHER_PROVIDER_BASE_URL",
        "https://api.open-meteo.com/v1/forecast"
    )
    WEATHER_PROVIDER_TIMEOUT_SECONDS = int(
        os.getenv("WEATHER_PROVIDER_TIMEOUT_SECONDS", "5")
    )


