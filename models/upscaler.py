from io import BytesIO

import fal_client
from PIL import Image
import requests
from config import UPSCALER_PARAMS
from dotenv import load_dotenv

from utils import upload_to_imgbb

# Загрузка переменной окружения с FAL_KEY
load_dotenv()


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])


def upscale(image, factor=2):
    image_url = upload_to_imgbb(image)

    params = UPSCALER_PARAMS
    params["image_url"] = image_url
    params["upscale_factor"] = factor

    result = fal_client.subscribe(
        "fal-ai/clarity-upscaler",
        arguments=params,
        with_logs=True,
        on_queue_update=on_queue_update,
    )

    response = requests.get(result["image"]['url'])
    response.raise_for_status()

    img_data = BytesIO(response.content)
    pil_image = Image.open(img_data)

    return pil_image

