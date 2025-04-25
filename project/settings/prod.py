from .base import *

# 生产环境配置文件
DEPLOY = 'PROD'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4'
        },
        'TEST': {
            'NAME': 'yijian-local-test',
        }
    }
}

ALLOWED_HOSTS = [
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
    '121.37.219.111',  # 测试
    'admin-api.yijian.taixun.tech',  # 正式
    '124.71.27.16',  # 正式
    'admin.yijian.taixun.tech',
    '192.168.1.110',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')  # local

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  # local

# Application definition
DJANGO_APPS = [
    'corsheaders',
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    'rest_framework',
    'requests',
    'django_filters',
    'debug_toolbar',
]

LOCAL_APPS = [
    'base',
    'system',
    'boss',
    'order',
    'shop',
    'barber',
    'activity',
    'help',
    'user',
    'task',
    'coupon',
    'article',
    'member',
    'sample'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS

# ==============================================================================
#                                  日志配置
# ==============================================================================

# logging 模块
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
        }
        # 日志格式
    },
    'filters': {
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

# 店铺采集任务数据表
SHOP_COLLECT_DATA_TABLE = "yj_tmp_shop"


# ==============================================================================
#                                  Celery配置
# ==============================================================================
BROKER_URL = 'redis://127.0.0.1:6379/11'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/12'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False
UTC_ENABLE = False

CELERYD_MAX_TASKS_PER_CHILD = 200
CELERYD_TASK_LOG_LEVEL = 'INFO'
CELERY_DEFAULT_EXCHANGE = 'default'

# ==============================================================================
#                                  小程序配置
# ==============================================================================
# 商户端微信小程序配置
WECHAT_MINIAPP_APPID = ''
WECHAT_MINIAPP_APPSECRET = ''
# 订阅消息配置
WECHAT_MINIAPP_APPROVE_DISABLED_TEMPLATE = ''  # 审核失败模板ID
WECHAT_MINIAPP_APPROVE_ENABLED_TEMPLATE = ''  # 审核通过模板ID


# ==============================================================================
#                                  腾讯云文件上传配置
# ==============================================================================
QCLOUD_STORAGE_OPTION = {
    'SecretId': '',
    'SecretKey': '',
    'Region': '',
    'Bucket': '',
}
COS_URL = None  # 'https://www.shuyungroup.com'  # 自定义域名， 不配置将使用 COS 默认域名
COS_FAST_CDN = False  # 默认加速域名是否开启
COS_BUCKET_URL = 'http://file.yijian.taixun.tech'
COS_STATIC_BASE_PATH = 'applet/static'


# ==============================================================================
#                                  正式环境公众号
# ==============================================================================
WECHAT_MP_APPID = ''
WECHAT_MP_APP_SECRET = ''


# ==============================================================================
#                                  微信支付配置
# ==============================================================================
WECHAT_PAY_MCH_ID = ''
WECHAT_PAY_MCH_KEY = ''
WECHAT_PAY_MCH_CERT = ''
WECHAT_PAY_MCH_CERT_KEY = ''

# ==============================================================================
#                                  赛邮云短信配置
# ==============================================================================
SUB_MAIL_APP_ID = ''  # SUBMAIL控制台创建appid
SUB_MAIL_APP_KEY = ''  # SUBMAIL控制台获取appkey
SUB_MAIL_TEMPLATE_ID = ''  # 短信模板id
SUB_MAIL_SIGN_TYPE = ''  # 验证类型
SUB_MAIL_SIGN_VERSION = ''  # 签名计算方式
SUB_MAIL_URL = 'https://api.mysubmail.com/message/multixsend.json'  # 批量发送短信URL