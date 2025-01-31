import fal_client
from config import LORA_GENERATION_PARAMS
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO

from models.yolo_model import check_image
from utils import save_image

# Загрузка переменной окружения с FAL_KEY
load_dotenv()


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])


def generate_image():
    while True:
        try:
            result = fal_client.subscribe(
                "fal-ai/flux-lora",
                arguments=LORA_GENERATION_PARAMS,
                with_logs=True,
                on_queue_update=on_queue_update,
            )

            if "images" in result and len(result["images"]) > 0:
                print("\nУспешно сгенерировано изображений:", len(result["images"]))

                pil_images = []
                for image in result["images"]:
                    response = requests.get(image['url'])
                    response.raise_for_status()

                    img_data = BytesIO(response.content)
                    pil_image = Image.open(img_data)
                    pil_images.append(pil_image)

                image = pil_images[0]

                if check_image(image):
                    return image
                else:
                    path = f'generated_data/bad_image.png'
                    save_image(image, path)
                    print(f"Фото отклонено для изображения")

            else:
                print("Ошибка генерации: результат не содержит изображений")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Ошибка загрузки изображения: {str(e)}")
            return None
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            return None
