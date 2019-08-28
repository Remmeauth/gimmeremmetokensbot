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
    get_account_name,
    get_public_key,
    get_private_key,
    get_request_tokens_datetime,
    insert_starter_user_info,
    update_request_tokens_datetime,
)
from eos.account import Account
from eos.transaction import Transaction
from eos.wallet import Wallet
from utils import generate_account_name

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
PRODUCTION_HOST = os.environ.get('PRODUCTION_HOST')
ENVIRONMENT = os.environ.get('ENVIRONMENT')
MASTER_WALLET_PRIVATE_KEY = os.environ.get('MASTER_WALLET_PRIVATE_KEY')
MASTER_ACCOUNT_NAME = os.environ.get('MASTER_ACCOUNT_NAME')
TRANSACTIONS_SYMBOL = os.environ.get('TRANSACTIONS_SYMBOL')
STABLE_REMME_TOKENS_REQUEST_AMOUNT = int(os.environ.get('STABLE_REMME_TOKENS_REQUEST_AMOUNT'))
REQUEST_TOKENS_PERIOD_IN_HOURS_LIMIT = os.environ.get('REQUEST_TOKENS_PERIOD_IN_HOURS_LIMIT')
STAKE_QUANTITY = os.environ.get('STAKE_QUANTITY')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


