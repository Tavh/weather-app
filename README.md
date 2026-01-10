# Weather App

A full-stack Weather App built for Ikarus Security, allowing users to register, log in, and manage their own "weather zones" (saved cities or locations) through a CRUD API. For each zone, the app fetches current temperature data from a public weather API.

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
- **Status**: To be implemented
- **Planned**: React with Base Web components

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
- Docker Desktop (for running with MSSQL)
- Python 3.10+ (for local development)

### Running with Docker Compose (Recommended)

The easiest way to run the entire application stack:

```bash
docker-compose up --build
```

This will:
- Start Microsoft SQL Server
- Start the backend API server
- Make the API available at `http://127.0.0.1:8080/api/v1`
- Provide Swagger UI at `http://127.0.0.1:8080/api/v1/ui/`

### Running Backend Locally

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

## Development Status

### ✅ Completed
- Backend REST API with OpenAPI specification
- User authentication (JWT)
- City search functionality
- Weather zone CRUD operations
- Weather data fetching and caching
- Multi-tenant data isolation
- Comprehensive test suite

### 🚧 In Progress
- Frontend implementation (React with Base Web)

## License

This project is part of an assignment for Ikarus Security.
