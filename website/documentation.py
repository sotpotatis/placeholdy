"""documentation.py
This file defines the frontend/documentation routes of the page."""
from flask import Blueprint, render_template
from libraries.configuration_file import get_configuration_file
from libraries.paths import STATIC_DIR
from libraries.pico_css_downloader import download_pico_css
import logging, os
# Initialize things
logger = logging.getLogger(__name__)
docs = Blueprint(__name__, "documentation")

# Check that a Pico CSS file exists
PICO_CSS_FILE = os.path.join(STATIC_DIR, "pico.min.css")
if not os.path.exists(PICO_CSS_FILE):
    logger.info("Automatically downloading Pico CSS and placing into the static directory...")
    download_pico_css(PICO_CSS_FILE)
    logger.info("Pico CSS was been downloaded.")

@docs.route("/")
def index():
    logger.info("Got a request to the index page. Returning...")
    config = get_configuration_file()
    return render_template("index.html", config=config) # Expose configuration to rendered template
