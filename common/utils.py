import binascii
import os
import uuid


def get_random_str(digital=6):
    return binascii.hexlify(os.urandom(digital)).decode()


class UUIDTools(object):
    """
    uuid utils tools
    """

    @staticmethod
    def uuid4():
        """
        return uuid4 hex string
        uuid4 hex string equal to uuid.uuid4.replace('-','')
        :return:
        """
        return uuid.uuid4()
