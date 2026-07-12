"""
Log Handlers

This module contains utility functions for setting up logging
consistently, tied to Gunicorn's logger when running under gunicorn.
"""
import logging


def init_logging(app, logger_name: str = "gunicorn.error"):
    """Set up logging for production"""
    logger = logging.getLogger(logger_name)
    if logger.handlers:
        app.logger.handlers = logger.handlers
        app.logger.setLevel(logger.level)
    app.logger.propagate = False
