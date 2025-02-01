import os
import logging
import telebot
from telebot import types
from config import WORKING_CHAT_ID, MY_CHAT_ID, CHANNEL_ID
from models.flux import generate_image_flux
from models.diffusion_model import generate_image_diffuser
from models.text_generator import generate_text
from utils import import_token, save_image
from meme_generator import put_text_on_image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MemeBot:
    def __init__(self):
        self.token = import_token(os.path.curdir)
        self.bot = telebot.TeleBot(self.token)
        self.user_captions = {}
        self._register_handlers()

    def _register_handlers(self):
        self.bot.message_handler(commands=['start'])(self._handle_start)
        self.bot.message_handler(content_types=['text'])(self._handle_message)

    def _handle_start(self, message: telebot.types.Message):
        user_status = self.bot.get_chat_member(CHANNEL_ID, message.from_user.id).status
        if user_status not in ['member', 'administrator', 'creator']:
            self.bot.send_message(message.chat.id, "Перед работой с ботом надо сначала подписаться на группу!")
            return

        self.bot.send_message(message.chat.id,
                              "Привет! С помощью этого бота ты можешь сгенерировать мем с котом в группу! Задор!")
        self.bot.send_message(message.chat.id,
                              "Просто напиши свою подпись к мему, а он автоматически сгенерируется и отправится💫")

    def _log_request(self, message: telebot.types.Message) -> None:
        user_info = f"@{message.from_user.username} ({message.from_user.id})"
        logger.info(f"New request from {user_info}: {message.text}")

        # Send notification to admin
        self.bot.send_message(
            MY_CHAT_ID,
            f"New request from {user_info}:\n{message.text}"
        )

    def _handle_message(self, message: telebot.types.Message) -> None:
        user_status = self.bot.get_chat_member(CHANNEL_ID, message.from_user.id).status
        if user_status not in ['member', 'administrator', 'creator']:
            self.bot.send_message(message.chat.id, "Перед работой с ботом надо сначала подписаться на группу!")
            return

        self._log_request(message)
        self.user_captions[message.chat.id] = message.text

        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Хочу обосрыша!🤩")
        btn2 = types.KeyboardButton("Давайте нормального.😐")
        markup.add(btn1, btn2)

        self.bot.send_message(message.chat.id, "Ты хочешь сгенерировать обосрыша или нормального кота?",
                              reply_markup=markup)
        self.bot.register_next_step_handler(message, self._handle_choice)

    def _handle_choice(self, message: telebot.types.Message) -> None:
        self.bot.send_message(message.chat.id, "Начата генерация мема...")

        if message.text == "Хочу обосрыша!🤩":
            image = generate_image_diffuser()
        else:
            image = generate_image_flux()

        caption = self.user_captions.get(message.chat.id, "Вот твой мем!")
        meme = put_text_on_image(image, caption)

        # Save result
        path = 'generated_data/generated_meme.png'
        save_image(meme, path)
        self._send_meme(message, path, caption)

    def _send_meme(self, message: telebot.types.Message, meme_path: str, caption: str) -> None:
        try:
            with open(meme_path, 'rb') as f:
                self.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=f,
                    caption=caption
                )
            self.bot.send_message(message.chat.id, "Мем отправлен ✅")
            logger.info("Мем отправлен!")
        except Exception as e:
            logger.error(f"Ошибка при отправке: {str(e)}")
            self.bot.reply_to(
                message,
                "Произошла ошибка при создании мема("
            )

    def run(self):
        logger.info("Бот запущен")
        self.bot.infinity_polling(
            timeout=10,
            long_polling_timeout=5
        )
