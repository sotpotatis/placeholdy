from libraries.image_creator import PlaceholderImageCreator
from libraries.models import Image

p = PlaceholderImageCreator("fonts/Tuffy-Bold.ttf", False)
p.create_image(Image(width=120, height=120))
