# TODO 活动奖励
import binascii
import os


def _generate_random_str(digital):
    """
    生成随机数
    :param digital: 数字位数
    :return:
    """
    return binascii.hexlify(os.urandom(digital)).decode()