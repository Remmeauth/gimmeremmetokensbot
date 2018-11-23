import binascii
import re

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from remme_client.remme.constants.entity_type import EntityType
from remme_client.remme.constants.pub_key_type import PubKeyType
from remme_client.remme.constants.remme_family_name import RemmeFamilyName
from remme_client.remme.constants.remme_patterns import RemmePatterns
from remme_client.remme.protos.proto_buf_pb2 import NewPubKeyPayload, PubKeyMethod
from remme_client.remme.protos.transaction_pb2 import TransactionPayload
from remme_client.remme.remme_utils import generate_address, generate_settings_address, sha512_hexdigest


class RemmePublicKeyStorage:
    """
    Class for working with public key storage.
    @example
    ```python
    remme = Remme()
    # if you don't have private and public keys you can generate them
    from remme.remme_utils import generate_rsa_key_pair
    private_key, public_key = generate_rsa_key_pair();
    store_response = await remme.public_key_storage.store(
         data="store data",
         private_key=private_key, # need for signing data
         public_key=public_key,
         valid_from=valid_from,
         valid_to=valid_to
    )
    async for msg in store_response.connect_to_web_socket():
        print(msg)

        key_is_valid = await remme.public_key_storage.check(public_key)
        print(key_is_valid) # True

        public_key_info = await remme.public_key_storage.get_info(public_key)
        print(public_key_info) # public_key_info

        revoke = await remme.public_key_storage.revoke(public_key)
        # You can connect_to_web_socket like in store method.
        print(revoke.batch_id) # r"\^[a-f0-9]{128}$\"

        public_keys = await remme.public_key_storage.get_account_public_keys(remme.account.public_key_hex)
        print(public_keys) # []

        store_response.close_web_socket()
    ```
    """

    _remme_api = None
    _remme_transaction = None
    _remme_account = None
    _family_name = RemmeFamilyName.PUBLIC_KEY.value
    _family_version = "0.1"

    def __init__(self, remme_api, remme_account, remme_transaction):
        """
        @example
        Usage without remme main package
        ```python
        api = RemmeApi()
        account = RemmeAccount()
        transaction = RemmeTransactionService(api, account)
        public_key_storage = RemmePublicKeyStorage(rest, account, transaction)
        ```
        :param remme_api: RemmeApi
        :param remme_account: RemmeAccount
        :param remme_transaction: RemmeTransaction
        """
        self._remme_api = remme_api
        self._remme_transaction = remme_transaction
        self._remme_account = remme_account

    def _public_key_to_pem(self, public_key):
        return public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                       format=serialization.PublicFormat.SubjectPublicKeyInfo).strip(b"\n")

    def _private_key_from_pem(self, private_key):
        return serialization.load_pem_private_key(private_key, password=None, backend=default_backend())

    async def store(self, data, private_key, public_key, valid_from, valid_to,
                    public_key_type=PubKeyType.RSA.value, entity_type=EntityType.PERSONAL.value):
        """
        Store public key with its data into REMChain.
        Send transaction to chain.
        @example
        ```python
        public_key_storage_data = PublicKeyStore(
             data="store data",
             private_key=private_key, # need for signing data
             public_key=public_key,
             valid_from=valid_from,
             valid_to=valid_to
        )
        store_response = await remme.public_key_storage.store(public_key_storage_data)
        async for msg in store_response.connect_to_web_socket():
            print(msg)
            store_response.close_web_socket()
        ```
        :param data: {string}
        :param private_key: {rsa.RSAPrivateKey | PEM bytes}
        :param public_key: {rsa.RSAPublicKey | PEM bytes}
        :param valid_from: {integer}
        :param valid_to: {integer}
        :param public_key_type: {Enum value}
        :param entity_type: {Enum value}
        :return: {Promise}
        """
        private_key = private_key if isinstance(private_key, rsa.RSAPrivateKey) else self._private_key_from_pem(private_key)
        public_key = self._public_key_to_pem(public_key) if isinstance(public_key, rsa.RSAPublicKey) else public_key.strip(b"\n")
        message = self.generate_message(data)
        entity_hash = self.generate_entity_hash(message)
        entity_hash_signature = self._generate_signature(entity_hash, private_key)
        payload = NewPubKeyPayload(
            public_key=public_key,
            public_key_type=public_key_type,
            entity_type=entity_type,
            entity_hash=binascii.hexlify(entity_hash),
            entity_hash_signature=entity_hash_signature,
            valid_from=valid_from,
            valid_to=valid_to
        ).SerializeToString()
        pub_key_address = generate_address(self._family_name, public_key)
        storage_pub_key = generate_settings_address("remme.settings.storage_pub_key")
        setting_address = generate_settings_address("remme.economy_enabled")
        storage_address = generate_address(self._remme_account.family_name, storage_pub_key)
        payload_bytes = self._generate_transaction_payload(PubKeyMethod.STORE, payload)
        return await self._create_and_send_transaction([pub_key_address, storage_pub_key, setting_address,
                                                        storage_address], payload_bytes)

    def _check_public_key(self, public_key):
        try:
            if isinstance(public_key, bytes):
                if re.match(RemmePatterns.PUBLIC_KEY.value, public_key) is None:
                    # I was stopped here
                    pass
        except Exception:
            raise Exception("Given public key is not a valid")

    async def _get_info_by_public_key(self, public_key):
        self._check_public_key(public_key)
        if isinstance(public_key, rsa.RSAPublicKey):
            public_key = self._public_key_to_pem(public_key)
        raise NotImplementedError

    async def check(self, public_key):
        """
        Check public key on validity and revocation.
        Can take address of public key.
        @example
        ```python
        is_valid = await remme.public_key_storage.check(public_key)
        print(is_valid) # True or False
        ```
        :param public_key: {string | cryptography.hazmat.backends.openssl.rsa._RSAPrivateKey | PEM bytes} publicKey
        :return: {Promise<boolean>}
        """
        return await self._get_info_by_public_key(public_key)

    def revoke(self, public_key):
        raise NotImplementedError

    def get_user_public_key(self, user_account_public_key):
        raise NotImplementedError

    def generate_message(self, data):
        return sha512_hexdigest(data)

    def generate_entity_hash(self, message):
        return binascii.unhexlify(message)

    def _generate_signature(self, data, private_key):
        return binascii.hexlify(private_key.sign(data, padding.PKCS1v15(), hashes.SHA512()))

    def _generate_transaction_payload(self, method, data):
        return TransactionPayload(method=method, data=data).SerializeToString()

    async def _create_and_send_transaction(self, inputs_and_outputs, payload_bytes):
        transaction = await self._remme_transaction.create(family_name=self._family_name,
                                                           family_version=self._family_version,
                                                           inputs=inputs_and_outputs,
                                                           outputs=inputs_and_outputs,
                                                           payload_bytes=payload_bytes)
        return await self._remme_transaction.send(transaction)
