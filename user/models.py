import uuid
import hashlib
from django.db import models
from model_utils.models import TimeStampedModel

from user import constants as c


class User(TimeStampedModel):
    """
    消费者用户（会员）
    描述：消费者只要是授权了就是我们的线上会员了，为了和线下结合还需要补充字段
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    phone = models.CharField(verbose_name='手机号', max_length=64, blank=True)
    openid = models.CharField(verbose_name='小程序openid', max_length=64, blank=True)
    mp_openid = models.CharField(verbose_name='公众号openid', max_length=64, blank=True)
    unionid = models.CharField(verbose_name='unionid', max_length=64, blank=True)
    name = models.CharField(verbose_name='昵称', max_length=128, blank=True)
    avatar = models.CharField(verbose_name='头像', blank=True, max_length=255)
    session_key = models.CharField(verbose_name='小程序session_key', blank=True, max_length=100)
    gender = models.IntegerField(verbose_name='性别', choices=c.USER_GENDER_CHOICE, default=c.USER_GENDER_UNKNOWN)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    email = models.CharField(verbose_name='邮箱', blank=True, max_length=255)
    hair_change_use_count = models.IntegerField(verbose_name='换发功能使用次数', default=0)

    credit = models.IntegerField(verbose_name='积分', help_text='用户当前所有积分', default=0)
    status = models.IntegerField(verbose_name='状态', choices=c.STATUS_CHOICE, default=c.STATUS_NORMAL, help_text='正常、禁用')
    last_login_time = models.DateTimeField(verbose_name="最近登录时间", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '消费者用户'
        verbose_name_plural = verbose_name
        db_table = 'yj_user'


class UserAddress(TimeStampedModel):
    """
    收货地址
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    user_id = models.CharField(verbose_name='用户id', max_length=50)
    name = models.CharField(verbose_name='收件人', max_length=128)
    phone = models.CharField(verbose_name='电话', max_length=64)
    province = models.CharField(verbose_name='省份', max_length=64, blank=True)
    province_code = models.CharField(verbose_name='省份代号', max_length=32, blank=True)
    city = models.CharField(verbose_name='城市', max_length=64, blank=True)
    city_code = models.CharField(verbose_name='城市代号', max_length=32, blank=True)
    district = models.CharField(verbose_name='地区', max_length=128, blank=True)
    district_code = models.CharField(verbose_name='地区代号', max_length=32, blank=True)
    address = models.CharField(verbose_name='收件地址', help_text='详细地址', max_length=255, blank=True)
    default = models.IntegerField(verbose_name='默认地址', default=c.BOOL_TYPE_FALSE, choices=c.BOOL_TYPE_CHOICE)

    def __str__(self):
        return "%s: %s" % (self.name, self.address)

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
        db_table = 'yj_user_address'


class CreditLog(TimeStampedModel):
    """
    用户积分变更记录
    什么时间 哪个用户 参与了什么活动 增加了还是减少了 多少积分
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    user_id = models.CharField(verbose_name='用户id', max_length=50)
    user_name = models.CharField(verbose_name='用户名', max_length=200, blank=True)
    credit = models.IntegerField(verbose_name='积分变化', help_text='积分变化量可以为正数也可以为负数，正数则增加，负数则减少')
    remain = models.IntegerField(verbose_name='剩余积分', blank=True, null=True)
    merchant_id = models.CharField(verbose_name='商城id', blank=True, null=True, max_length=50)
    type = models.IntegerField(verbose_name='变更类型', default=c.CREDIT_TYPE_PLUS, choices=c.CREDIT_TYPE_CHOICE)
    remark = models.CharField(verbose_name='备注', max_length=255, help_text='由客户端创建的备注信息', blank=True)

    def __str__(self):
        return "[%s] %s" % (self.user_name, self.remark)

    class Meta:
        verbose_name = '积分记录'
        verbose_name_plural = verbose_name
        db_table = 'yj_user_credit_log'


class UserLoginLog(TimeStampedModel):
    """
    用户登录记录
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    user_id = models.CharField(verbose_name='用户id', max_length=50)
    user_name = models.CharField(verbose_name='姓名', max_length=255, blank=True)
    ip = models.CharField(verbose_name='ip', max_length=255, blank=True)
    ip_city = models.CharField(verbose_name='所在城市', max_length=255, blank=True)

    class Meta:
        verbose_name = '用户登录记录'
        verbose_name_plural = verbose_name
        db_table = 'yj_user_login_log'


class Collection(TimeStampedModel):
    """
    用户收藏记录
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺名', max_length=128, blank=True)
    barber_id = models.CharField(verbose_name='理发师id', max_length=50, blank=True)
    barber_name = models.CharField(verbose_name='理发师名', max_length=128, blank=True)
    example_id = models.CharField(verbose_name='作品id', max_length=50, blank=True)
    example_name = models.CharField(verbose_name='作品名', max_length=128, blank=True)
    type = models.IntegerField(verbose_name='收藏类型', default=c.COLLECT_TYPE_CANCEL, choices=c.COLLECT_TYPE_TABLE)

    class Meta:
        verbose_name = '用户收藏记录'
        verbose_name_plural = verbose_name
        db_table = 'yj_user_collection'


class CustomerOrder(TimeStampedModel):
    """
    客户订单
    """
    id = models.CharField(verbose_name='pk', max_length=50, primary_key=True, default=uuid.uuid4, editable=False)
    order_no = models.CharField(verbose_name='订单号', max_length=50, blank=True, null=True, help_text='微信支付返回的订单号')
    # 客户
    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)
    user_name = models.CharField(verbose_name='用户姓名', max_length=255, blank=True, null=True)
    user_phone = models.CharField(verbose_name='用户手机号', max_length=50, blank=True, null=True)
    # 价格
    price = models.FloatField(verbose_name='预估价格', default=0)
    discount_amount = models.FloatField(verbose_name='优惠金额', default=0)
    real_amount = models.FloatField(verbose_name='实付金额', default=0)
    system_config_id = models.CharField(verbose_name='系统配置id', max_length=50, blank=True)
    status = models.IntegerField(verbose_name='订单状态', choices=c.ORDER_STATUS_CHOICE,
                                 default=c.ORDER_STATUS_WAITING_PAY, help_text='默认待支付')
    type = models.IntegerField(verbose_name='类型', choices=c.ORDER_TYPE_CHOICE, default=c.ORDER_TYPE_HAIR_CHANGE)
    remark = models.CharField(verbose_name='备注', max_length=255, blank=True)

    class Meta:
        db_table = 'yj_user_customer_order'
        verbose_name = '客户订单'
        verbose_name_plural = verbose_name


class CountLog(TimeStampedModel):
    """
    用户换发次数记录
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    user_id = models.CharField(verbose_name='用户id', max_length=50)
    user_name = models.CharField(verbose_name='姓名', max_length=255, blank=True)
    count = models.IntegerField(verbose_name='次数变化', blank=True, default=0)
    remain = models.IntegerField(verbose_name='剩余次数', blank=True, null=True)

    class Meta:
        verbose_name = '用户使用次数记录'
        verbose_name_plural = verbose_name
        db_table = 'yj_user_count_log'
