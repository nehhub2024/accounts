"""WSGI entry point for production servers (gunicorn, uWSGI, etc.)"""
from service import app

if __name__ == "__main__":
    app.run()
