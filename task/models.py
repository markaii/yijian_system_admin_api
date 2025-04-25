from uuid import uuid4

from django.db import models
from model_utils.models import TimeStampedModel

from task import constants as c


class ShopCollectTask(TimeStampedModel):
    """
    店铺采集任务模型
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='任务名称', max_length=100, blank=True)
    cookie = models.TextField(verbose_name='cookie', blank=True)
    # 省市区
    province = models.CharField(verbose_name='省份', max_length=64, blank=True)
    province_code = models.CharField(verbose_name='省份代号', max_length=32, blank=True)
    city = models.CharField(verbose_name='城市', max_length=64, blank=True)
    city_code = models.CharField(verbose_name='城市代号', max_length=32, blank=True)
    district = models.CharField(verbose_name='地区', max_length=128, blank=True)
    district_code = models.CharField(verbose_name='地区代号', max_length=32, blank=True)
    # 初始URL
    initial_url = models.CharField(verbose_name='初始URL', max_length=255, blank=True, help_text="采集任务的初始URL")
    status = models.IntegerField(verbose_name='状态', default=c.SHOP_COLLECT_STATUS_NOT,
                                 choices=c.SHOP_COLLECT_STATUS_CHOICE)

    class Meta:
        db_table = 'yj_shop_collect_task'
        verbose_name = '店铺采集任务模型'
        verbose_name_plural = verbose_name


class ShopCollectLog(TimeStampedModel):
    """
    店铺采集记录模型
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='店铺名称', max_length=100)
    phone = models.CharField(verbose_name='手机号', max_length=64, unique=True)
    # 关联采集任务
    task_id = models.CharField(verbose_name='任务id', max_length=50, blank=True)
    task_name = models.CharField(verbose_name='任务名称', max_length=100, blank=True)
    # 省市区
    province = models.CharField(verbose_name='省份', max_length=64, blank=True)
    province_code = models.CharField(verbose_name='省份代号', max_length=32, blank=True)
    city = models.CharField(verbose_name='城市', max_length=64, blank=True)
    city_code = models.CharField(verbose_name='城市代号', max_length=32, blank=True)
    district = models.CharField(verbose_name='地区', max_length=128, blank=True)
    district_code = models.CharField(verbose_name='地区代号', max_length=32, blank=True)
    address = models.CharField(verbose_name='详细地址', help_text='详细地址', max_length=255, blank=True)

    sms_status = models.IntegerField(verbose_name='短信发送状态', default=c.SMS_STATUS_NOT,
                                     choices=c.SMS_STATUS_CHOICES)

    class Meta:
        db_table = 'yj_shop_collect_log'
        verbose_name = '店铺采集记录'
        verbose_name_plural = verbose_name
