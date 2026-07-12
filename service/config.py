"""
Global Configuration for Application
"""
import os

# Get configuration from environment
DATABASE_URI = os.getenv(
    "DATABASE_URI", "sqlite:///test.db"
)

# Enforce HTTPS redirects only when explicitly requested (e.g. behind a real
# TLS-terminating proxy). Keep disabled for local dev / CI / Kubernetes
# clusters that use plain HTTP internally.
FORCE_HTTPS = os.getenv("FORCE_HTTPS", "False").lower() in ("true", "1", "yes")

# Secret for session signing, CSRF, etc.
SECRET_KEY = os.getenv("SECRET_KEY", "s3cr3t-key-shhhh")

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
