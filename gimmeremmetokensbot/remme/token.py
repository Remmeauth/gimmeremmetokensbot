"""
Provide implementation of the Remme node tokens.

Code below is vendor code and located by address `https://github.com/Remmeauth/remme-client-python`.
"""
import os
import json
from base64 import b64encode

import requests

from remme.account import RemmeAccount
from remme.constants.amount import STABLE_REMME_TOKENS_REQUEST_AMOUNT
from remme.constants.family_name import RemmeFamilyName
from remme.protos.account_pb2 import AccountMethod, TransferPayload
from remme.protos.transaction_pb2 import TransactionPayload
from remme.utils import generate_address, create_nonce, sha512_hexdigest
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction


class RequestToNode:

    @staticmethod
    def send(method, params=None):
        if params is None:
            params = {}

        parameters = {
            'jsonrpc': '2.0',
            'id': '11',
            'method': method,
            'params': params,
        }

        return requests.post(
            'https://' + os.environ.get('NODE_HOST'),
            data=json.dumps(parameters),
            verify=False
        )


class TransactionService:

    def __init__(self, private_key_hex):
        self.request_to_node = RequestToNode()
        self._remme_account = RemmeAccount(private_key_hex)

    def create(self, family_name, family_version, inputs, outputs, payload_bytes):
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
        node_config = self.request_to_node.send(method='get_node_config')
        node_public_key = node_config.json().get('result').get('node_public_key')

        txn_header_bytes = TransactionHeader(
            family_name=family_name,
            family_version=family_version,
            inputs=inputs + [self._remme_account.address],
            outputs=outputs + [self._remme_account.address],
            signer_public_key=self._remme_account.public_key_hex,
            batcher_public_key=node_public_key,
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

    def __init__(self, private_key_hex=None):
        self.request_to_node = RequestToNode()
        self.transaction_service = TransactionService(private_key_hex=private_key_hex)

    @staticmethod
    def _validate_public_key(key):
        if len(key) != 66:
            raise Exception("Invalid key")
        return key

    def get_balance(self, address):

        balance_info = self.request_to_node.send(method='get_balance', params={
            'public_key_address': address,
        })

        return balance_info.json().get('result')

    def send_transaction(self, public_key_to, amount=STABLE_REMME_TOKENS_REQUEST_AMOUNT):
        """
        Send raw transaction to Remme node.
        """
        sent_transaction_info = self.request_to_node.send(method='send_raw_transaction', params={
            'data': self._create_transaction(public_key_to, amount),
        })

        batch_id = sent_transaction_info.json().get('result')

        return batch_id

    def _create_transaction(self, public_key_to, amount):
        """
        Create raw transaction based on address's public key send token to and amount.
        """
        public_key_to = self._validate_public_key(public_key_to)
        receiver_address = generate_address(RemmeFamilyName.ACCOUNT.value, public_key_to)

        transfer = TransferPayload()
        transfer.address_to = receiver_address
        transfer.value = amount

        tr = TransactionPayload()
        tr.method = AccountMethod.TRANSFER
        tr.data = transfer.SerializeToString()

        return self.transaction_service.create(
            family_name=RemmeFamilyName.ACCOUNT.value,
            family_version=self._family_version,
            inputs=[receiver_address],
            outputs=[receiver_address],
            payload_bytes=tr.SerializeToString(),
        )
