# Weather App

A full-stack Weather App, allowing users to register, log in, and manage their own "weather zones" (saved cities or locations) through a CRUD API. For each zone, the app fetches current temperature data from a public weather API.

## Project Overview

This application provides a complete weather management system where authenticated users can:
- **Register and authenticate** with secure JWT-based authentication
- **Search for cities** by name using geocoding services
- **Manage weather zones** (create, read, update, delete) for their favorite locations
- **View weather data** for each zone with the ability to refresh current conditions

## Tech Stack

### Backend
- **Framework**: Flask with Connexion & OpenAPI
- **Database**: Microsoft SQL Server (Primary) with SQLite fallback
- **ORM**: SQLAlchemy
- **API Documentation**: OpenAPI 3.0 with Swagger UI
- **Authentication**: JWT with Argon2 password hashing
- **Testing**: Pytest

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: Base Web
- **Routing**: React Router
- **State Management**: React Context API

## Project Structure

```
weather-app/
├── backend/          # Flask REST API backend
│   ├── app/         # Application code
│   ├── tests/       # Test suite
│   ├── openapi/     # OpenAPI specification
│   └── README.md    # Backend-specific documentation
├── docker-compose.yml  # Docker Compose configuration
└── README.md        # This file
```

## Quick Start

### Prerequisites

**For Docker Compose:**
- Docker Desktop
- Docker Compose

**For Local Development:**
- Node.js 18+ and npm
- Python 3.10+
- Microsoft SQL Server (or use Docker for database only)

### Option 1: Running with Docker Compose (Recommended)

The easiest way to run the entire application stack:

1. **Create environment file** (first time only):
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to customize values if needed (passwords, ports, etc.)

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

This will:
- Start Microsoft SQL Server
- Start the backend API server on port 8080 (configurable via `BACKEND_PORT` in `.env`)
- Start the frontend application on port 3000 (configurable via `FRONTEND_PORT` in `.env`)
- Make the API available at `http://localhost:8080/api/v1`
- Make the frontend available at `http://localhost:3000`
- Provide Swagger UI at `http://localhost:8080/api/v1/ui/`

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080/api/v1
- API Docs: http://localhost:8080/api/v1/ui/

**Note:** The `.env` file is gitignored. Copy `.env.example` to `.env` and customize values for your environment.

### Inspecting the Database (Docker)

To inspect the Microsoft SQL Server database while it's running in Docker:

1.  **Connect to the database container:**
    ```bash
    docker-compose exec db /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P StrongPass123! -C
    ```

    *Note: This opens a SQL shell (`1>`). It is not a bash shellwill not work.*

2.  **Run SQL queries:**

    To execute a query, type the SQL statement, press Enter, then type `GO` and press Enter again.
    
    Check for existing data:
    ```sql
    SELECT * FROM users;
    GO
    ```

    List user tables:
    ```sql
    SELECT name FROM sys.tables WHERE name NOT LIKE 'spt_%' AND name NOT LIKE 'MS%';
    GO
    ```

    Type `QUIT` to exit the SQL prompt.

### Viewing Logs (Docker)

To view the logs for the running services:

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Option 2: Running Locally

#### Backend Setup

1. **Start the database** (using Docker):
   ```bash
   docker-compose up db -d
   ```

2. **Install ODBC Driver 18 for SQL Server** (Windows only):
   
   **Option A: Download and Install**
   - Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   - Install "ODBC Driver 18 for SQL Server"
   - Restart your terminal after installation
   
   **Option B: Use SQLite instead** (No driver needed):
   - Skip ODBC installation
   - Don't set `DATABASE_URL` - it will use SQLite automatically
   - Note: SQLite is a fallback for development only

3. **Set up Python environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   
   **For MSSQL (with Docker database):**
   ```powershell
   # Windows PowerShell
   $env:DATABASE_URL="mssql+pyodbc://sa:StrongPass123!@localhost:1433/weather_app?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
   $env:SECRET_KEY="your-secret-key-here"
   ```
   
   ```bash
   # Linux/Mac
   export DATABASE_URL="mssql+pyodbc://sa:StrongPass123!@localhost:1433/weather_app?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
   export SECRET_KEY="your-secret-key-here"
   ```
   
   **For SQLite (no driver needed):**
   ```powershell
   # Windows PowerShell - Just set SECRET_KEY, DATABASE_URL will default to SQLite
   $env:SECRET_KEY="your-secret-key-here"
   ```
   
   Or simply don't set `DATABASE_URL` - it will use SQLite automatically.

5. **Run the backend**:
   ```bash
   python run.py
   ```

   Backend will be available at `http://localhost:8080`

#### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run the development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`
   
   The Vite dev server is configured to proxy API requests to `http://localhost:8080`

**Note:** When running locally, the frontend uses Vite's proxy to forward `/api` requests to the backend on port 8080. No additional configuration needed.

### Running Backend Locally (Detailed)

For detailed backend setup instructions, see [backend/README.md](backend/README.md).

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token

### City Search
- `GET /api/v1/cities/search?q={city_name}` - Search for cities by name

### Weather Zones
- `GET /api/v1/zones` - List all zones for authenticated user
- `POST /api/v1/zones` - Create a new zone
- `GET /api/v1/zones/{id}` - Get zone details
- `PUT /api/v1/zones/{id}` - Update a zone
- `DELETE /api/v1/zones/{id}` - Delete a zone
- `POST /api/v1/zones/{id}/refresh` - Refresh weather data for a zone

## Example Usage

### 1. Register and Login
```bash
# Register
curl -X POST http://127.0.0.1:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "demo_user", "password": "StrongPass123!"}'

# Login
curl -X POST http://127.0.0.1:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo_user", "password": "StrongPass123!"}'
```

### 2. Search for Cities
```bash
curl -X GET "http://127.0.0.1:8080/api/v1/cities/search?q=Paris" \
  -H "Authorization: Bearer <TOKEN>"
```

### 3. Create a Zone from Search Result
```bash
curl -X POST http://127.0.0.1:8080/api/v1/zones \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Paris", "latitude": 48.8566, "longitude": 2.3522}'
```

### 4. Refresh Weather
```bash
curl -X POST http://127.0.0.1:8080/api/v1/zones/1/refresh \
  -H "Authorization: Bearer <TOKEN>"
```

## Testing

Run the backend test suite:

```bash
cd backend
python -m pytest tests
```

For manual integration testing:

```bash
cd backend
python temp_debug/manual_test.py
```

## Documentation

- **Backend Documentation**: See [backend/README.md](backend/README.md) for detailed backend setup, architecture, and configuration
- **API Documentation**: Available at `http://127.0.0.1:8080/api/v1/ui/` when the server is running

