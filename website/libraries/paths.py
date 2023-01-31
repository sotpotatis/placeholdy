"""paths.py
Contains static definitions for paths."""
import os, logging

logger = logging.getLogger(__name__)
FILE_PATH = os.path.realpath(__file__)
LIBRARIES_DIR = os.path.dirname(FILE_PATH)
CODE_DIR = os.path.dirname(LIBRARIES_DIR)
STATIC_DIR = os.path.join(CODE_DIR, "static")
WORKING_DIR = os.getenv("PLACEHOLDY_WORKING_DIRECTORY", os.getcwd())
CONFIGURATION_FILE_PATH = os.path.join(
    WORKING_DIR, "config.json5"
)  # Location of the config file
IMAGES_DIRECTORY_PATH = os.getenv(
    "PLACEHOLDY_IMAGES_DIRECTORY", os.path.join(WORKING_DIR, "images")
)  # Location of the image directory
# Check for uncreated config file
if not os.path.exists(CONFIGURATION_FILE_PATH):
    raise FileNotFoundError(
        f"Can not find configuration file. (Make sure that it exists on {CONFIGURATION_FILE_PATH})."
    )
# Create image storage directory if exists
if not os.path.exists(IMAGES_DIRECTORY_PATH):
    logger.info(f"Creating path for storing images ({IMAGES_DIRECTORY_PATH})...")
    os.mkdir(IMAGES_DIRECTORY_PATH)
    logger.info("Path for storing images created.")
