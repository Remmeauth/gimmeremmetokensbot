from remme_client.remme.constants.remme_methods import RemmeMethods


class RemmeSwap:

    _remme_api = None
    _remme_transaction_service = None

    def __init__(self, remme_api, transaction_service):
        self._remme_api = remme_api
        self._remme_transaction_service = transaction_service

    def approve(self, swap_id):
        raise NotImplementedError

    def close(self, swap_id, secret_key):
        raise NotImplementedError

    def expire(self, swap_id):
        raise NotImplementedError

    async def get_public_key(self):
        return await self._remme_api.send_request(RemmeMethods.ATOMIC_SWAP_PUBLIC_KEY)

    def get_info(self, swap_id):
        raise NotImplementedError

    def init(self, data):
        raise NotImplementedError

    def set_secret_lock(self, swap_id, secret_lock):
        raise NotImplementedError

    def generate_transaction_payload(self, method, data):
        raise NotImplementedError

    def validate_data(self, data):
        raise NotImplementedError

    def get_address(self, method, swap_id, receiver_address):
        raise NotImplementedError

    def create_and_send_transaction(self, transaction_payload, inputs_outputs):
        raise NotImplementedError

    def check_parameters(self, parameters):
        raise NotImplementedError
