from project.constants import *

# 系统配置值类型
SYSTEM_CONFIG_VALUE_TYPE_AMOUNT = 0
SYSTEM_CONFIG_VALUE_TYPE_DISCOUNT_AMOUNT = 1
SYSTEM_CONFIG_VALUE_TYPE_VALIDITY = 2
SYSTEM_CONFIG_VALUE_TYPE_CHOICES = Choices(
    (SYSTEM_CONFIG_VALUE_TYPE_AMOUNT, '原价'),
    (SYSTEM_CONFIG_VALUE_TYPE_DISCOUNT_AMOUNT, '折扣价'),
    (SYSTEM_CONFIG_VALUE_TYPE_VALIDITY, '有效期')
)

# 过期类型
EXPIRE_TYPE_ONE_YEAR = 0
EXPIRE_TYPE_CHOICES = Choices(
    (EXPIRE_TYPE_ONE_YEAR, '一年')
)

SAMPLE_ROLE_TYPE_FEMALE = 0
SAMPLE_ROLE_TYPE_MALE = 1
SAMPLE_ROLE_TYPE_CHILD = 2
SAMPLE_ROLE_TYPE_UNKNOW = 3
SAMPLE_ROLE_TYPE_CHOICE = Choices(
    (SAMPLE_ROLE_TYPE_FEMALE, '女士'),
    (SAMPLE_ROLE_TYPE_MALE, '男士'),
    (SAMPLE_ROLE_TYPE_CHILD, '少儿'),
    (SAMPLE_ROLE_TYPE_UNKNOW, '未知')
)

SAMPLE_TYPE_HAIR_STYLE = 0
SAMPLE_TYPE_HAIR_COLOR = 1
SAMPLE_TYPE_CHOICE = Choices(
    (SAMPLE_TYPE_HAIR_STYLE, '发型'),
    (SAMPLE_TYPE_HAIR_COLOR, '发色')
)

# =============================================================================
# 微信 相关接口URL
# =============================================================================
WECHAT_BASE_URL = "https://api.weixin.qq.com/"
WECHAT_GEN_URL_SCHEME = "wxa/generatescheme?access_token={access_token}"  # 生成小程序scheme码