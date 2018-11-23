import aiohttp_json_rpc
from remme_client.remme.constants.remme_methods import RemmeMethods


class RemmeAPI:
    """
     Main class that send requests to our REMME protocol
     Check JSON-RPC API specification:
     https://remmeio.atlassian.net/wiki/spaces/WikiREMME/pages/292814862/RPC+API+specification.
     @param {string} node_address
     @param {string | int} node_port
     @param {boolean} ssl_mode

     @example
     ```python
        from remme.remme import Remme

        network_config = {
            'node_address': "localhost",
            'node_port': "8080",
            'ssl_mode': False
        }
     ```
        remme = Remme(network_config=network_config)
        result = await remme._api.send_request(RemmeMethods.SOME_REMME_METHOD)
        print(f"result {result}")
    """

    _node_address = None
    _ssl_mode = None
    _rpc_client = None
    _request_URI = None

    def __init__(self, network_config):
        """
        :param network_config: {dict}
        """
        self._node_address = network_config['node_address'] + ":" + network_config['node_port']
        self._ssl_mode = network_config['ssl_mode']
        # self._request_URI = "https://" if self._ssl_mode else "http://" + self._node_address
        self._request_URI = "https://node-genesis-testnet.remme.io:433"
        # self._request_URI = "https://node-genesis-testnet.remme.io:433"
        # self._request_URI = "https://node-1-testnet.remme.io:433"
        self._rpc_client = aiohttp_json_rpc.JsonRpcClient()

    async def send_request(self, method, params=None):
        """
        Make and send request with given method and payload.
        Create url from given network config
        Get JSON-RPC method and create request config in correspond to this spec https://www.jsonrpc.org/specification.
        :param method: {RemmeMethods}
        :param params: {dict}
        :return: {Promise}
        """
        if not isinstance(method, RemmeMethods):
            raise Exception("Invalid RPC method given.")
        try:
            await self._rpc_client.connect_url(url=self._request_URI)
        except Exception:
            raise Exception("Please check if your node running at {url}".format(url=self._request_URI))
        request_data = {'method': method.value}
        if params:
            request_data['params'] = params
        try:
            return await self._rpc_client.call(**request_data)
        finally:
            await self._rpc_client.disconnect()

    @property
    def node_address(self):
        """
        Get node address that was provided by user
        :return: {string}
        """
        return self._node_address

    @property
    def ssl_mode(self):
        """
        Get ssl mode that was provided by user
        :return: {string}
        """
        return self._ssl_mode
