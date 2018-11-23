from remme_client.remme.remme_utils import generate_address
from remme_client.remme.constants.remme_family_name import RemmeFamilyName
from remme_client.remme.constants.remme_methods import RemmeMethods
from remme_client.remme.protos.account_pb2 import AccountMethod, TransferPayload
from remme_client.remme.protos.transaction_pb2 import TransactionPayload


class RemmeToken:

    api = None
    transaction_service = None
    _family_version = "0.1"

    def __init__(self, rest, transaction_service):
        self.api = rest
        self.transaction_service = transaction_service

    def validate_amount(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount")
        return amount

    async def _create_transfer_tx(self, public_key_to, amount):
        public_key_to = self.validate_public_key(public_key_to)
        amount = self.validate_amount(amount)
        receiver_address = generate_address(RemmeFamilyName.ACCOUNT.value, public_key_to)
        # print(f"receiver address: {receiver_address}")

        transfer = TransferPayload()
        transfer.address_to = receiver_address
        transfer.value = amount

        # print(f"transfer address : {transfer.address_to} ; transfer value : {transfer.value}")
        # print(f"transfer serialized : {transfer.SerializeToString()}")

        tr = TransactionPayload()
        tr.method = AccountMethod.TRANSFER
        tr.data = transfer.SerializeToString()

        # print(f"transaction method : {tr.method} ; transaction data : {tr.data}")
        # print(f"transaction serialized : {tr.SerializeToString()}")

        return await self.transaction_service.create(family_name=RemmeFamilyName.ACCOUNT.value,
                                                family_version=self._family_version,
                                                inputs=[receiver_address],
                                                outputs=[receiver_address],
                                                payload_bytes=tr.SerializeToString())

    async def transfer(self, public_key_to, amount):
        payload = await self._create_transfer_tx(public_key_to, amount)
        return await self.transaction_service.send(payload)

    @staticmethod
    def validate_public_key(key):
        if len(key) != 66:
            raise Exception("Invalid key")
        return key

    async def get_balance(self, public_key):
        params = {"public_key": self.validate_public_key(public_key)}
        result = await self.api.send_request(RemmeMethods.TOKEN, params)
        # print(f'get_balance result: {result}')
        return result
