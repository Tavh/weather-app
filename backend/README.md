# Weather App Backend

A robust, layered REST API backend for managing weather zones and fetching real-time weather data. Built with Python, Flask, and Connexion, following an OpenAPI-first design approach.

## 1. Project Overview

*   **Authentication**: Secure JWT-based auth with Argon2 password hashing.
*   **City Search**: Search for cities by name using Open-Meteo Geocoding API.
*   **Zone Management**: CRUD operations for weather zones with strict multi-tenancy (users manage only their own zones).
*   **Weather Integration**: Real-time weather fetching via Open-Meteo API.
*   **Observability**: Structured, production-ready logging.

**Tech Stack**:
*   Python 3.10+
*   Flask & Connexion (OpenAPI 3.0)
*   SQLAlchemy (ORM) with **Microsoft SQL Server** (Primary) or SQLite (Fallback)
*   Pydantic (Data Validation)
*   Pytest (Testing)

## 2. Architecture

The application follows a strict layered architecture to ensure separation of concerns:

1.  **API Layer (`app/api`)**: Handles HTTP requests, input validation (via OpenAPI), and session lifecycle.
2.  **Service Layer (`app/services`)**: Contains business logic (Auth, Zones, Weather). Services are stateless.
3.  **Repository Layer (`app/repo`)**: Abstraction for data access. **Multi-tenancy** is enforced here via a base `UserScopedRepository` that automatically filters data by the authenticated user.
4.  **Database**: SQLAlchemy models map to Microsoft SQL Server tables (or SQLite for local development).

**Key Design Decisions**:
*   **Request-Scoped Sessions**: Database sessions are managed via a context manager in the API layer, ensuring auto-commit/rollback per request.
*   **Provider Isolated**: The `WeatherService` encapsulates the 3rd-party provider (Open-Meteo), allowing it to be swapped with minimal changes.

## 3. Project Structure

```text
backend/
├── app/
│   ├── api/            # Controllers / Route Handlers
│   ├── core/           # Config, Database, Logging, Security, Exceptions
│   ├── dtos/           # Pydantic Data Transfer Objects
│   ├── models/         # SQLAlchemy Database Models
│   ├── repo/           # Data Access Layer (Repositories)
│   └── services/       # Business Logic Layer
├── openapi/
│   └── openapi.yaml    # OpenAPI 3.0 Specification
├── tests/              # Pytest Suite (Integration Tests)
├── requirements.txt    # Project Dependencies
└── run.py              # Application Entry Point
```

## 4. Setup & Running

The application supports **Microsoft SQL Server** as the primary database, with three deployment modes:

### A. MSSQL via Docker Compose (Recommended)

**This is the primary and recommended way to run the backend.** Docker Compose provisions both Microsoft SQL Server and the backend API with a single command, mirroring the intended production infrastructure.

**Prerequisites**: Docker Desktop installed.

**Steps**:
1.  **Start everything**:
    ```bash
    docker-compose up --build
    ```
    *   Starts MSSQL (`db`) and the backend (`backend`) services.
    *   The backend automatically waits for the database to be healthy before starting.
    *   No manual configuration needed.

