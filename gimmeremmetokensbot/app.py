"""
Provide implementation of `gimmeremmetokensbot` Telegram bot.
"""
import logging
import os

import telebot
from flask import Flask, request

from remme.account import RemmeAccount
from remme.token import RemmeToken
from constants import (
    ALREADY_GOTTEN_ACCOUNT_CREDENTIALS_BOT_RESPONSE_PHRASE,
    CHECK_MY_BALANCE_KEYBOARD_BUTTON,
    REQUEST_TOKENS_KEYBOARD_BUTTON,
    START_COMMAND_BOT_RESPONSE_PHRASE,
)
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
    keyboard.row(REQUEST_TOKENS_KEYBOARD_BUTTON, CHECK_MY_BALANCE_KEYBOARD_BUTTON)
    bot.send_message(message.from_user.id, 'Choose one of the the following keyboard buttons:', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == REQUEST_TOKENS_KEYBOARD_BUTTON, content_types=['text'])
def handle_gimme_tokens_button(message):
    """
    Handle user's request a new batch of Remme tokens.
    """
    public_key = get_public_key(chat_id=message.chat.id)

    batch_id = RemmeToken(private_key_hex=MASTER_ACCOUNT_PRIVATE_KEY).send_transaction(public_key_to=public_key)
    bot.send_message(
        message.chat.id,
        f'Tokens have been sent! Batch identifier (use it to fetch transaction data from node) is: {batch_id}',
    )


@bot.message_handler(func=lambda message: message.text == CHECK_MY_BALANCE_KEYBOARD_BUTTON, content_types=['text'])
def handle_check_balance_button(message):
    """
    Handle user's request to check address tokens balance.
    """
    token_balance = RemmeToken().get_balance(
        address=get_address(chat_id=message.chat.id),
    )

    bot.send_message(message.chat.id, f'Your tokens balance is: {token_balance}')


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Send initial text for user.

    Contains generation new account (address, public key and private key) and
    publishing it as part of the responding message.

    If user already has account, send corresponding (your account already created) phrase and do nothing.
    """
    is_user = check_if_user_exist(chat_id=message.chat.id)

    if is_user:
        bot.send_message(message.chat.id, ALREADY_GOTTEN_ACCOUNT_CREDENTIALS_BOT_RESPONSE_PHRASE)
        return

    account = RemmeAccount(private_key_hex=None)
    logger.info(f'Account with address `{account.address}` is created.')

    insert_starter_user_info(
        chat_id=message.chat.id,
        nickname=message.from_user.username,
        address=account.address,
        public_key=account.public_key_hex,
        are_creads_shown=True,
    )

    account_credentials_message_part = \
        f'\n' \
        f'Address: {account.address}\n'\
        f'Public key: {account.public_key_hex}\n' \
        f'Private key: {account.private_key_hex}'

    bot.send_message(message.chat.id, START_COMMAND_BOT_RESPONSE_PHRASE + account_credentials_message_part)
    render_keyboard(message)


@server.route('/' + TOKEN, methods=['POST'])
def get_updates_from_telegram():
    """
    Push updates from Telegram to bot pull.
    """
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode('utf-8'))]
    )

    return '!', 200


@server.route('/')
def web_hook():
    """
    Initialize web-hook for production server.
    """
    bot.remove_webhook()
    bot.set_webhook(url=PRODUCTION_HOST + '/' + TOKEN)

    return '!', 200


if __name__ == '__main__':
    create_db_tables()

    if os.environ.get('ENVIRONMENT') == 'production':
        server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    if os.environ.get('ENVIRONMENT') == 'development':
        bot.polling()
