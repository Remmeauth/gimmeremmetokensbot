"""
Provide implementation of Telegram bot core.
"""
import os

import telebot
from flask import Flask, request

from remme.account import RemmeAccount
from database import (
    check_if_user_exist,
    create_db_tables,
    get_public_key,
    insert_starter_user_info,
)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Send initial text for user.

    Contains generation new account (address, public key and private key) and publishing it.
    """
    remme = RemmeAccount(private_key_hex=None)

    chat_message = \
        'Hello, we appreciate your attention on Global Hack Weekend and participation in REMME challenges.\n' \
        'For dealing with REMME stuff we send you newly created account which you can request ' \
        'REMME \ntokens for testing purposes for! \n' \
        f'Address: {remme.address}\n' \
        f'Public key: {remme.public_key_hex}\n' \
        f'Private key: {remme.private_key_hex}\n'

    bot.send_message(message.chat.id, chat_message)


@server.route("/" + TOKEN, methods=['POST'])
def getMessage():
    """
    Read new updates.
    """
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )

    return "!", 200


@server.route("/")
def webhook():
    """
    Initialize webhook for production server.
    """
    bot.remove_webhook()
    bot.set_webhook(url="https://intense-harbor-47746.herokuapp.com/" + TOKEN)

    return '!', 200


if __name__ == '__main__':
    create_db_tables()

    if os.environ.get('ENVIRONMENT') == 'production':
        server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    if os.environ.get('ENVIRONMENT') == 'local':
        bot.polling()
