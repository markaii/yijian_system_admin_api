from uuid import uuid4

from model_utils.models import TimeStampedModel
from django.db import models
from system import constants as c


class SystemConfig(TimeStampedModel):
    """
    系统配置
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name="配置名称", max_length=100, blank=True)
    value = models.CharField(verbose_name="配置值", max_length=255, blank=True)
    value_type = models.IntegerField(verbose_name="值类型", default=c.SYSTEM_CONFIG_VALUE_TYPE_AMOUNT,
                                     choices=c.SYSTEM_CONFIG_VALUE_TYPE_CHOICES, help_text="默认类型金额")
    count = models.IntegerField(verbose_name="次数", default=0)
    sort = models.IntegerField(verbose_name='排序码', default=0, help_text='升序排序')

    class Meta:
        db_table = 'yj_system_config'
        verbose_name = "系统配置"
        verbose_name_plural = verbose_name


class SystemSample(TimeStampedModel):
    """
    系统样本
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    file = models.CharField(verbose_name='文件地址', max_length=255, blank=True)
    type = models.IntegerField(verbose_name='类型', choices=c.SAMPLE_TYPE_CHOICE, default=c.SAMPLE_TYPE_HAIR_STYLE)
    sort = models.IntegerField(verbose_name='排序码', default=0, help_text='升序排序')
    status = models.IntegerField(verbose_name='状态', default=c.STATUS_NORMAL, choices=c.STATUS_CHOICE)
    role_type = models.IntegerField(verbose_name='角色类型', choices=c.SAMPLE_ROLE_TYPE_CHOICE,
                                    default=c.SAMPLE_ROLE_TYPE_FEMALE)
    color = models.CharField(verbose_name='颜色', max_length=50, blank=True)

    class Meta:
        db_table = 'yj_system_sample'
        verbose_name = "系统样本"
        verbose_name_plural = verbose_name