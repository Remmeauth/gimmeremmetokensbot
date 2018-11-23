
class BatchInfoDto:
    """
    Wrapper class for response on batch info response,
    which contain identifier of batch, batch status and list of invalid transaction if exists.
    """

    batch_id = None
    status = None
    invalid_transactions = None

    def __init__(self, batch_id, status, invalid_transactions):
        """
        Get information about batch
        :param batch_id: {string}
        :param status: {string}
        :param invalid_transactions: {list}
        """
        self.batch_id = batch_id
        self.status = status
        self.invalid_transactions = invalid_transactions
