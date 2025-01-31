from bot.bot import bot

if __name__ == "__main__":
    bot.infinity_polling(timeout=10, long_polling_timeout=5)