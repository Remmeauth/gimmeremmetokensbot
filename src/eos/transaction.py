"""
Provide implementation of transaction.
"""
import os

from eosiopy.eosioparams import EosioParams
from eosiopy.nodenetwork import NodeNetwork
from eosiopy.rawinputparams import RawinputParams
from eosiopy import eosio_config

MASTER_WALLET_PRIVATE_KEY = os.environ.get('MASTER_WALLET_PRIVATE_KEY')
NODEOS_HOST = os.environ.get('NODEOS_HOST')
NODEOS_PORT = os.environ.get('NODEOS_PORT')

eosio_config.url = f'https://{NODEOS_HOST}'
eosio_config.port = int(NODEOS_PORT)


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
        }, 'eosio.token', f'{account_from_name}@active')

        eosio_params = EosioParams(raw_input_params.params_actions_list, MASTER_WALLET_PRIVATE_KEY)

        transaction = NodeNetwork.push_transaction(eosio_params.trx_json)
        return transaction.get('transaction_id')
