"""api_routes.py
This file defines the API routes of the page."""
from flask import Blueprint, request, send_from_directory
from pydantic import ValidationError
from http import HTTPStatus
import logging

# Internal libraries
from libraries.configuration_file import get_configuration_file
from libraries.image_creator import PlaceholderImageCreator
from libraries.paths import IMAGES_DIRECTORY_PATH
from libraries.models import Image

# Initialize things
logger = logging.getLogger(__name__)
api = Blueprint(__name__, "api_routes")
# Load config
config = get_configuration_file()
IMAGE_FONT = config["image_font"]
API_DEFAULTS = config["api_defaults"]
# Load optional variables and their defaults
ENABLE_CACHING = config.get("caching", True)
CACHING_DIRECTORY = config.get("caching_directory", IMAGES_DIRECTORY_PATH)
DEFAULT_CACHE_FORMAT = "{width}x{height}_{background_color}_{text_color}.png"
CACHE_FORMAT = config.get("caching_directory", DEFAULT_CACHE_FORMAT)
ERROR_IMAGE_BACKGROUND_COLOR = config.get("error_image_background_color", "#e37f7f")
ERROR_IMAGE_TEXT_COLOR = config.get("error_image_text_color", "#753636")
# Initialize an image creator
image_creator = PlaceholderImageCreator(
    use_cache=ENABLE_CACHING,
    image_font=IMAGE_FONT,
    cache_directory=CACHING_DIRECTORY,
    cache_format=CACHE_FORMAT,
)


def generate_error_response(error_message):
    """Creates an error image with the error message being
    displayed."""
    error_image = Image(
        width=512,
        height=512,
        text=error_message,
        background_color=ERROR_IMAGE_BACKGROUND_COLOR,
        text_color=ERROR_IMAGE_TEXT_COLOR,
    )
    return image_creator.create_image(error_image)


@api.route("/placeholder")
def return_placeholder():
    """Returns a placeholder."""
    logger.debug("Got a request to /placeholder.")
    # Validate arguments
    if request.args is not None:
        logger.debug(f"Validating arguments {request.args}...")
        # Do not allow custom text to prevent service abuse/non-serious uses
        if "text" in request.args:
            del request.args["text"]
        # Use pydantic to validate the arguments
        image = None
        try:
            image = Image(**request.args)
            logger.info(
                "Got a request to /placeholder with valid args. Creating image..."
            )
            image_filepath = image_creator.create_image(image)
            logger.info("Image created.")
        except ValidationError as e:
            logger.info("Invalid arguments passed. Returning error...")
            error_message = f"""Validation errors: \n{e}.\nRefer to the documentation for further help."""
            image_filepath = generate_error_response(error_message)
    else:
        image_filepath = generate_error_response(
            "No arguments passed. Refer to the documentation for further help."
        )
    logger.info(f"Returning image {image_filepath} to user...")
    return send_from_directory(CACHING_DIRECTORY, image_filepath)
