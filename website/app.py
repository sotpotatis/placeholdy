"""app.py
Running this script creates a function with the app that serves the website."""
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

LOGGING_LEVELS = {  # Mappings: string -> logging level constant
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def create_app() -> Flask:
    """Creates the app for the website."""
    from libraries.configuration_file import get_configuration_file

    # Load config and some parameters
    config = get_configuration_file()
    CORS_SETTINGS = config.get("cors", {"enabled": True, "allowed_origins": "*"})
    REQUEST_LIMIT_SETTINGS = config.get(
        "request_limit", {"enabled": False, "limits": None}
    )
    # Set up logging
    LOGGING_LEVEL_NAME = config.get("logging_level", "info").lower()
    LOGGING_LEVEL = LOGGING_LEVELS[LOGGING_LEVEL_NAME]
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=LOGGING_LEVEL)
    # Print some information
    logger.info("~Placeholdy!~")
    logger.info("Created with <3 by Albin")
    # Create a Flask app
    app = Flask(__name__, static_url_path="")
    # Set up CORS if configured
    if CORS_SETTINGS["enabled"]:
        logger.info("Applying CORS configuration...")
        cors = CORS(
            app,
            resources={
                r"/placeholder/*": {"origins": CORS_SETTINGS["allowed_origins"]}
            },
        )
        logger.info("CORS configuration applied.")
    else:
        logger.warning(
            "CORS has been disabled. People may not be able to use your service to the fullest!"
        )
    # Set up request limit
    if REQUEST_LIMIT_SETTINGS["enabled"]:
        logger.info("Enabling request limit...")
        # Ensure type
        if isinstance(REQUEST_LIMIT_SETTINGS["limits"], list):
            request_limits = REQUEST_LIMIT_SETTINGS["limits"]
        else:
            request_limits = [REQUEST_LIMIT_SETTINGS["limits"]]
        limiter = Limiter(
            key_func=get_remote_address,
            app=app,
            default_limits=request_limits,
            storage_uri="memory://",
        )
        logger.info("Request limiter enabled.")
    else:
        logger.warning(
            "You have not set up a request limit. This is highly recommended for a production application!"
        )
    # Import blueprints
    from api_routes import api
    from documentation import docs

    # ... and register them
    logger.info("Registering blueprints...")
    for blueprint in [api, docs]:
        app.register_blueprint(blueprint)
    logger.info("Blueprints registered.")
    # Load other functions, such as CORS etc.
    return app
