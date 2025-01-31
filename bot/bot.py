import os
import telebot
from config import *
from models.diffusion_model import generate_image
from models.text_generator import generate_text
from utils.utils import import_token, save_image
from meme_generator import put_text_on_image

# Make bot session
token = import_token(os.path.curdir)
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text', 'image'])
def send_meme(message):
    if message.from_user.username is not None:
        if message.text == '/start':
            return

        print("Сообщение от пользователя:", message.from_user.username)
        print("Текст сообщения::", message.text)

        bot.send_message(MY_CHAT_ID, f'Сообщение: {message.text}')
        bot.send_message(MY_CHAT_ID, f'От пользователя: {message.from_user.username}')

        print('Начата генерация фото')
        image = generate_image()
        print('Фото сгенерировано')

        print('Начата генерация текста')
        text = generate_text()
        print('Текст сгенерирован')

        meme = put_text_on_image(image, text)

        path = 'generated_data/generated_meme.png'
        save_image(meme, path)
        print('Мем создан')

        try:
            file = open(path, 'rb')
            try:
                if message.text != 'мем' and message.text != 'Мем':
                    bot.send_photo(MY_CHAT_ID, file, caption=message.text)
                else:
                    bot.send_photo(MY_CHAT_ID, file)
                print("Мем отправлен")
            except Exception as e:
                print("Error sending the photo")
                print(e)
        except Exception as e:
            print("Error reading the file")
            print(e)


# Loop for code execution
bot.infinity_polling(timeout=10, long_polling_timeout=5)