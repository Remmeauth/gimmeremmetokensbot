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
NODEOS_PORT = ':' + str(NODEOS_PORT) if NODEOS_PORT else ''
STAKE_QUANTITY = os.environ.get('STAKE_QUANTITY')
MINIMUM_STAKE = os.environ.get('MINIMUM_STAKE')

NODEOS_API_URL = f'https://{NODEOS_HOST}{NODEOS_PORT}'

logger = telebot.logger


class Account:
    """
    Account implementation.
    """

    def get_balance(self, name, symbol) -> str:
        """
        Get balance of the account.
        """
        # payload = {
        #     'account': name,
        #     'code': 'rem.token',
        #     'symbol': symbol,
        # }
        payload = {
            'account_name': name,
        }

        try:
            response = requests.post(
                NODEOS_API_URL + '/v1/chain/get_account',
                data=json.dumps(payload),
                headers=APPLICATION_JSON_HEADERS,
            )

            logger.info(f'AAA*50, {response.json()}')

            core_liquid_balance = int(response.json().get('core_liquid_balance').split('.')[0])
            staked = str(response.json().get('voter_info').get('staked'))
            staked = staked[:-4]  # remove accuracy

            logger.info(f'{core_liquid_balance}')
            logger.info(f'{staked}')

            return core_liquid_balance, staked, int(core_liquid_balance) + int(staked)

        except AttributeError:
            return f'{MINIMUM_STAKE}.0000', f'{STAKE_QUANTITY}.0000', f'{MINIMUM_STAKE + STAKE_QUANTITY}.0000'

    def create(self, wallet_public_key, name, symbol, stake_quantity):
        """
        Create account.
        """
        response = Cleos(url=NODEOS_API_URL).create_account(
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
