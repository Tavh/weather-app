#!/bin/bash
# Wait for SQL Server to be ready and accepting connections, this is for the docker-compose deployment
# Reads connection details from environment variables

set -e

host="${DB_HOST:-db}"
port="${DB_PORT:-1433}"
user="${DB_USER:-sa}"
password="${DB_SA_PASSWORD}"
max_attempts="${DB_WAIT_MAX_ATTEMPTS:-30}"
attempt=0

if [ -z "$password" ]; then
    echo "[WAIT] ERROR: DB_SA_PASSWORD environment variable is not set"
    exit 1
fi

echo "[WAIT] Waiting for SQL Server at $host:$port to be ready..."

while [ $attempt -lt $max_attempts ]; do
    attempt=$((attempt + 1))
    echo "[WAIT] Attempt $attempt/$max_attempts..."
    
    # Try to connect using sqlcmd
    if /opt/mssql-tools18/bin/sqlcmd -S "$host" -U "$user" -P "$password" -C -Q "SELECT 1" > /dev/null 2>&1; then
        echo "[WAIT] SQL Server is ready!"
        exec "$@"
    fi
    
    if [ $attempt -lt $max_attempts ]; then
        echo "[WAIT] SQL Server not ready yet, waiting 2 seconds..."
        sleep 2
    fi
done

echo "[WAIT] ERROR: SQL Server did not become ready after $max_attempts attempts"
exit 1