2.  **Access the application**:
    *   **Swagger UI**: [http://127.0.0.1:8080/api/v1/ui/](http://127.0.0.1:8080/api/v1/ui/)
    *   **API Root**: `http://127.0.0.1:8080/api/v1`

**Environment Variables** (automatically set by docker-compose):
```bash
DATABASE_URL=mssql+pyodbc://sa:YOUR_PASSWORD@db:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
SECRET_KEY=your_secret_key_here
LOG_LEVEL=INFO
```

### B. MSSQL Running Locally (Advanced / Optional)

If you prefer to run Microsoft SQL Server locally (outside Docker), you can connect the backend to your local instance.

**Prerequisites**: 
*   Microsoft SQL Server installed and running locally (or use Docker for database only: `docker-compose up db -d`)
*   **ODBC Driver 18 for SQL Server installed** (Required on Windows)

**Installing ODBC Driver 18 for SQL Server (Windows)**:
1. Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
2. Install "ODBC Driver 18 for SQL Server"
3. Restart your terminal/PowerShell after installation
4. Verify installation:
   ```powershell
   Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}
   ```

**Steps**:
1.  **Setup Python environment**:
    ```bash
    python -m venv .venv
    .venv\Scripts\Activate.ps1  # Windows
    # source .venv/bin/activate  # Linux/Mac
    pip install -r requirements.txt
    ```

2.  **Configure connection**:
    Set the `DATABASE_URL` environment variable to point to your MSSQL instance:
    ```powershell
    # Windows PowerShell - Connect to Docker database
    $env:DATABASE_URL="mssql+pyodbc://sa:StrongPass123!@localhost:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    
    # Windows PowerShell - Connect to local SQL Server
    $env:DATABASE_URL="mssql+pyodbc://sa:YOUR_PASSWORD@localhost:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    ```
    
    ```bash
    # Linux/Mac
    export DATABASE_URL="mssql+pyodbc://sa:YOUR_PASSWORD@localhost:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    ```

3.  **Run the application**:
    ```bash
    python run.py
    ```

**Note**: The application code does not change. Only the connection string differs.

**Troubleshooting ODBC Driver Issues**:
- **Error: "Data source name not found"**: ODBC Driver 18 is not installed. Install it from the link above.
- **Error: "Driver not found"**: Check the driver name matches exactly: `ODBC+Driver+18+for+SQL+Server` (with spaces encoded as `+`)
- **Alternative**: Use SQLite fallback (see section C) - no driver installation needed

### C. SQLite (Development Fallback)

SQLite is available as a lightweight fallback for quick local iteration without database setup. **This is not the primary database** and should not be used in production.

**When to use**: Fast prototyping, quick tests, or when MSSQL is unavailable.

**Steps**:
1.  **Setup Python environment**:
    ```bash
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2.  **Run the application**:
    ```bash
    python run.py
    ```
    *   Uses `weather.db` (SQLite) by default when `DATABASE_URL` is not set.
    *   No additional configuration needed.

**Environment Variable** (optional, for explicit control):
```bash
DATABASE_URL=sqlite:///weather.db
```

## 5. Configuration

| Variable | Description | Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | Database connection string | See examples below |
| `SECRET_KEY` | JWT signing key (change in production) | `your_secret_key_here` |
| `LOG_LEVEL` | Logging level | `DEBUG`, `INFO`, `ERROR` |
| `WEATHER_PROVIDER_BASE_URL` | Weather API endpoint | `https://api.open-meteo.com/v1/forecast` |
| `CITY_GEOCODING_BASE_URL` | City geocoding API endpoint | `https://geocoding-api.open-meteo.com/v1/search` |

**Connection String Examples**:

*   **Docker Compose MSSQL**:
    ```
    mssql+pyodbc://sa:YOUR_PASSWORD@db:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
    ```

*   **Local MSSQL**:
    ```
    mssql+pyodbc://sa:YOUR_PASSWORD@localhost:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
    ```

*   **SQLite** (fallback):
    ```
    sqlite:///weather.db
    ```

## 6. Example API Usage (Curl)

**1. Register a User**
```bash
curl -X POST http://127.0.0.1:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"demo_user\", \"password\": \"StrongPass123!\"}"
```

**2. Login (Get JWT)**
```bash
curl -X POST http://127.0.0.1:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"demo_user\", \"password\": \"StrongPass123!\"}"
```
*Copy the `access_token` from the response for the following steps.*

**3. Search for Cities**
```bash
# Replace <TOKEN> with your JWT
curl -X GET "http://127.0.0.1:8080/api/v1/cities/search?q=Paris" \
  -H "Authorization: Bearer <TOKEN>"
```

**4. Create a Zone**
```bash
# Replace <TOKEN> with your JWT
curl -X POST http://127.0.0.1:8080/api/v1/zones \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Vienna\", \"latitude\": 48.2082, \"longitude\": 16.3738}"
```

**5. List Zones**
```bash
curl -X GET http://127.0.0.1:8080/api/v1/zones \
  -H "Authorization: Bearer <TOKEN>"
```

**6. Refresh Weather Data**
```bash
# Replace <ZONE_ID> with an ID from the list command
curl -X POST http://127.0.0.1:8080/api/v1/zones/<ZONE_ID>/refresh \
  -H "Authorization: Bearer <TOKEN>"
```

## 7. Testing

The project includes an integration test suite using `pytest` and an in-memory SQLite database.

```bash
# Run all tests
python -m pytest tests

# Run specific file
python -m pytest tests/test_zones.py
```

**Scope**: Tests cover Authentication flows, City Search functionality, Zone CRUD operations, Multi-tenant data isolation, and Weather Service integration (mocked).
