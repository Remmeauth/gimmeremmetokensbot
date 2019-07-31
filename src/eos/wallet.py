"""
Provide implementation of wallet.
"""
from eospy.keys import EOSKey


class Wallet:
    """
    Wallet implementation
    """

    def __init__(self):
        """
        Constructor.
        """
        eos_key = EOSKey()

        self._private_key = eos_key.to_wif()
        self._public_key = eos_key.to_public()

    @property
    def private_key(self):
        """
        Get wallet's private key.
        """
        return self._private_key

    @property
    def public_key(self):
        """
        Get wallet's public key.
        """
        return self._public_key
