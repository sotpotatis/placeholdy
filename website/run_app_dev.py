"""run_app_dev.py
Useful for running a development server.
NOTE: This should only be used in development."""
from app import create_app
from warnings import warn

warn(
    "You're running a development server. In production, use a production server like Gunicorn!"
)
create_app().run(debug=True)
