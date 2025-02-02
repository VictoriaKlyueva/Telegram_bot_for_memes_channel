import io
import os
import numpy as np
import random
import requests


def import_token(path):
    with open(os.path.join(path, 'token.txt')) as f:
        token = f.read().strip()
    return token


def import_imgbb_api(path):
    with open(os.path.join(path, 'imgbb_api.txt')) as f:
        text = f.read().strip()
    return text


def upload_to_imgbb(pil_image, image_format="JPEG"):
    url = "https://api.imgbb.com/1/upload"
    api_key = import_imgbb_api(os.path.curdir)

    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format=image_format)
    byte_arr.seek(0)

    response = requests.post(url, data={"key": api_key}, files={"image": byte_arr})
    if response.status_code == 200:
        return response.json()["data"]["url"]
    else:
        raise Exception(f"Не удалось загрузить фото. Код ошибки: {response.status_code}")


def soft_max(output):
    exp_values = np.exp(output)
    return (exp_values / np.sum(exp_values))[1]


def save_image(image, path):
    image.save(path)


def text_post_processing(text):
    return text.replace('\n', '').replace('&nbsp;', ' ').split('  ')


def get_prompt():
    path = os.path.join(os.path.curdir, 'prompts_data')
    file_path = os.path.join(path, "prompts_ideas.txt")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file or directory: '{file_path}'")

    with open(file_path, "r", encoding="utf-8") as prompts_object:
        prompts = prompts_object.read().replace('\r', '').split('\n')

    prompt = random.choice(prompts).split()
    prompt = prompt if len(prompt) <= 3 else prompt[:random.randint(1, 3)]
    prompt = ' '.join(prompt)

    if len(prompt) == 1:
        addition = random.choice(prompts)
        prompt += ' ' + addition

    return prompt


def dynamic_text_position(size, text):
    width, height = size
    font_size = int(930 / (1.05 * len(text)))
    x = min(0.05 * width, 20)
    y = height - font_size - 20

    return font_size, x, y


def add_shadow(text, draw, font, x, y, offset=3, shadow_color='black'):
    for off in range(offset):
        draw.text((x - off, y), text, font=font, fill=shadow_color)
        draw.text((x + off, y), text, font=font, fill=shadow_color)
        draw.text((x, y + off), text, font=font, fill=shadow_color)
        draw.text((x, y - off), text, font=font, fill=shadow_color)
        draw.text((x - off, y + off), text, font=font, fill=shadow_color)
        draw.text((x + off, y + off), text, font=font, fill=shadow_color)
        draw.text((x - off, y - off), text, font=font, fill=shadow_color)
        draw.text((x + off, y - off), text, font=font, fill=shadow_color)
