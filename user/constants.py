from project.constants import *

CREDIT_TYPE_PLUS = 0
CREDIT_TYPE_MINUS = 1
CREDIT_TYPE_CHOICE = Choices(
    (CREDIT_TYPE_PLUS, '增加积分'),
    (CREDIT_TYPE_MINUS, '消耗积分')
)

CERT_STATUS_WAITING = 0
CERT_STATUS_SUCCESS = 1
CERT_STATUS_FAILED = 2
CERT_STATUS_CHOICE = Choices(
    (CERT_STATUS_WAITING, '待审核'),
    (CERT_STATUS_SUCCESS, '审核成功'),
    (CERT_STATUS_FAILED, '审核失败')
)

USER_CERT_SOURCE_TYPE_NONE = 0
USER_CERT_SOURCE_TYPE_SCAN = 1
USER_CERT_SOURCE_TYPE_CHOICE = Choices(
    (USER_CERT_SOURCE_TYPE_NONE, '普通'),
    (USER_CERT_SOURCE_TYPE_SCAN, '扫码活动')
)

IC_CARD_TYPE_UNKNOWN = 0
IC_CARD_TYPE_PERSON = 1
IC_CARD_TYPE_COMPANY = 2
IC_CARD_TYPE_CHOICE = Choices(
    (IC_CARD_TYPE_UNKNOWN, '未知'),
    (IC_CARD_TYPE_PERSON, '个人卡'),
    (IC_CARD_TYPE_COMPANY, '单位卡')
)

# 订单状态
ORDER_STATUS_WAITING_PAY = 0
ORDER_STATUS_SUCCESS_PAY = 1
ORDER_STATUS_CANCEL = 2
ORDER_STATUS_CHOICE = Choices(
    (ORDER_STATUS_WAITING_PAY, '待支付'),
    (ORDER_STATUS_SUCCESS_PAY, '已支付'),
    (ORDER_STATUS_CANCEL, '已取消')
)

# 订单类型
ORDER_TYPE_HAIR_CHANGE = 0
ORDER_TYPE_CHOICE = Choices(
    (ORDER_TYPE_HAIR_CHANGE, '变更发型')
)


# #####################################
# API接口错误表
# #####################################
class ErrorCode:
    ERROR_ACCOUNT_UNREGISTERED = 100001  # 账号未注册
    ERROR_ACCOUNT_REGISTERED = 100002  # 账号已注册
    ERROR_ACCOUNT_MOBILE_ERROR = 100003  # 手机号码错误
    ERROR_ACCOUNT_PASSWORD_ERROR = 100004  # 密码错误
    ERROR_ACCOUNT_BANNED = 100005  # 账号被禁用
    ERROR_ACCOUNT_DELETED = 100006  # 账号已删除
    ERROR_ACCOUNT_DEVICE_CHANGE = 100007  # 非常用设备登录
    ERROR_ACCOUNT_BLACK_LIST = 100008  # 账号在黑名单中
    ERROR_ACCOUNT_DEVICE_BLACK_LIST = 100009  # 设备在黑名单中
    ERROR_USER_PHONE = 2009

    # 小程序相关的错误
    ERROR_WXA_CODE_ERROR = 100301  # 无效的登陆code

    # Token相关的错误
    ERROR_TOKEN_ERROR = 100800  # Token错误未知
    ERROR_TOKEN_EXPIRED = 100801  # Token过期
    ERROR_TOKEN_TAMPERED = 100803  # Token被篡改
    ERROR_TOKEN_NOT_FOUND_ACCOUNT = 100804  # Token未查询到店铺
    ERROR_TOKEN_EMPTY = 100805  # Token未设置
    # 短信相关的错误
    ERROR_SMS_SEND_ERROR = 100900  # 短信发送错误
    ERROR_SMS_EXCEED_LIMIT = 100901  # 短信次数超过限制
    ERROR_SMS_CODE_ERROR = 100902  # 验证码错误
    ERROR_WX_TEMPLATE_ERROR = 100903  # 微信模板消息发送错误


ERROR_TABLE = Choices(
    (ErrorCode.ERROR_ACCOUNT_UNREGISTERED, '账号未注册'),
    (ErrorCode.ERROR_ACCOUNT_REGISTERED, '账号已注册'),
    (ErrorCode.ERROR_ACCOUNT_MOBILE_ERROR, '手机号码错误'),
    (ErrorCode.ERROR_ACCOUNT_PASSWORD_ERROR, '密码错误'),
    (ErrorCode.ERROR_ACCOUNT_BANNED, '账号被禁用'),
    (ErrorCode.ERROR_ACCOUNT_DELETED, '账号已删除'),
    (ErrorCode.ERROR_ACCOUNT_DEVICE_CHANGE, '非常用设备登录'),
    (ErrorCode.ERROR_ACCOUNT_DELETED, '账号已删除'),
    (ErrorCode.ERROR_ACCOUNT_BLACK_LIST, '账号在黑名单中'),
    (ErrorCode.ERROR_ACCOUNT_DEVICE_BLACK_LIST, '设备在黑名单中'),
    # 小程序相关的错误
    (ErrorCode.ERROR_WXA_CODE_ERROR, '无效的登陆code'),
    # Token相关的错误
    (ErrorCode.ERROR_TOKEN_ERROR, 'Token错误未知'),
    (ErrorCode.ERROR_TOKEN_EXPIRED, 'Token过期'),
    (ErrorCode.ERROR_TOKEN_TAMPERED, 'Token被篡改'),
    (ErrorCode.ERROR_TOKEN_NOT_FOUND_ACCOUNT, 'Token未查询到店铺'),
    (ErrorCode.ERROR_TOKEN_EMPTY, 'Token未设置'),
    # 短信相关的错误
    (ErrorCode.ERROR_SMS_SEND_ERROR, '短信发送错误'),
    (ErrorCode.ERROR_SMS_EXCEED_LIMIT, '短信次数超过限制'),
    (ErrorCode.ERROR_SMS_CODE_ERROR, '验证码错误'),
    (ErrorCode.ERROR_WX_TEMPLATE_ERROR, '微信模板消息发送错误'),
)

COLLECT_TYPE_CANCEL = 0
COLLECT_TYPE_SHOP = 1
COLLECT_TYPE_BARBER = 2
COLLECT_TYPE_EXAMPLE = 3
COLLECT_TYPE_TABLE = Choices(
    (COLLECT_TYPE_CANCEL, '未收藏'),
    (COLLECT_TYPE_SHOP, '收藏店铺'),
    (COLLECT_TYPE_BARBER, '收藏理发师'),
    (COLLECT_TYPE_EXAMPLE, '收藏作品')
)
