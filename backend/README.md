# Weather App Backend

This is the Python/Flask/Connexion backend for the Weather App. It uses OpenAPI 3.0 for API definition and validation.

## Project Structure

```text
backend/
├── app/
│   ├── api/            # Route handlers (controllers)
│   │   ├── auth.py     # Auth endpoints (Register, Login)
│   │   └── zones.py    # Zone management endpoints
│   ├── core/
│   │   ├── config.py   # Configuration (SQLAlchemy, JWT settings)
│   │   ├── security.py # JWT and Password utilities
│   │   └── database.py # DB init (SQLAlchemy)
│   └── __init__.py     # App factory (create_app)
├── openapi/
│   └── openapi.yaml    # OpenAPI 3.0 Specification
├── run.py              # Application entry point
├── requirements.txt    # dependencies
└── README.md
```

## Setup & Running

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server**
   ```bash
   python run.py
   ```
   The server runs at `http://127.0.0.1:8080`.
   
   - **Swagger UI**: [http://127.0.0.1:8080/api/v1/ui/](http://127.0.0.1:8080/api/v1/ui/)
   - **API Prefix**: `/api/v1`

## Testing with Curl

### 1. Register (Stub)
```bash
curl -X POST http://127.0.0.1:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"testuser\", \"password\": \"securePass123\"}"
```

### 2. Login (Get Token)
```bash
curl -X POST http://127.0.0.1:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"testuser\", \"password\": \"securePass123\"}"
```
*Returns a stub token: `{"access_token": "stub_token", ...}`*

### 3. Create Zone
```bash
curl -X POST http://127.0.0.1:8080/api/v1/zones \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer stub_token" \
  -d "{\"name\": \"My Home\", \"latitude\": 48.85, \"longitude\": 2.35}"
```

### 4. Get Zone
```bash
curl -X GET http://127.0.0.1:8080/api/v1/zones/1 \
  -H "Authorization: Bearer stub_token"
```

### 5. Refresh Zone Weather
```bash
curl -X POST http://127.0.0.1:8080/api/v1/zones/1/refresh \
  -H "Authorization: Bearer stub_token"
```
