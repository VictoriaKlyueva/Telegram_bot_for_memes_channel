import telebot
import os


def import_token(path):
    with open(os.path.join(path, 'token.txt')) as f:
        token = f.read().strip()

    return token


def main(name):
    token = import_token('')
    bot = telebot.TeleBot('')


if __name__ == '__main__':
    main('PyCharm')
