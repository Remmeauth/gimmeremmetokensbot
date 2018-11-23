"""
Provide implementation of Telegram bot core.
"""
import logging
import os

import telebot
from flask import Flask, request

from remme.account import RemmeAccount
from remme.token import RemmeToken
from database import (
    check_if_user_exist,
    create_db_tables,
    get_address,
    get_public_key,
    insert_starter_user_info,
)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
MASTER_ACCOUNT_PRIVATE_KEY = os.environ.get('MASTER_ACCOUNT_PRIVATE_KEY')
PRODUCTION_HOST = os.environ.get('PRODUCTION_HOST')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


def render_keyboard(message):
    """
    Render main keyboard.
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Gimme Remme tokens', 'I want to check my balance')
    bot.send_message(message.from_user.id, 'Choose something:', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Gimme Remme tokens', content_types=['text'])
def handle_gimme_tokens_button(message):
    """
    Handle user's request to send Remme token to his address.
    """
    public_key = get_public_key(chat_id=message.chat.id)

    batch_id = RemmeToken(private_key_hex=MASTER_ACCOUNT_PRIVATE_KEY).send_transaction(public_key_to=public_key)
    bot.send_message(message.chat.id, f'Tokens have been sent! Batch identifier is: {batch_id}')


@bot.message_handler(func=lambda message: message.text == 'I want to check my balance', content_types=['text'])
def handle_check_balance_button(message):
    """
    Handle user's request to check balance his balance.
    """
    token_balance = RemmeToken().get_balance(
        address=get_address(chat_id=message.chat.id),
    )

    bot.send_message(message.chat.id, f'Your tokens balance is: {token_balance}')


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Send initial text for user.

    Contains generation new account (address, public key and private key) and publishing it.
    """
    remme = RemmeAccount(private_key_hex=None)
    logger.info(f'Account with address `{remme.address}` is created.')

    is_user = check_if_user_exist(chat_id=message.chat.id)

    if is_user:
        bot.send_message(message.chat.id, 'You already got the credentials. Find it at the start of the dialog.')
        return

    insert_starter_user_info(
        chat_id=message.chat.id,
        nickname=message.from_user.username,
        address=remme.address,
        public_key=remme.public_key_hex,
        are_creads_shown=True,
    )

    chat_message = \
        'Hello, we appreciate your attention on Global Hack Weekend and participation in REMME challenges.\n' \
        'For dealing with REMME stuff we send you newly created account which you can request ' \
        'REMME \ntokens for testing purposes for! \n\n' \
        f'Address: {remme.address}\n' \
        f'Public key: {remme.public_key_hex}\n' \
        f'Private key: {remme.private_key_hex}\n'

    bot.send_message(message.chat.id, chat_message)
    render_keyboard(message)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    """
    Read new updates.
    """
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode('utf-8'))]
    )

    return '!', 200


@server.route('/')
def webhook():
    """
    Initialize webhook for production server.
    """
    bot.remove_webhook()
    bot.set_webhook(url=PRODUCTION_HOST + '/' + TOKEN)

    return '!', 200


if __name__ == '__main__':
    create_db_tables()

    if os.environ.get('ENVIRONMENT') == 'production':
        server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    if os.environ.get('ENVIRONMENT') == 'local':
        bot.polling()
