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

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=PRODUCTION_HOST + '/' + TOKEN)
    return "!", 200


if __name__ == '__main__':
    create_db_tables()

    if os.environ.get('ENVIRONMENT') == 'production':
        server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    if os.environ.get('ENVIRONMENT') == 'development':
        bot.polling()
