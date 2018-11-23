from remme_client.remme.constants.pub_key_type import PubKeyType
from remme_client.remme.constants.entity_type import EntityType


class IPublicKeyStore:
    """
    Interface that take method store in publicKeyStorage
    """

    data = None
    public_key = None
    valid_from = None
    valid_to = None
    private_key = None
    public_key_type = None
    entity_type = None

    def __init__(self, data, public_key, valid_from, valid_to, private_key,
                 public_key_type=PubKeyType.RSA.value, entity_type=EntityType.PERSONAL.value):
        """
        :param data: {string}
        :param public_key: {Key | PEM}
        :param valid_from: {Key | PEM}
        :param valid_to: {integer}
        :param private_key: {integer}
        :param public_key_type: {NewPubKeyPayload.PubKeyType}
        :param entity_type: {NewPubKeyPayload.EntityType}
        """
        self.data = data
        self.public_key = public_key
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.private_key = private_key
        self.public_key_type = public_key_type
        self.entity_type = entity_type
