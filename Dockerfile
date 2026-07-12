FROM python:3.9-slim

# Set up a working folder
WORKDIR /app

# Install system dependencies needed for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application contents
COPY service/ ./service/

# Create a non-root user and switch to it for security
RUN useradd --uid 1000 flask && chown -R flask /app
USER flask

# Expose the service port
EXPOSE 8080

# Run the service using gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]
