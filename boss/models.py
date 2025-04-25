from django.db import models
from uuid import uuid4
from model_utils.models import TimeStampedModel

from boss import constants as c


# Create your models here.
class Boss(TimeStampedModel):
    """
    商户老板端账号
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    phone = models.CharField(verbose_name='手机号', max_length=64, unique=True)
    name = models.CharField(verbose_name='用户名', max_length=128, blank=True)
    password = models.CharField(verbose_name='密码', max_length=50)
    salt = models.CharField(verbose_name='加密盐', max_length=50)

    gender = models.IntegerField(verbose_name='性别', default=c.USER_GENDER_UNKNOWN, choices=c.USER_GENDER_CHOICE)
    avatar = models.CharField(verbose_name='头像', blank=True, max_length=255)

    # 所属门店
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)

    # 使用通用的状态，注册后默认禁用，审核通过后才能登陆
    status = models.IntegerField(verbose_name='状态', choices=c.STATUS_CHOICE, default=c.STATUS_DISABLED)

    session_key = models.CharField(verbose_name='小程序session_key', blank=True, max_length=100)
    openid = models.CharField(verbose_name='小程序openid', max_length=64, blank=True)
    unionid = models.CharField(verbose_name='微信unionid', max_length=64, blank=True)

    class Meta:
        db_table = 'yj_boss'
        verbose_name = '老板账号模型'
        verbose_name_plural = verbose_name
