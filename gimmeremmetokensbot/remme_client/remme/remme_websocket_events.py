
class RemmeWebSocketEvents:

    _socket_address = None
    _ssl_mode = None

    def __init__(self, socket_address, ssl_mode):
        self._socket_address = socket_address
        self._ssl_mode = ssl_mode

    def subscribe(self, data, callback):
        raise NotImplementedError

    def unsubscribe(self):
        raise NotImplementedError
