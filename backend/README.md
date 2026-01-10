# Weather App Backend

A robust, layered REST API backend for managing weather zones and fetching real-time weather data. Built with Python, Flask, and Connexion, following an OpenAPI-first design approach.

## 1. Project Overview

*   **Authentication**: Secure JWT-based auth with Argon2 password hashing.
*   **Zone Management**: CRUD operations for weather zones with strict multi-tenancy (users manage only their own zones).
*   **Weather Integration**: Real-time weather fetching via Open-Meteo API.
*   **Observability**: Structured, production-ready logging.

**Tech Stack**:
*   Python 3.10+
*   Flask & Connexion (OpenAPI 3.0)
*   SQLAlchemy (ORM) ~ SQLite (Default)
*   Pydantic (Data Validation)
*   Pytest (Testing)

## 2. Architecture

The application follows a strict layered architecture to ensure separation of concerns:

1.  **API Layer (`app/api`)**: Handles HTTP requests, input validation (via OpenAPI), and session lifecycle.
2.  **Service Layer (`app/services`)**: Contains business logic (Auth, Zones, Weather). Services are stateless.
3.  **Repository Layer (`app/repo`)**: Abstraction for data access. **Multi-tenancy** is enforced here via a base `UserScopedRepository` that automatically filters data by the authenticated user.
4.  **Database**: SQLAlchemy models map to SQLite tables.

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

**Prerequisites**: Python 3.10+ installed.

1.  **Create Virtual Environment**:
    ```poweshell
    python -m venv .venv
    .venv\Scripts\Activate.ps1  # Windows
    # source .venv/bin/activate # Mac/Linux
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Application**:
    ```bash
    python run.py
    ```
    *   Server runs at: `http://127.0.0.1:8080/api/v1`
    *   **Swagger UI**: [http://127.0.0.1:8080/api/v1/ui/](http://127.0.0.1:8080/api/v1/ui/)

## 5. Configuration

Configuration is handled via `app/core/config.py` and Environment Variables.

| Variable | Default (Local) | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite:///.../weather.db` | Connection string for DB. |
| `SECRET_KEY` | `dev_secret_...` | Key for signing JWTs. **Change in Prod**. |
| `LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `ERROR`). |
| `WEATHER_PROVIDER_BASE_URL` | Open-Meteo URL | 3rd party Weather API endpoint. |

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

**3. Create a Zone**
```bash
# Replace <TOKEN> with your JWT
curl -X POST http://127.0.0.1:8080/api/v1/zones \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Vienna\", \"latitude\": 48.2082, \"longitude\": 16.3738}"
```

**4. List Zones**
```bash
curl -X GET http://127.0.0.1:8080/api/v1/zones \
  -H "Authorization: Bearer <TOKEN>"
```

**5. Refresh Weather Data**
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

**Scope**: Tests cover Authentication flows, Zone CRUD operations, Multi-tenant data isolation, and Weather Service integration (mocked).
