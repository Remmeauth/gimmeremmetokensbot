"""
Provide implementation of Telegram bot core.
"""
import os

import telebot
from flask import Flask, request

from remme.account import RemmeAccount
from remme.token import RemmeToken

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
MASTER_ACCOUNT_PRIVATE_KEY = os.environ.get('MASTER_ACCOUNT_PRIVATE_KEY')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


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
    batch_id = RemmeToken(private_key_hex=MASTER_ACCOUNT_PRIVATE_KEY).send_transaction(
        public_key_to='0262fa4ba54bc181163104be925bb4ccca61a91fb50b7fa2d9f065aa2730e3304e',
    )

    bot.send_message(message.chat.id, f'Tokens have been sent! Batch identifier is: {batch_id}')


@bot.message_handler(func=lambda message: message.text == 'I want to check my balance', content_types=['text'])
def handle_check_balance_button(message):
    """
    Handle user's request to check balance his balance.
    """
    token_balance = RemmeToken().get_balance(
        address='1120071dd9da358c3c50f15802966f89c5d82f636c8cd79203109f52e6f346dce27305',
    )

    bot.send_message(message.chat.id, f'Your tokens balance is: {token_balance}')


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
        'REMME \ntokens for testing purposes for! \n\n' \
        f'Address: {remme.address}\n' \
        f'Public key: {remme.public_key_hex}\n' \
        f'Private key: {remme.private_key_hex}\n'

    bot.send_message(message.chat.id, chat_message)
    render_keyboard(message)


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
    if os.environ.get('ENVIRONMENT') == 'production':
        server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    if os.environ.get('ENVIRONMENT') == 'local':
        bot.polling()
