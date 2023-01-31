"""image_creator.py
The actual code that creates the placeholder images."""
import logging
import os.path
from typing import Optional
from .models import Image
from PIL import Image, ImageDraw, ImageFont, ImageColor


class PlaceholderImageCreator:
    """A creator capable of creating placeholder images."""

    def __init__(
        self,
        image_font: str,
        use_cache: bool,
        cache_directory: Optional[str] = None,
        cache_format: Optional[str] = None,
    ):
        """Initializes an image creator.

        :param image_font: The font to use for the image.

        :param use_cache: Whether to use the cache or not. To avoid creating images multiple times,
        it is highly recommended to use a cache directory. The creator will load
        cached files from it if the request is repeated.

        :param cache_directory: Sets the image cache directory where the cache is loaded from.
        See use_cache for more information

        :param cache_format: The format that the cache image files use."""
        self.use_cache = use_cache
        self.cache_directory = cache_directory
        self.cache_format = cache_format
        self.image_font = image_font
        self.logger = logging.getLogger(__name__)

    def calculate_font(
        self, image: Image, image_draw, image_pil, font_name: str
    ) -> ImageFont.FreeTypeFont:
        """Calculates and returns the font to use for an image based on the biggest available font size.

        :param image: The image to be created.

        :param font_name: The font name/path to use."""
        size_breakpoint = 0.8 * min({image.width, image.height})
        current_font = ImageFont.truetype(font_name, 0)
        while image_draw.textsize(image.text, current_font)[0] < size_breakpoint:
            current_font = ImageFont.truetype(font_name, current_font.size + 1)
        return current_font

    def format_image_filepath(self, image: Image) -> str:
        """To use the cache, images will be saved using the defined file format.
        This format will format the filename by passing the Image as a dict.

        :param image: The image to retrive details from.

        :returns A formatted version of the current image format with image details
        filled out."""
        format_parameters = image.dict()
        format_parameters["background_color"] = str(image.background_color)
        format_parameters["text_color"] = str(image.text_color)
        output_filepath = self.cache_format
        for parameter_key, parameter_value in format_parameters.items():
            format_entry_text = "{%s}" % (parameter_key)
            output_filepath = output_filepath.replace(
                format_entry_text, str(parameter_value)
            )
        output_filepath = output_filepath.replace("\n", "").strip().replace(" ", "_")
        return output_filepath

    def draw_image(self, image: Image) -> str:
        """Draws an image.

        :param image: The image information to create.

        :returns The output RELATIVE (to self.cache_directory) path of the image."""
        self.logger.info(f"Creating image using details {image}...")
        # Start by initializing a canvas and getting text colors.
        # The color names will already be validated
        background_color_rgb = ImageColor.getrgb(image.background_color)
        text_color_rgb = ImageColor.getrgb(image.text_color)
        image_pil = Image.new(
            mode="RGB", size=(image.width, image.height), color=background_color_rgb
        )
        # Initialize ImageDraw object
        image_draw = ImageDraw.ImageDraw(image_pil)
        # Create font
        image_font = self.calculate_font(image, image_draw, image_pil, self.image_font)
        # Add font text
        image_draw.text(
            text=image.text,
            font=image_font,
            fill=text_color_rgb,
            xy=(image.width / 2, image.height / 2),
            anchor="mm",  # Align the font to the middle (finally they made this sexy!)
        )
        image_filename = self.format_image_filepath(image)
        image_filepath = os.path.join(self.cache_directory, image_filename)
        self.logger.info(f"Image created. Saving as {image_filepath}...")
        image_pil.save(image_filepath)
        self.logger.info("Image created.")
        return image_filename

    def create_image(self, image: Image) -> str:
        """Creates an image or loads it from the cache.

        :param image: The image information to create.

        :returns The output RELATIVE (to self.cache_directory) path of the image."""
        self.logger.info(f"Checking for image with details {image} in cache...")
        image_filepath = self.format_image_filepath(
            image
        )  # Get where the image would be stored if it is
        if not self.use_cache or image_filepath not in os.listdir(self.cache_directory):
            self.logger.info(
                "Image not previously created or cache disabled. Creating file..."
            )
            return self.draw_image(image)  # Return the new (relative) filepath
        else:
            self.logger.info(f"Loading cached image from {image_filepath}...")
            return image_filepath  # Return the relative filepath
