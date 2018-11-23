import math

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
from remme_client.remme.models.certificate_transaction_response import CertificateTransactionResponse


class RemmeCertificate:
    """
    Class for working with certificates, such as create, store, revoke, check, getInfo.
    @example
    ```python
    remme = Remme()
    certificate_transaction_result = await remme.certificate.create_and_store({
        common_name: "username",
        email: "user@email.com",
        name: "John",
        surname: "Smith",
        country_name: "US",
        validity: 360,
        serial: `${Date.now()}`
    })

    async for response in certificate_transaction_result.connect_to_web_socket():
        print("store", response)
        if response.status === "COMMITTED":
            certificate_transaction_result.close_web_socket()
            status = await remme.certificate.check(certificate_transaction_result.certificate)
            print('status:', status) # True
            info = await remme.certificate.get_info(certificate_transaction_result.certificate)
            print("info:", info)
            revoke = await remme.certificate.revoke(certificate_transaction_result.certificate)
            async for res in revoke.connect_to_web_socket():
                print("revoke", response)
                if res.status === "COMMITTED":
                    revoke.close_web_socket()
                    status = await remme.certificate.check(certificate_transaction_result.certificate)
                    print(status) # False
    ```
    """

    _rsa_key_size = 2048
    remme_public_key_storage = None

    def __init__(self, remme_public_key_storage):
        """
        Usage without remme main package
        ```python
        api = RemmeApi()
        account = RemmeAccount()
        transaction = RemmeTransactionService(api, account)
        public_key_storage = RemmePublicKeyStorage(api, account, transaction)
        certificate = RemmeCertificate(public_key_storage)
        ```
        :param remme_public_key_storage: {IRemmePublicKeyStorage}
        """
        self.remme_public_key_storage = remme_public_key_storage

    def _create_subject(self, data):
        """
        :param data: {CreateCertificateDto}
        :return: object {x509.Name}
        """
        if not data.common_name:
            raise Exception("Attribute common_name must have a value")
        serial = data.serial if isinstance(data.serial, str) else str(data.serial)
        prepared_data = [
            x509.NameAttribute(NameOID.COMMON_NAME, data.common_name),
            x509.NameAttribute(NameOID.EMAIL_ADDRESS, data.email),
            # x509.NameAttribute(NameOID.LOCALITY_NAME, data.locality_name),
            # x509.NameAttribute(NameOID.POSTAL_ADDRESS, data.postal_address),
            # x509.NameAttribute(NameOID.POSTAL_CODE, data.postal_code),
            # x509.NameAttribute(NameOID.STREET_ADDRESS, data.street_address),
            x509.NameAttribute(NameOID.COUNTRY_NAME, data.country_name),
            # x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, data.state_name),
            x509.NameAttribute(NameOID.GIVEN_NAME, data.name),
            x509.NameAttribute(NameOID.SURNAME, data.surname),
            # x509.NameAttribute(NameOID.PSEUDONYM, data.pseudonym),
            # x509.NameAttribute(NameOID.GENERATION_QUALIFIER, data.generation_qualifier),
            # x509.NameAttribute(NameOID.TITLE, data.title),
            x509.NameAttribute(NameOID.SERIAL_NUMBER, serial),
            # x509.NameAttribute(NameOID.BUSINESS_CATEGORY, data.business_category)
        ]
        return x509.Name(prepared_data)

    def _prepare_serial(self, serial):
        serial = serial or x509.random_serial_number()
        serial = serial if isinstance(serial, int) else int(serial)
        return serial

    def _create_certificate(self, private_key, create_certificate_dto):
        """
        :param private_key:
        :param create_certificate_dto:
        :return:
        """
        if not create_certificate_dto.validity:
            raise Exception("Attribute validity must have a value")
        subject = self._create_subject(create_certificate_dto)
        not_before = datetime.utcnow() + timedelta(days=create_certificate_dto.valid_after) \
            if create_certificate_dto.valid_after else datetime.utcnow()

        cert = x509.CertificateBuilder()\
            .subject_name(subject)\
            .issuer_name(subject)\
            .public_key(private_key.public_key())\
            .serial_number(self._prepare_serial(create_certificate_dto.serial))\
            .not_valid_before(not_before)\
            .not_valid_after(not_before + timedelta(days=create_certificate_dto.validity))\
            .sign(private_key, hashes.SHA256(), default_backend())
        return cert

    def create(self, create_certificate_dto):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=self._rsa_key_size,
                                               backend=default_backend())
        return private_key, self._create_certificate(private_key, create_certificate_dto)

    def _certificate_from_pem(self, certificate):
        return x509.load_pem_x509_certificate(certificate, default_backend())

    def _certificate_to_pem(self, certificate):
        return certificate.public_bytes(encoding=serialization.Encoding.PEM)

    async def store(self, certificate, private_key):
        """
        :param certificate:
        :return:
        """
        if isinstance(certificate, str):
            certificate = self._certificate_from_pem(certificate)
        certificate_pem = self._certificate_to_pem(certificate)
        public_key = certificate.public_key()
        # private_key = certificate.private_key()
        # if not private_key:
        #     raise Exception("Your certificate does not have private key")
        valid_from = math.floor(int(certificate.not_valid_before.strftime("%s")) / 1000)
        valid_to = math.floor(int(certificate.not_valid_after.strftime("%s")) / 1000)
        return await self.remme_public_key_storage.store(data=certificate_pem, public_key=public_key,
                                                         private_key=private_key, valid_from=valid_from,
                                                         valid_to=valid_to)

    async def create_and_store(self, create_certificate_dto):
        private_key, certificate = self.create(create_certificate_dto)
        batch_response = await self.store(certificate, private_key)
        cert_response = CertificateTransactionResponse(
            node_address=batch_response.node_address,
            ssl_mode=batch_response.ssl_mode,
            batch_id=batch_response.batch_id
        )
        cert_response.certificate = certificate
        return cert_response

    def check(self, certificate):
        raise NotImplementedError

    def get_info(self):
        raise NotImplementedError

    def revoke(self, certificate):
        raise NotImplementedError

    def sign(self):
        raise NotImplementedError

    def verify(self):
        raise NotImplementedError
