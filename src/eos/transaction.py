"""
Provide implementation of transaction.
"""
import os
import telebot

from eosiopy.eosioparams import EosioParams
from eosiopy.nodenetwork import NodeNetwork
from eosiopy.rawinputparams import RawinputParams
from eosiopy import eosio_config

MASTER_WALLET_PRIVATE_KEY = os.environ.get('MASTER_WALLET_PRIVATE_KEY')
NODEOS_HOST = os.environ.get('NODEOS_HOST')
NODEOS_PORT = os.environ.get('NODEOS_PORT')

eosio_config.url = f'http://{NODEOS_HOST}'
eosio_config.port = int(NODEOS_PORT)
logger = telebot.logger


class Transaction:
    """
    Transaction implementation.
    """

    def send(self, account_from_name, account_to_name, amount, symbol) -> str:
        """
        Send transaction.
        """
        raw_input_params = RawinputParams('transfer', {
            'from': account_from_name,
            'memo': 'Remme Protocol transaction.',
            'quantity': f'{amount}.0000 {symbol}',
            'to': account_to_name,
        }, 'rem.token', f'{account_from_name}@active')

        eosio_params = EosioParams(raw_input_params.params_actions_list, MASTER_WALLET_PRIVATE_KEY)

        transaction = NodeNetwork.push_transaction(eosio_params.trx_json)
        logger.info(f'TRANSACTION RESPONSE: {transaction}')
        return transaction.get('transaction_id')
