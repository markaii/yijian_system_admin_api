from .base import *

# 测试环境配置文件
DEPLOY = 'DEV'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'm',
        'PORT': '10098',
        'OPTIONS': {
            'charset': 'utf8mb4'
        },
        'TEST': {
            'NAME': 'yijian-local-test',
        }
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')  # local

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  # local
# debug tool 安装位置
INTERNAL_IPS = ['127.0.0.1', ]

ALLOWED_HOSTS = [
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
    '121.37.219.111',  # 测试
    'admin-api.yijian.taixun.tech',  # 正式
    '124.71.27.16',  # 正式
]

# Application definition

DJANGO_APPS = [
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
    'corsheaders',
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
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS
