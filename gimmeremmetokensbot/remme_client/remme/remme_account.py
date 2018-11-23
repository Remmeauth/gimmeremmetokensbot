from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_signing import create_context, CryptoFactory
from remme_client.remme.remme_utils import generate_address, is_string_or_bytes, utf8_to_bytes
from remme_client.remme.constants.remme_patterns import RemmePatterns
from remme_client.remme.constants.remme_family_name import RemmeFamilyName
import re


class RemmeAccount:
    """
    Account that is used for signing transactions and storing public keys which he was signed.
    @example
    ```python
    remme = Remme(private_key_hex="ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9")
    print(remme._account.private_key_hex)  # "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"

    another_remme = Remme()
    print(another_remme._account.private_key_hex)  # "b5167700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d10783919129f"

    data = "transaction data"
    signed_data = remme._account.sign(data)

    is_verify = remme._account.verify(signed_data, data)
    print(is_verify)  # True

    is_verify_in_another_account = another_remme._account.verify(signed_data, data)
    print(is_verify_in_another_account)  # False
    ```
    """

    _context = None
    _family_name = None
    _signer = None
    _private_key_hex = None
    _private_key = None
    _public_key_hex = None
    _public_key = None
    _address = None

    def __init__(self, private_key_hex):
        """
        Get or generate private key, create signer by using private key,
        generate public key from private key and generate account address by using public key and family name
        (https://docs.remme.io/remme-core/docs/family-account.html#addressing)
        @example
        Get private key
        ```python
        account = RemmeAccount("ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9")
        print(account.private_key_hex) // "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"
        ```

        Generate new private key
        ```python
        account = RemmeAccount()
        print(account.private_key_hex) // "b5167700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d10783919129f"
        ```
        :param private_key_hex: {string}
        """
        self._family_name = RemmeFamilyName.ACCOUNT.value
        if private_key_hex and re.match(RemmePatterns.PRIVATE_KEY.value, private_key_hex) is None:
            raise Exception("Invalid private key given!")
        self._context = create_context("secp256k1")
        if not private_key_hex:
            self._private_key = self._context.new_random_private_key()
        else:
            self._private_key = Secp256k1PrivateKey.from_hex(private_key_hex)

        self._signer = CryptoFactory(self._context).new_signer(self._private_key)
        self._private_key_hex = self._private_key.as_hex()
        self._private_key = Secp256k1PrivateKey.from_hex(self._private_key_hex)
        self._public_key = self._signer.get_public_key()
        self._public_key_hex = self._public_key.as_hex()
        self._address = generate_address(self._family_name, self._public_key_hex)

    def sign(self, transaction):
        """
        Get transaction and sign it by signer
        @example
        ```python
        data = "transaction data"
        signed_data = account.sign(data)
        print(signedData)
        ```
        :param transaction: {string | bytes}
        :return: {hex_encoded_string}
        """
        if isinstance(transaction, str):
            transaction = utf8_to_bytes(transaction)
        return self._signer.sign(transaction)

    def verify(self, signature, transaction):
        """
        Verify given signature to given transaction
        @example
        ```python
        data = "transaction data"
        signed_data = account.sign(data)

        is_verify = account.verify(signed_data, data)
        print(is_verify) # True

        is_verify_in_another_account = another_account.verify(signed_data, data)
        print(is_verify_in_another_account) # False
        ```
        :param signature: {string | bytes}
        :param transaction: {string | bytes}
        :return: {boolean}
        """
        if not is_string_or_bytes(signature) or not is_string_or_bytes(transaction):
            raise Exception("Invalid parameters given. Expected string or bytes")
        if isinstance(transaction, str):
            transaction = utf8_to_bytes(transaction)
        return self._context.verify(signature, transaction, self._public_key)

    @property
    def family_name(self):
        """
        Family name for generate address for this account in the blockchain.
        (https://docs.remme.io/remme-core/docs/family-account.html)
        :return: {string}
        """
        return self._family_name

    @property
    def address(self):
        """
        Address of this account in blockchain.
        (https://docs.remme.io/remme-core/docs/family-account.html#addressing)
        :return: {string}
        """
        return self._address

    @property
    def public_key(self):
        """
        Get public key that that was generated from public key hex
        :return: {sawtooth_signing.secp256k1.Secp256k1PublicKey}
        """
        return self._public_key

    @property
    def public_key_hex(self):
        """
        Get public key hex that was generated automatically or given by user
        :return: {string}
        """
        return self._public_key_hex

    @property
    def private_key(self):
        """
        Get private key that was generated from user's public key
        :return: {sawtooth_signing.secp256k1.Secp256k1PrivateKey}
        """
        return self._private_key

    @property
    def private_key_hex(self):
        """
        Get private key hex that was generated from user's private key
        :return: {string}
        """
        return self._private_key_hex
