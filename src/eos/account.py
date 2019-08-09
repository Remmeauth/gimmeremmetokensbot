"""
Provide implementation of account.
"""
import json
import os
import requests

import eospy.keys
import telebot
from eospy.cleos import Cleos

APPLICATION_JSON_HEADERS = {
    'accept': "application/json",
    'content-type': "application/json"
}

MASTER_WALLET_PRIVATE_KEY = os.environ.get('MASTER_WALLET_PRIVATE_KEY')
MASTER_ACCOUNT_NAME = os.environ.get('MASTER_ACCOUNT_NAME')
NODEOS_HOST = os.environ.get('NODEOS_HOST')
NODEOS_PORT = os.environ.get('NODEOS_PORT')

NODEOS_API_URL = f'http://{NODEOS_HOST}:{NODEOS_PORT}/v1/'

logger = telebot.logger


class Account:
    """
    Account implementation.
    """

    def get_balance(self, name, symbol) -> str:
        """
        Get balance of the account.
        """
        payload = {
            'account': name,
            'code': 'rem.token',
            'symbol': symbol,
        }

        response = requests.post(
            NODEOS_API_URL + 'chain/get_currency_balance',
            data=json.dumps(payload),
            headers=APPLICATION_JSON_HEADERS,
        )

        try:
            return response.json().pop(0).replace(f' {symbol}', '')
        except (KeyError, IndexError):
            return '0.0000'

    def create(self, wallet_public_key, name, symbol, stake_quantity):
        """
        Create account.
        """
        response = Cleos(url=f'http://{NODEOS_HOST}:{NODEOS_PORT}').create_account(
            MASTER_ACCOUNT_NAME,
            eospy.keys.EOSKey(MASTER_WALLET_PRIVATE_KEY),
            name,
            wallet_public_key,
            wallet_public_key,
            stake_quantity=f'{stake_quantity}.0000 {symbol}',
            ramkb=8,
            permission='active',
            transfer=True,
            broadcast=True,
        )

        logger.info(f'Account creation response: {response}')
