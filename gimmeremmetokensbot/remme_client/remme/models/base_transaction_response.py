from remme_client.remme.remme_utils import is_valid_batch_id
from remme_client.remme.remme_websocket import RemmeWebSocket


class BaseTransactionResponse(RemmeWebSocket):
    """
    Wrapper class for response on transaction request,
    which contain identifier of batch and communication with WebSockets.
    """

    _batch_id = None
    """
    Identifier of batch that contain sending transaction
    """

    def __init__(self, node_address, ssl_mode, batch_id):
        """
        Get address of node, ssl mode, and identifier of batch.
        Then implement RemmeWebSocket class and provide data to it.
        :param node_address: {string}
        :param ssl_mode: {boolean}
        :param batch_id: {string}
        """
        super(BaseTransactionResponse, self).__init__(node_address, ssl_mode)
        self._batch_id = batch_id
        self.data = {
            "batch_ids": [
                self._batch_id
            ]
        }

    @property
    def batch_id(self):
        """
        Get identifier of batch that contain sending transaction
        :return: batch_id {string}
        """
        return self._batch_id

    @batch_id.setter
    def batch_id(self, value):
        """
        close old connection if exists to prevent listening message for old batch and set identified of batch
        :param value: {string}
        :return:
        """
        if not is_valid_batch_id(value):
            raise Exception("Invalid given batch id")
        if self._socket:
            self.close_web_socket()
        self._batch_id = value
        self.data = {
            "batch_ids": [
                self._batch_id
            ]
        }

    async def __aenter__(self):
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
