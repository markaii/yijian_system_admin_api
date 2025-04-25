import os
import logging
from celery import Celery

from django.conf import settings


# wechatpy 依赖requests。这里提高requests日志输出的级别
logging.getLogger("requests").setLevel(logging.WARNING)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('system_admin')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
