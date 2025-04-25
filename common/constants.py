# -*- coding: utf-8 -*-
from model_utils.choices import Choices

# API接口通用错误
API_MESSAGE_OK = 0
API_MESSAGE_FORBIDDEN = 403
API_MESSAGE_PARAM_ERROR = 400
API_MESSAGE_NOT_FOUND = 404
API_MESSAGE_SERVER_ERROR = 500

API_MESSAGE_TABLE = Choices(
    (API_MESSAGE_OK, 'OK'),
    (API_MESSAGE_FORBIDDEN, '权限不足'),
    (API_MESSAGE_PARAM_ERROR, '参数错误'),
    (API_MESSAGE_NOT_FOUND, '资源未找到'),
    (API_MESSAGE_SERVER_ERROR, '服务端异常,请稍后再试'),
)

# 全局常量定义
STATUS_BIND = 0  # 禁用
STATUS_NORMAL = 1  # 正常

STATUS_CHOICE = Choices(
    (STATUS_NORMAL, '启用'),
    (STATUS_BIND, '禁用'),
)

# bool类型统一定义，0：false，1：true
BOOL_TYPE_FALSE = 0
BOOL_TYPE_TRUE = 1

BOOL_TYPE_CHOICE = Choices(
    (BOOL_TYPE_FALSE, '否'),
    (BOOL_TYPE_TRUE, '是')
)

USER_GENDER_MALE = 0
USER_GENDER_FEMALE = 1
USER_GENDER_UNKNOWN = 2

USER_GENDER_CHOICE = Choices(
    (USER_GENDER_MALE, '男'),
    (USER_GENDER_FEMALE, '女'),
    (USER_GENDER_UNKNOWN, '保密'),
)


# #####################################
# API接口错误表
# #####################################
class ErrorCode:
    # Token相关的错误
    ERROR_TOKEN_ERROR = 100800  # Token错误未知
    ERROR_TOKEN_EXPIRED = 100801  # Token过期
    ERROR_TOKEN_TAMPERED = 100803  # Token被篡改
    ERROR_TOKEN_NOT_FOUND_ACCOUNT = 100804  # Token未查询到店铺
    ERROR_TOKEN_EMPTY = 100805  # Token未设置


ERROR_TABLE = Choices(
    # 系统错误
    (API_MESSAGE_PARAM_ERROR, '400请求错误'),
    (API_MESSAGE_NOT_FOUND, '资源未找到'),
    (API_MESSAGE_SERVER_ERROR, '服务器出错'),
    # Token相关的错误
    (ErrorCode.ERROR_TOKEN_EXPIRED, 'Token过期'),
    (ErrorCode.ERROR_TOKEN_TAMPERED, 'Token被篡改'),
    (ErrorCode.ERROR_TOKEN_NOT_FOUND_ACCOUNT, 'Token未查询到店铺'),
    (ErrorCode.ERROR_TOKEN_EMPTY, 'Token未设置'),
)
