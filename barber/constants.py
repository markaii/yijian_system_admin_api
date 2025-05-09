from project.constants import *


BARBER_BUSINESS_STATUS_REST = 0
BARBER_BUSINESS_STATUS_SERVING = 1
BARBER_BUSINESS_STATUS_CHOICE = Choices(
    (BARBER_BUSINESS_STATUS_REST, '休息'),
    (BARBER_BUSINESS_STATUS_SERVING, '服务中'),
)

# 理发师从业年数枚举
BARBER_WORK_LITTLE = 0
BARBER_WORK_ONE = 1
BARBER_WORK_TWO = 2
BARBER_WORK_THREE = 3
BARBER_WORK_FORE = 4
BARBER_WORK_FIVE = 5
BARBER_WORK_SIX = 6
BARBER_WORK_SEVEN = 7
BARBER_WORK_EIGHT = 8
BARBER_WORK_NINE = 9
BARBER_WORK_TEN = 10
BARBER_WORK_GREATER = 11
BARBER_WORK_TABLE = Choices(
    (BARBER_WORK_LITTLE, '小于一年'),
    (BARBER_WORK_ONE, '一年'),
    (BARBER_WORK_TWO, '两年'),
    (BARBER_WORK_THREE, '三年'),
    (BARBER_WORK_FORE, '四年'),
    (BARBER_WORK_FIVE, '五年'),
    (BARBER_WORK_SIX, '六年'),
    (BARBER_WORK_SEVEN, '七年'),
    (BARBER_WORK_EIGHT, '八年'),
    (BARBER_WORK_NINE, '九年'),
    (BARBER_WORK_TEN, '十年'),
    (BARBER_WORK_GREATER, '大于十年')
)

EXAMPLE_GENDER_UNKNOWN = 0
EXAMPLE_GENDER_MALE = 1
EXAMPLE_GENDER_FEMALE = 2
EXAMPLE_GENDER_GENERAL = 3
EXAMPLE_GENDER_CHOICE = Choices(
    (EXAMPLE_GENDER_UNKNOWN, '未知'),
    (EXAMPLE_GENDER_MALE, '男'),
    (EXAMPLE_GENDER_FEMALE, '女'),
    (EXAMPLE_GENDER_GENERAL, '通用')
)

SERVICE_PRICE_SECRECY_NO = 0
SERVICE_PRICE_SECRECY_YES = 1
SERVICE_PRICE_SECRECY_TABLE = Choices(
    (SERVICE_PRICE_SECRECY_NO, '价格不保密'),
    (SERVICE_PRICE_SECRECY_YES, '价格保密')
)
