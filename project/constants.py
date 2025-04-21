# coding:utf-8
from model_utils.choices import Choices

STATUS_NORMAL = 0
STATUS_DISABLED = 1

STATUS_CHOICE = Choices(
    (STATUS_NORMAL, u'正常'),
    (STATUS_DISABLED, u'禁用'),
)

ACTIVITY_STATUS_WAITING = 0
ACTIVITY_STATUS_ENABLE = 1
ACTIVITY_STATUS_DISABLE = 2
ACTIVITY_STATUS_CHOICE = Choices(
    (ACTIVITY_STATUS_WAITING, '等待开始'),
    (ACTIVITY_STATUS_ENABLE, '有效，进行中'),
    (ACTIVITY_STATUS_DISABLE, '禁用，已过期')
)

USER_GENDER_UNKNOWN = 0
USER_GENDER_MALE = 1
USER_GENDER_FEMALE = 2

USER_GENDER_CHOICE = Choices(
    (USER_GENDER_UNKNOWN, '未知'),
    (USER_GENDER_MALE, '男'),
    (USER_GENDER_FEMALE, '女'),
)

# bool类型统一定义，0：false，1：true
BOOL_TYPE_FALSE = 0
BOOL_TYPE_TRUE = 1

BOOL_TYPE_CHOICE = Choices(
    (BOOL_TYPE_FALSE, '否'),
    (BOOL_TYPE_TRUE, '是')
)

# 文件类型
FILE_TYPE_IMG = 0
FILE_TYPE_VIDEO = 1
FILE_TYPE_CHOICE = Choices(
    (FILE_TYPE_IMG, '图片'),
    (FILE_TYPE_VIDEO, '视频')
)

# 价格类型
PRICE_TYPE_FIXED = 0
PRICE_TYPE_SECTION = 1
PRICE_TYPE_CHOICE = Choices(
    (PRICE_TYPE_FIXED, '固定价格'),
    (PRICE_TYPE_SECTION, '价格区间')
)

DELETE_TYPE_NORMAL = 0
DELETE_TYPE_DELETED = 1

DELETE_CHOICE = Choices(
    (DELETE_TYPE_NORMAL, 'normal', '正常'),
    (DELETE_TYPE_DELETED, 'deleted', '删除')
)

ENABLE_TYPE_NORMAL = 0
ENABLE_TYPE_ABNORMAL = 1

ENABLE_CHOICE = Choices(
    (ENABLE_TYPE_NORMAL, 'normal', '有效'),
    (ENABLE_TYPE_ABNORMAL, 'abnormal', '无效')
)

# 默认为空的父元素id
DEFAULT_BLANK_PARENT_ID = ''

# API message
API_MESSAGE_OK = 0
API_MESSAGE_PARAM_ERROR = u'400 参数错误请检查'
API_MESSAGE_NOT_FOUND = u'404 未找到'

# =================
# ERROR TABLE
# =================
ERROR_PASSWORD = u'1001密码错误'
ERROR_PHONE_ALREADY_REGISTERED = u'1002手机号已经注册'
ERROR_PHONE_UNREGISTERED = u'1003手机号未注册'
ERROR_ACCOUNT_PHONE_ERROR = u'1004账号或密码不正确'
ERROR_SMS_CODE_ERROR = u'1005验证码错误'

EMPTY_DEPARTMENT = u'该公司的部门为空'

CREDIT_TYPE_PLUS = 0
CREDIT_TYPE_MINUS = 1
CREDIT_TYPE_CHOICE = Choices(
    (CREDIT_TYPE_PLUS, '增加积分'),
    (CREDIT_TYPE_MINUS, '消耗积分')
)

ERROR_ARTICLE_CATEGORY_EXIST = 2001
ERROR_COUPON_NOT_EXIST = 2002
ERROR_XXL_CONFIG_EXIST = 2003
ERROR_WX_TEMPLATE_ERROR = 6004  # 微信模板消息发送错误

ERROR_CHOICE = Choices(
    (ERROR_ARTICLE_CATEGORY_EXIST, '文章分类不存在'),
    (ERROR_COUPON_NOT_EXIST, '优惠券不存在'),
    (ERROR_XXL_CONFIG_EXIST, '消消乐配置不存在'),
)


# -*- coding: utf-8 -*-


class ErrorCode:
    # Token相关的错误
    ERROR_TOKEN_ERROR = 100800  # Token错误未知
    ERROR_TOKEN_EXPIRED = 100801  # Token过期
    ERROR_TOKEN_TAMPERED = 100803  # Token被篡改
    ERROR_TOKEN_NOT_FOUND_ACCOUNT = 100804  # Token未查询到店铺
    ERROR_TOKEN_EMPTY = 100805  # Token未设置

    # 微信接口错误
    ERROR_WECHAT_API = 2101


ERROR_TABLE = Choices(
    # Token相关的错误
    (ErrorCode.ERROR_TOKEN_ERROR, 'Token错误未知'),
    (ErrorCode.ERROR_TOKEN_EXPIRED, 'Token过期'),
    (ErrorCode.ERROR_TOKEN_TAMPERED, 'Token被篡改'),
    (ErrorCode.ERROR_TOKEN_NOT_FOUND_ACCOUNT, 'Token未查询到店铺'),
    (ErrorCode.ERROR_TOKEN_EMPTY, 'Token未设置'),
    (ERROR_WX_TEMPLATE_ERROR, '微信模板消息发送错误'),

    (ErrorCode.ERROR_WECHAT_API, '调用微信接口失败')
)
