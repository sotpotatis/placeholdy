"""pico_css_downloader.py
Downloads Pico CSS (https://picocss.com) to a specific path."""
import requests, logging

logger = logging.getLogger(__name__)

def download_pico_css(destination_path:str):
    """Downloads the picocss.min.css file and places it into the
    set path.

    :param destination_path: The destination of the CSS file."""
    logger.info(f"Downloading Pico CSS to {destination_path}...")
    request = requests.get("https://unpkg.com/@picocss/pico@1.5.7/css/pico.min.css")
    if request.status_code != 200:
        error_message = f"Request failed. Unexpected status code {request.status_code} with text: {request.text}."
        logger.critical(error_message)
        raise Exception(error_message)
    with open(destination_path, "wb") as output_file:
        output_file.write(request.content)
    logger.info("Pico CSS was downloaded.")
