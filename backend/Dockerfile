FROM python:3.10-slim

# Install system dependencies for MSSQL ODBC Driver
# Using Debian 12 repository (works with python:3.10-slim which is based on Debian 13)
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev \
    ca-certificates \
    && mkdir -p /usr/share/keyrings \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list -o /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait script and make it executable
COPY wait-for-db.sh /usr/local/bin/wait-for-db.sh
RUN chmod +x /usr/local/bin/wait-for-db.sh

COPY . .

# Expose port (default Flask)
EXPOSE 8080

# Use entrypoint script to wait for database, then run the app
# The script reads DB_SA_PASSWORD from environment and executes CMD after database is ready
ENTRYPOINT ["/usr/local/bin/wait-for-db.sh"]
CMD ["python", "run.py"]
