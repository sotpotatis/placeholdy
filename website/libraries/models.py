"""models.py
The new thing I learnt for this project - using Pydantic to
validate data."""
from pydantic import BaseModel, validator, ValidationError
from typing import List, Dict, Tuple
from .configuration_file import get_configuration_file
from PIL import ImageColor

# Get color configuration
config = get_configuration_file()
API_DEFAULTS = config["api_defaults"]
API_LIMITS = config["api_limits"]
DEFAULT_BACKGROUND_COLOR: str = API_DEFAULTS["background_color"]
DEFAULT_TEXT_COLOR: str = API_DEFAULTS["text_color"]
MAX_IMAGE_WIDTH = API_LIMITS["image_width"]
MAX_IMAGE_HEIGHT = API_LIMITS["image_height"]


class Image(BaseModel):
    """The Image class defines the input data to create a new
    placeholder image."""

    width: int  # Image width in pixels
    height: int  # Image height in pixels
    text: str = None  # Image text
    background_color: str = DEFAULT_BACKGROUND_COLOR  # Image color
    text_color: str = DEFAULT_TEXT_COLOR  # Text color

    @validator("width")
    def width_is_within_range(cls, value):
        """Validates that the image width is within the allowed range"""
        assert (
            0 < value < MAX_IMAGE_WIDTH
        ), f"Image width not in allowed range 0-{MAX_IMAGE_WIDTH}."
        return value

    @validator("height")
    def height_is_within_range(cls, value):
        """Validates that the image width is within the allowed range"""
        assert (
            0 < value < MAX_IMAGE_HEIGHT
        ), f"Image height not in allowed range 0-{MAX_IMAGE_HEIGHT}."
        return value

    @validator("background_color", "text_color", pre=True, always=True)
    def color_is_valid(cls, value):
        """Validates that a color is a valid color."""
        try:
            ImageColor.getrgb(value)
            return value
        except ValueError as e:
            raise ValueError(f"Invalid color value. ({e}")

    @validator("text", pre=True, always=True)
    def set_text_to_image_dimensions(cls, value, values):
        """Sets the text argument to the default value of the format
        {width}x{height}"""
        # If custom text is set
        if value is not None:
            return value
        # If the values are invalid (not set, make the output empty)
        if "height" in values and "width" in values:
            height = values["height"]
            width = values["width"]
            return f"{width}x{height}"
        else:
            return ""