def render_main_keyboard(message):
    """
    Render main keyboard.
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Get my account credentials', REQUEST_TOKENS_KEYBOARD_BUTTON, CHECK_MY_BALANCE_KEYBOARD_BUTTON)
    bot.send_message(message.from_user.id, 'Choose one of the the following keyboard buttons:', reply_markup=keyboard)


def is_request_tokens_possible(message, request_tokens_period_in_hours_limit):
    """
    Check if last user's tokens request is fit to set period.

    We have last user's request date and time and variable with limit of requests period.
    If user's time in second less than limit's one, user's cannot ask more tokens.

    1. Get last user's tokens request datetime.
    2. Get difference between now datetime and user's in seconds.
    3. Get limit variable in hours, convert to seconds and equals with user's one.
    4. If user's tokens request time in seconds is not more that periodic limit time in seconds, return False.
    5. Else, return True.
    """
    request_tokens_datetime = get_request_tokens_datetime(message.chat.id)

    if request_tokens_datetime is not None:
        request_tokens_period_in_seconds_limit = request_tokens_period_in_hours_limit * 60 * 60

        time_from_last_token_request = datetime.now() - request_tokens_datetime
        time_from_last_token_request_in_seconds = time_from_last_token_request.total_seconds()

        if time_from_last_token_request_in_seconds < request_tokens_period_in_seconds_limit:
            return False

    return True


@bot.message_handler(func=lambda message: message.text == 'Get my account credentials', content_types=['text'])
def handle_getting_account_credentials(message):
    """
    Handle user's request to check address tokens balance.
    """
    try:
        account_name = get_account_name(chat_id=message.chat.id)
        public_key = get_public_key(chat_id=message.chat.id)
        private_key = get_private_key(chat_id=message.chat.id)

        balances_message = \
            f'Your account name: {account_name}\n' \
            f'Your owner/active public key: {public_key}'

        if private_key is None:
            balances_message += '\n\nYour private key cannot be fetched because we started supporting the restoring ' \
                                'account data after the time you got credentials.'
        else:
            balances_message += f'\nYour owner/active private key: {private_key}'

        bot.send_message(message.chat.id, balances_message)

    except psycopg2.ProgrammingError:
        bot.send_message(message.chat.id, SOMETHING_WENT_WRONG_PHRASE)


@bot.message_handler(func=lambda message: message.text == CHECK_MY_BALANCE_KEYBOARD_BUTTON, content_types=['text'])
def handle_check_balance_button(message):
    """
    Handle user's request to check address tokens balance.
    """
    try:
        account_name = get_account_name(chat_id=message.chat.id)

        user_tokens_balance, user_stake_balance, total_balance  = Account().get_balance(
            name=account_name, symbol=TRANSACTIONS_SYMBOL,
        )

        balances_message = \
            f'Your staked tokens: {user_stake_balance} REM\n' \
            f'Your unstaked tokens: {user_tokens_balance} REM\n' \
            f'Total: {total_balance} REM'

        bot.send_message(message.chat.id, balances_message)

    except psycopg2.ProgrammingError:
        bot.send_message(message.chat.id, SOMETHING_WENT_WRONG_PHRASE)


@bot.message_handler(func=lambda message: message.text == REQUEST_TOKENS_KEYBOARD_BUTTON, content_types=['text'])
def handle_gimme_tokens_button(message):
    """
    Handle user's request a new batch of Remme tokens.
    """
    try:
        _, _, total_balance = Account().get_balance(name=MASTER_ACCOUNT_NAME, symbol=TRANSACTIONS_SYMBOL)
        master_account_tokens_balance = int(float(total_balance))

        if int(master_account_tokens_balance) < STABLE_REMME_TOKENS_REQUEST_AMOUNT:
            bot.send_message(message.chat.id, FAUCET_IS_EMPTY_PHRASE)
            return

        account_to_name = get_account_name(chat_id=message.chat.id)

        if ENVIRONMENT == 'production':

            request_tokens_period_in_hours_limit = os.environ.get('REQUEST_TOKENS_PERIOD_IN_HOURS_LIMIT')

            if not is_request_tokens_possible(
                    message=message,
                    request_tokens_period_in_hours_limit=int(request_tokens_period_in_hours_limit),
            ):
                bot.send_message(
                    message.chat.id,
                    f'You are able to request tokens only once per {request_tokens_period_in_hours_limit} hours.',
                )
                return

        sent_transaction_id = Transaction().send(
            account_from_name=MASTER_ACCOUNT_NAME,
            account_to_name=account_to_name,
            amount=STABLE_REMME_TOKENS_REQUEST_AMOUNT,
            symbol=TRANSACTIONS_SYMBOL,
        )
        update_request_tokens_datetime(chat_id=message.chat.id)

        bot.send_message(
            message.chat.id,
            f'Tokens have been sent! Transaction identifier is:\n{sent_transaction_id}',
        )

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
        render_main_keyboard(message=message)
        return

    wallet = Wallet()
    account_name = generate_account_name()

    Account().create(
        wallet_public_key=wallet.public_key,
        name=account_name,
        symbol=TRANSACTIONS_SYMBOL,
        stake_quantity=STAKE_QUANTITY,
    )

    logger.info(f'Account with name `{account_name}` is created.')

    Transaction().send(
        account_from_name=MASTER_ACCOUNT_NAME,
        account_to_name=account_name,
        amount=STABLE_REMME_TOKENS_REQUEST_AMOUNT,
        symbol=TRANSACTIONS_SYMBOL,
    )

    account_credentials_message_part = \
        f'\nWe have automatically created an account with some REM tokens for you:' \
        f'*\nAccount name*: {account_name}' \
        f'*\nOwner/active public key*: {wallet.public_key}' \
        f'*\nOwner/active private key*: {wallet.private_key}'

    insert_starter_user_info(
        chat_id=message.chat.id,
        nickname=message.from_user.username,
        account_name=account_name,
        public_key=wallet.public_key,
        private_key=wallet.private_key,
        are_creads_shown=True,
    )

    bot_start_message = \
        START_COMMAND_BOT_GREETING_PHRASE + \
        account_credentials_message_part + \
        START_COMMAND_BOT_TESTNET_INTERACTIONS_PHRASE

    bot.send_message(message.chat.id, bot_start_message, parse_mode='Markdown')
    render_main_keyboard(message=message)


@server.route('/' + TOKEN, methods=['POST'])
def get_updates_from_telegram():
    """
    Push updates from Telegram to bot pull.
    """
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
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
