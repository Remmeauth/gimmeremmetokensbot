from remme.utils import generate_address
from remme.constants.family_name import RemmeFamilyName
from remme.protos.account_pb2 import AccountMethod, TransferPayload
from remme.protos.transaction_pb2 import TransactionPayload


from remme_client.remme.remme_utils import create_nonce, sha512_hexdigest
from base64 import b64encode
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction


from remme.account import RemmeAccount

class TransactionService:

    def __init__(self):
        self._remme_account = RemmeAccount(self._private_key_hex)

    async def create(self, family_name, family_version, inputs, outputs, payload_bytes):
        """
        Documentation for building transactions
        https://sawtooth.hyperledger.org/docs/core/releases/latest/_autogen/sdk_submit_tutorial_python.html#building-the-transaction
        @example
        ```python
        family_name = "pub_key"
        family_version = "0.1"
        inputs = []
        outputs = []
        payload_bytes = b"my transaction"
        transaction = await remme_transaction.create(family_name, family_version, inputs, outputs, payload_bytes)
        ```
        :param family_name: {string}
        :param family_version: {string}
        :param inputs: {list}
        :param outputs: {list}
        :param payload_bytes: {bytes}
        :return: {Couroutine}
        """
        # config = await self._remme_api.send_request(RemmeMethods.NODE_CONFIG)
        config = {
            "node_public_key": "03738df3f4ac3621ba8e89413d3ff4ad036c3a0a4dbb164b695885aab6aab614ad",
            "storage_public_key": "03738df3f4ac3621ba8e89413d3ff4ad036c3a0a4dbb164b695885aab6aab614ad"
        }

        txn_header_bytes = TransactionHeader(
            family_name=family_name,
            family_version=family_version,
            inputs=inputs + [self._remme_account.address],
            outputs=outputs + [self._remme_account.address],
            signer_public_key=self._remme_account.public_key_hex,
            # batcher_public_key=config.node_public_key,
            batcher_public_key=config.get('node_public_key'),
            nonce=create_nonce(),
            dependencies=[],
            payload_sha512=sha512_hexdigest(payload_bytes)
        ).SerializeToString()
        signature = self._remme_account.sign(txn_header_bytes)
        txn = Transaction(
            header=txn_header_bytes,
            header_signature=signature,
            payload=payload_bytes
        ).SerializeToString()
        return b64encode(txn).decode('utf-8')


class RemmeToken:

    _family_version = "0.1"

    def __init__(self, rest, transaction_service):
        self.api = rest
        self.transaction_service = transaction_service

    @staticmethod
    def validate_public_key(key):
        if len(key) != 66:
            raise Exception("Invalid key")
        return key

    def validate_amount(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount")
        return amount


    async def create_transaction(self, public_key_to, amount):
        public_key_to = self.validate_public_key(public_key_to)
        amount = self.validate_amount(amount)
        receiver_address = generate_address(RemmeFamilyName.ACCOUNT.value, public_key_to)

        transfer = TransferPayload()
        transfer.address_to = receiver_address
        transfer.value = amount

        tr = TransactionPayload()
        tr.method = AccountMethod.TRANSFER
        tr.data = transfer.SerializeToString()

        return await self.transaction_service.create(
            family_name=RemmeFamilyName.ACCOUNT.value,
            family_version=self._family_version,
            inputs=[receiver_address],
            outputs=[receiver_address],
            payload_bytes=tr.SerializeToString()
        )
