import re
from remme_client.remme.constants.remme_methods import RemmeMethods
from remme_client.remme.constants.remme_patterns import RemmePatterns
from remme_client.remme.remme_utils import is_valid_batch_id


class RemmeBlockchainInfo:

    _remme_api = None

    def __init__(self, remme_api):
        self._remme_api = remme_api

    async def get_batch_by_id(self, batch_id):
        if not is_valid_batch_id(batch_id):
            raise Exception("Invalid batch id given.")
        params = {'id': batch_id}
        return await self._remme_api.send_request(RemmeMethods.FETCH_BATCH, params)

    def get_batches(self, query):
        raise NotImplementedError

    def get_block_by_id(self, block_id):
        raise NotImplementedError

    async def get_blocks(self, query):
        query = query if query else {"start": 0, "limit": 0}
        return await self._remme_api.send_request(RemmeMethods.BLOCK_INFO, params=query)

    def get_peers(self):
        raise NotImplementedError

    def get_receipts(self):
        raise NotImplementedError

    def get_state(self):
        raise NotImplementedError

    def get_state_by_address(self, address):
        raise NotImplementedError

    def get_transaction_by_id(self, tx_id):
        raise NotImplementedError

    def get_transactions(self, query):
        raise NotImplementedError

    async def get_network_status(self):
        return await self._remme_api.send_request(RemmeMethods.NETWORK_STATUS)

    def get_block_info(self, query):
        raise NotImplementedError

