from remme_client.remme.remme_atomic_swap import RemmeSwap
from remme_client.remme.remme_batch import RemmeBatch
from remme_client.remme.remme_blockchain_info import RemmeBlockchainInfo
from remme_client.remme.remme_certificate import RemmeCertificate
from remme_client.remme.remme_token import RemmeToken
from remme_client.remme.remme_account import RemmeAccount
from remme_client.remme.remme_api import RemmeAPI
from remme_client.remme.remme_transaction_service import RemmeTransactionService
from remme_client.remme.remme_public_key_storage import RemmePublicKeyStorage
from remme_client.remme.remme_websocket_events import RemmeWebSocketEvents

__author__ = 'dethline'


class Remme:
    """
    Class representing a client for Remme.
    """

    _private_key_hex = None
    _network_config = None
    _api = None
    account = None
    transaction_service = None
    public_key_storage = None
    certificate = None
    token = None
    batch = None
    swap = None
    blockchain_info = None
    events = None

    def __init__(self, private_key_hex="", network_config=None):
        """
        :param private_key_hex: The hex of private key. Which is used for creating account in library
        which would sign transactions.
        :param network_config: The config of network.
        """
        default_network_config = {'node_address': "localhost", 'node_port': "8080", 'ssl_mode': False}

        self._private_key_hex = private_key_hex
        self._network_config = default_network_config if network_config is None else network_config

        self._api = RemmeAPI(self._network_config)
        self.account = RemmeAccount(self._private_key_hex)

        self.transaction_service = RemmeTransactionService(self._api, self.account)
        self.public_key_storage = RemmePublicKeyStorage(self._api, self.account, self.transaction_service)
        self.certificate = RemmeCertificate(self.public_key_storage)
        self.token = RemmeToken(self._api, self.transaction_service)
        self.batch = RemmeBatch(self._api)
        self.swap = RemmeSwap(self._api, self.transaction_service)
        self.blockchain_info = RemmeBlockchainInfo(self._api)
        self.events = RemmeWebSocketEvents(self._api.node_address, self._api.ssl_mode)
