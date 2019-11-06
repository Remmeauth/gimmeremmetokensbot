"""
Provide implementation of transaction.
"""
import os
import telebot

from eospy.keys import EOSKey
from eospy.cleos import Cleos

MASTER_WALLET_PRIVATE_KEY = os.environ.get('MASTER_WALLET_PRIVATE_KEY')
NODEOS_HOST = os.environ.get('NODEOS_HOST')
NODEOS_PORT = os.environ.get('NODEOS_PORT')
NODEOS_PORT = ':' + str(NODEOS_PORT) if NODEOS_PORT else ''

NODEOS_API_URL = f'https://{NODEOS_HOST}{NODEOS_PORT}'

logger = telebot.logger


class Transaction:
    """
    Transaction implementation.
    """

    def send(self, account_from_name, account_to_name, amount, symbol) -> str:
        """
        Send transaction.
        """
        cleos_conn = Cleos(url=NODEOS_API_URL)

        transfer_data = cleos_conn.abi_json_to_bin(
            'rem.token',
            'transfer', {
                'from': account_from_name,
                'to': account_to_name,
                'quantity': f'{amount}.0000 {symbol}',
                'memo': 'Remme Protocol transaction.'
            })
        transfer_json = {
            'account': 'rem.token',
            'name': 'transfer',
            'authorization': [{
                'actor': account_from_name,
                'permission': 'active'
            }],
            'data': transfer_data['binargs']
        }
        transaction = {"actions": [transfer_json]}

        transaction_res = cleos_conn.push_transaction(
            transaction,
            EOSKey(MASTER_WALLET_PRIVATE_KEY),
            broadcast=True,
            timeout=30
        )

        logger.info(f'TRANSACTION RESPONSE: {transaction_res}')
        return transaction_res['transaction_id']
