from io import BytesIO
from PIL import ImageDraw, ImageFont
from utils.utils import *


def put_text_on_image(image, text):
    draw = ImageDraw.Draw(image)

    fonts = os.listdir('fonts')
    font_choice = random.choice(fonts)
    color = (255, 255, 255)

    font_size, x, y = dynamic_text_position(text)

    with open('fonts/' + font_choice, "rb") as f:
        bytes_font = BytesIO(f.read())
    font = ImageFont.truetype(bytes_font, font_size if font_choice == "lobster.ttf" else font_size - 1)

    add_shadow(text, draw, font, x, y)
    draw.text((x, y), text, color, font=font)

    return image
