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
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port (default Flask)
EXPOSE 8080

CMD ["python", "run.py"]
