import os
import numpy as np
import random
import codecs


def import_token(path):
    with open(os.path.join(path, 'token.txt')) as f:
        token = f.read().strip()
    return token


def soft_max(output):
    exp_values = np.exp(output)
    return (exp_values / np.sum(exp_values))[1]


def save_image(image, path):
    image.save(path)


def text_post_processing(text):
    return text.replace('\n', '').replace('&nbsp;', ' ').split('  ')


def get_prompt():
    path = '../prompts_data/'
    prompts_object = codecs.open(path + "prompts_ideas.txt", "r", "utf_8_sig")
    prompts = prompts_object.read().replace('\r', '').split('\n')

    prompt = random.choice(prompts).split()
    prompt = prompt if len(prompt) <= 3 else prompt[:random.randint(1, 3)]
    prompt = ' '.join(prompt)

    if len(prompt) == 1:
        addition_object = codecs.open(path + "prompts_ideas.txt", "r", "utf_8_sig")
        addition = random.choice(prompts)
        prompt += ' ' + addition

    return prompt


def dynamic_text_position(text):
    font_size = int(480 / len(text))
    x = 15
    y = 240 - font_size
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
