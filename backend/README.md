# Weather App Backend

This is the backend for the Weather App, built with Python, Flask, and Connexion (OpenAPI 3.0).

## Prerequisites

- Python 3.9+
- A compatible ODBC driver for MSSQL might be required for the `pyodbc` dependency (e.g., ODBC Driver 17 for SQL Server), though the current implementation contains stubs.

## Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Configuration settings are located in `app/core/config.py`.
Since this is a stubbed implementation, no database connection is actively established by default, but you can configure `SQLALCHEMY_DATABASE_URI` there.

## Running the Application

Start the Flask development server:
```bash
python run.py
```

The application will start on `http://localhost:8080`.

## API Documentation

Once the application is running, you can access the interactive Swagger UI documentation at:

[http://localhost:8080/api/v1/ui](http://localhost:8080/api/v1/ui)
