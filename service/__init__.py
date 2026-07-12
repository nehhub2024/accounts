"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up logging
and the SQLAlchemy database connection. It also applies Talisman
security headers and Flask-CORS to the application.
"""
import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service import config
from service.common import log_handlers

# NOTE: Do not change the order of this code
# The Flask app must be created
# BEFORE you import modules that depend on it !!!

# Create the Flask app
app = Flask(__name__)
app.config.from_object(config)

# Import the routes After the Flask app is created
from service import routes, models  # noqa: F401, E402
from service.common import error_handlers  # noqa: F401, E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

# Apply CORS to this app
CORS(app)

# Apply Talisman security headers.
# force_https is disabled by default so the service can run locally / in
# Kubernetes behind a load balancer that terminates TLS. Set FORCE_HTTPS=1
# in the environment to enforce HTTPS redirects.
talisman = Talisman(app, force_https=config.FORCE_HTTPS)

try:
    models.init_db(app)  # make our sqlalchemy tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
