from remme_client.remme.models.base_transaction_response import BaseTransactionResponse


class CertificateTransactionResponse(BaseTransactionResponse):

    _certificate = None

    def __init__(self, node_address, ssl_mode, batch_id, certificate=None):
        super(CertificateTransactionResponse, self).__init__(node_address=node_address, ssl_mode=ssl_mode,
                                                             batch_id=batch_id)
        self._certificate = certificate

    @property
    def certificate(self):
        return self._certificate

    @certificate.setter
    def certificate(self, value):
        # todo: check WS
        self._certificate = value
