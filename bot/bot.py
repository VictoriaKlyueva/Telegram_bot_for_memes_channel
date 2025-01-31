import os
import logging
import telebot
from config import WORKING_CHAT_ID
from models.diffusion_model import generate_image
from models.text_generator import generate_text
from utils.utils import import_token, save_image
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
        self._register_handlers()

    def _register_handlers(self):
        self.bot.message_handler(
            content_types=['text', 'image']
        )(self._handle_message)

    def _log_request(self, message: telebot.types.Message) -> None:
        user_info = f"@{message.from_user.username} ({message.from_user.id})"
        logger.info(f"New request from {user_info}: {message.text}")

        # Send notification to admin
        self.bot.send_message(
            WORKING_CHAT_ID,
            f"New request from {user_info}:\n{message.text}"
        )

    @staticmethod
    def _create_meme() -> str:
        logger.info("Starting meme generation pipeline")

        # Generate components
        image = generate_image()
        text = generate_text()

        # Combine components
        meme = put_text_on_image(image, text)

        # Save result
        path = 'generated_data/generated_meme.png'
        save_image(meme, path)
        logger.info(f"Meme saved to {path}")

        return path

    def _send_meme(self, message: telebot.types.Message, meme_path: str) -> None:
        try:
            with open(meme_path, 'rb') as f:
                caption = message.text if message.text.lower() not in ['мем', 'meme'] else None

                self.bot.send_photo(
                    chat_id=WORKING_CHAT_ID,
                    photo=f,
                    caption=caption
                )
            logger.info("Мем отправлен!")

        except Exception as e:
            logger.error(f"Ошибка при отправке: {str(e)}")
            self.bot.reply_to(
                message,
                "Произошла ошибка при создании мема("
            )

    def _handle_message(self, message: telebot.types.Message) -> None:
        if message.text == '/start':
            return

        self._log_request(message)

        try:
            meme_path = self._create_meme()
            self._send_meme(message, meme_path)

        except Exception as e:
            logger.error(f"Meme creation failed: {str(e)}")
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
