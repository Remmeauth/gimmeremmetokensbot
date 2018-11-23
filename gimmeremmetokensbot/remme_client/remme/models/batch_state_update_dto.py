
class BatchStateUpdateDto:
    """
    Wrapper class for response on batch state update response,
    which contain identifier of batch, batch status, batch type and data.
    """

    id = None
    type = None
    data = None
    status = None

    def __init__(self, id, type, data=None, status=None):
        """
        Get information about batch state update
        :param id: {string}
        :param type: {string}
        :param data: {object}
        :param status: {string}
        """
        self.id = id
        self.type = type
        self.data = data
        self.status = status