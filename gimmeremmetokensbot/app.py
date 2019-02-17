"""
Provide implementation of `gimmeremmetokensbot` Telegram bot.
"""
import logging
import os
from datetime import datetime

import telebot
import psycopg2
from flask import Flask, request

from constants import (
    ALREADY_GOTTEN_ACCOUNT_CREDENTIALS_PHRASE,
    CHECK_MY_BALANCE_KEYBOARD_BUTTON,
    FAUCET_IS_EMPTY_PHRASE,
    REQUEST_TOKENS_KEYBOARD_BUTTON,
    SOMETHING_WENT_WRONG_PHRASE,
    START_COMMAND_BOT_GREETING_PHRASE,
    START_COMMAND_BOT_TESTNET_INTERACTIONS_PHRASE,
)
from database import (
    check_if_user_exist,
    create_db_tables,
    get_address,
    get_public_key,
    get_request_tokens_datetime,
    insert_starter_user_info,
    update_request_tokens_datetime,
)
from remme.account import RemmeAccount
from remme.constants.amount import STABLE_REMME_TOKENS_REQUEST_AMOUNT
from remme.token import RemmeToken
from utils import send_keystore_file

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
MASTER_ACCOUNT_PRIVATE_KEY = os.environ.get('MASTER_ACCOUNT_PRIVATE_KEY')
PRODUCTION_HOST = os.environ.get('PRODUCTION_HOST')
REQUEST_TOKENS_PERIOD_IN_HOURS_LIMIT = int(os.environ.get('REQUEST_TOKENS_PERIOD_IN_HOURS_LIMIT'))

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


def is_request_tokens_possible(message, public_key):
    """
    Check if last user's tokens request is fit to set period.

    We have last user's request date and time and variable with limit of requests period.
    If user's time in second less than limit's one, user's cannot ask more tokens.

    1. Get last user's tokens request datetime;
    2. Get difference between now datetime and user's in seconds.
    3. Get limit variable in hours, convert to seconds and equals with user's one.
    4. If user's tokens request time in seconds is not more that periodic limit time in seconds, return False.
    5. Else, return True.
    """
    request_tokens_datetime = get_request_tokens_datetime(message.chat.id)

    if request_tokens_datetime is not None:
        request_tokens_period_in_seconds_limit = REQUEST_TOKENS_PERIOD_IN_HOURS_LIMIT * 60 * 60

        time_from_last_token_request = datetime.now() - request_tokens_datetime
        time_from_last_token_request_in_seconds = time_from_last_token_request.total_seconds()

        if time_from_last_token_request_in_seconds < request_tokens_period_in_seconds_limit:
            logger.info(
                f'Account with public key `{public_key}` is requesting token, '
                f'but last token request in second {time_from_last_token_request_in_seconds} not over set '
                f'{request_tokens_period_in_seconds_limit} as limit.')

            return False

    return True


@bot.message_handler(func=lambda message: message.text == REQUEST_TOKENS_KEYBOARD_BUTTON, content_types=['text'])
def handle_gimme_tokens_button(message):
    """
    Handle user's request a new batch of Remme tokens.
    """
    try:
        public_key = get_public_key(chat_id=message.chat.id)

        master_account = RemmeAccount(private_key_hex=MASTER_ACCOUNT_PRIVATE_KEY)
        master_account_token = RemmeToken(private_key_hex=MASTER_ACCOUNT_PRIVATE_KEY)

        if master_account_token.get_balance(address=master_account.address) < STABLE_REMME_TOKENS_REQUEST_AMOUNT:
            bot.send_message(message.chat.id, FAUCET_IS_EMPTY_PHRASE)
            return

        if not is_request_tokens_possible(message=message, public_key=public_key):
            bot.send_message(
                message.chat.id,
                f'You are able to request tokens only once per {REQUEST_TOKENS_PERIOD_IN_HOURS_LIMIT} hours.',
            )
            return

        batch_id = master_account_token.send_transaction(public_key_to=public_key)
        update_request_tokens_datetime(chat_id=message.chat.id)

        bot.send_message(
            message.chat.id,
            f'Tokens have been sent! Batch identifier (use it to fetch transaction data from node) is: {batch_id}',
        )

    except psycopg2.ProgrammingError:
        bot.send_message(message.chat.id, SOMETHING_WENT_WRONG_PHRASE)


@bot.message_handler(func=lambda message: message.text == CHECK_MY_BALANCE_KEYBOARD_BUTTON, content_types=['text'])
def handle_check_balance_button(message):
    """
    Handle user's request to check address tokens balance.
    """
    try:
        token_balance = RemmeToken().get_balance(
            address=get_address(chat_id=message.chat.id),
        )

        bot.send_message(message.chat.id, f'Your tokens balance is: {token_balance}')

    except psycopg2.ProgrammingError:
        bot.send_message(message.chat.id, SOMETHING_WENT_WRONG_PHRASE)


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
        bot.send_message(message.chat.id, ALREADY_GOTTEN_ACCOUNT_CREDENTIALS_PHRASE)
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
        f'*Address*: {account.address}\n'\
        f'*Public key*: {account.public_key_hex}\n' \
        f'*Private key*: {account.private_key_hex}'

    bot_start_message = \
        START_COMMAND_BOT_GREETING_PHRASE + \
        account_credentials_message_part + \
        START_COMMAND_BOT_TESTNET_INTERACTIONS_PHRASE

    bot.send_message(message.chat.id, bot_start_message, parse_mode='Markdown')

    send_keystore_file(bot=bot, message=message, account=account)

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
