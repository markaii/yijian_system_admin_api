from django.db import models
from model_utils.models import TimeStampedModel
from common.utils import UUIDTools

from coupon import constants as coupon_c
from member import constants as c


class MemberCard(TimeStampedModel):
    """
    商家创建的会员卡
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    name = models.CharField(verbose_name='会员卡名称', max_length=100, help_text='如白金VIP，钻石VIP')
    level = models.IntegerField(verbose_name='会员卡等级', default=c.CARD_LEVEL_FOURTH, choices=c.CARD_LEVEL_CHOICES,
                                help_text='会员卡等级，默认白金VIP')
    open_card_amount = models.FloatField(verbose_name='开卡金额', default=0, help_text='开通会员卡所需的金额')
    # 过期类型
    expire_type = models.IntegerField(verbose_name='过期类型', default=c.CARD_EXPIRE_TYPE_ALWAYS,
                                      choices=c.CARD_EXPIRE_TYPE_CHOICES, help_text='默认永久')
    # 门店
    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)

    status = models.IntegerField(verbose_name='状态', default=c.STATUS_NORMAL, choices=c.STATUS_CHOICE)
    sort = models.IntegerField(verbose_name='排序码', default=0, help_text='升序排序')

    class Meta:
        verbose_name = '会员卡'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_card'


class MemberCardDiscount(TimeStampedModel):
    """
    商家会员卡折扣
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    # 会员卡
    card_id = models.CharField(verbose_name='会员卡id', max_length=50, blank=True)
    card_name = models.CharField(verbose_name='会员卡名字', max_length=128, blank=True)
    # 折扣
    type = models.IntegerField(verbose_name='折扣类型', default=c.CARD_DISCOUNT_TYPE_REDUCTION,
                               choices=c.CARD_DISCOUNT_TYPE_CHOICES, help_text="默认每单立减")
    order_amount = models.FloatField(verbose_name='立减金额', default=0, help_text='每单立减XX元')
    discount = models.FloatField(verbose_name='折扣', default=100, help_text='折扣，如95折，不能超过100')

    class Meta:
        verbose_name = '会员卡折扣'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_card_discount'


class MemberCardCoupon(TimeStampedModel):
    """
    商家会员卡关联优惠券
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    # 会员卡
    card_id = models.CharField(verbose_name='会员卡id', max_length=50, blank=True)
    card_name = models.CharField(verbose_name='会员卡名字', max_length=128, blank=True)
    # 优惠券
    coupon_id = models.CharField(verbose_name='优惠券id', blank=False, max_length=50)
    coupon_name = models.CharField(verbose_name='优惠券名称', blank=False, max_length=100)
    count = models.IntegerField(verbose_name='优惠券数量', blank=True)

    class Meta:
        verbose_name = '会员卡关联优惠券'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_card_coupon'


class MemberCardChargeRule(TimeStampedModel):
    """
    商家会员卡关联充值充值规则
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    # 会员卡
    card_id = models.CharField(verbose_name='会员卡id', max_length=50, blank=True)
    card_name = models.CharField(verbose_name='会员卡名字', max_length=128, blank=True)
    # 满XX元，送XX元
    full_amount = models.FloatField(verbose_name='满XX元', default=0)
    send_amount = models.FloatField(verbose_name='送XX元', default=0)

    class Meta:
        verbose_name = '会员卡关联充值优惠'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_card_charge_rule'


class MemberCardInstance(TimeStampedModel):
    """
    用户开通的会员卡
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    # 会员
    user_id = models.CharField(verbose_name='会员id', max_length=50)
    user_name = models.CharField(verbose_name='会员名称', max_length=100, blank=True)
    user_phone = models.CharField(verbose_name='会员手机号', max_length=64, blank=True)
    # 门店
    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)
    # 会员卡
    card_id = models.CharField(verbose_name='会员卡id', max_length=50, blank=True)
    card_name = models.CharField(verbose_name='会员卡名字', max_length=128, blank=True)
    level = models.IntegerField(verbose_name='会员卡等级', default=c.CARD_LEVEL_FOURTH, choices=c.CARD_LEVEL_CHOICES,
                                help_text='关联会员卡等级')
    # 金额
    open_card_amount = models.FloatField(verbose_name='开卡金额', default=0, help_text='开通会员卡所需的金额')
    balance = models.FloatField(verbose_name='余额', default=0)
    consume_amount = models.FloatField(verbose_name='消费金额', default=0)
    total_amount = models.FloatField(verbose_name='充值总额', default=0)
    # 过期类型
    expire_type = models.IntegerField(verbose_name='过期类型', default=c.CARD_EXPIRE_TYPE_ALWAYS,
                                      choices=c.CARD_EXPIRE_TYPE_CHOICES, help_text='默认永久')
    validity_start = models.DateField(verbose_name='开始时间', blank=True, null=True)
    validity_end = models.DateField(verbose_name='结束时间', blank=True, null=True)
    card_no = models.CharField(verbose_name='卡号', max_length=50, blank=True, null=True)
    status = models.IntegerField(verbose_name='状态', default=c.CARD_STATUS_DISABLED, choices=c.CARD_STATUS_CHOICES,
                                 help_text='默认禁用')

    class Meta:
        verbose_name = '会员开卡记录'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_card_instance'


class MemberCardInstanceDiscount(TimeStampedModel):
    """
    用户会员卡关联折扣
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    # 会员卡实例
    card_instance_id = models.CharField(verbose_name='会员开卡id', max_length=50, blank=True)
    # 会员卡
    card_id = models.CharField(verbose_name='会员卡id', max_length=50, blank=True)
    card_name = models.CharField(verbose_name='会员卡名字', max_length=128, blank=True)
    # 折扣
    type = models.IntegerField(verbose_name='折扣类型', default=c.CARD_DISCOUNT_TYPE_REDUCTION,
                               choices=c.CARD_DISCOUNT_TYPE_CHOICES, help_text="默认每单立减")
    order_amount = models.FloatField(verbose_name='立减金额', default=0, help_text='每单立减XX元')
    discount = models.FloatField(verbose_name='折扣', default=100, help_text='折扣，如95折，不能超过100')

    class Meta:
        verbose_name = '会员开卡关联折扣'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_card_instance_discount'


class MemberCardInstanceChargeRule(TimeStampedModel):
    """
    用户会员卡关联充值优惠规则
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    # 会员卡实例
    card_instance_id = models.CharField(verbose_name='会员开卡id', max_length=50, blank=True)
    # 会员卡
    card_id = models.CharField(verbose_name='会员卡id', max_length=50, blank=True)
    card_name = models.CharField(verbose_name='会员卡名字', max_length=128, blank=True)
    # 满XX元，送XX元
    full_amount = models.FloatField(verbose_name='满XX元', default=0)
    send_amount = models.FloatField(verbose_name='送XX元', default=0)

    class Meta:
        verbose_name = '会员开卡关联充值优惠规则'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_card_instance_charge_rule'


class MemberCardChargeLog(TimeStampedModel):
    """
    用户会员卡充值记录
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    # 会员卡实例
    card_instance_id = models.CharField(verbose_name='会员开卡id', max_length=50, blank=True)
    card_no = models.CharField(verbose_name='会员卡号', max_length=50, blank=True, null=True)
    # 会员卡
    card_id = models.CharField(verbose_name='会员卡id', max_length=50, blank=True)
    card_name = models.CharField(verbose_name='会员卡名字', max_length=128, blank=True)
    level = models.IntegerField(verbose_name='会员卡等级', default=c.CARD_LEVEL_FOURTH, choices=c.CARD_LEVEL_CHOICES,
                                help_text='关联会员卡等级')
    # 会员
    user_id = models.CharField(verbose_name='会员id', max_length=50, blank=True)
    user_name = models.CharField(verbose_name='会员名称', max_length=100, blank=True)
    # 门店
    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)

    balance = models.FloatField(verbose_name='余额', default=0)
    charge_time = models.DateTimeField(verbose_name='充值时间', blank=True)
    charge_amount = models.FloatField(verbose_name='充值金额', default=0)
    send_amount = models.FloatField(verbose_name='赠送金额', default=0)

    class Meta:
        verbose_name = '会员卡充值记录'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_card_charge_log'


class MemberCardConsumeLog(TimeStampedModel):
    """
    用户会员卡消费记录
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    # 会员卡实例
    card_instance_id = models.CharField(verbose_name='会员开卡id', max_length=50, blank=True)
    card_no = models.CharField(verbose_name='会员卡号', max_length=50, blank=True, null=True)
    # 会员卡
    card_id = models.CharField(verbose_name='会员卡id', max_length=50, blank=True)
    card_name = models.CharField(verbose_name='会员卡名字', max_length=128, blank=True)
    level = models.IntegerField(verbose_name='会员卡等级', default=c.CARD_LEVEL_FOURTH, choices=c.CARD_LEVEL_CHOICES,
                                help_text='关联会员卡等级')
    # 会员
    user_id = models.CharField(verbose_name='会员id', max_length=50, blank=True)
    user_name = models.CharField(verbose_name='会员名称', max_length=100, blank=True)
    # 门店
    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)
    # 订单
    order_id = models.CharField(verbose_name='订单id', blank=True, max_length=50)

    balance = models.FloatField(verbose_name='余额', default=0)
    project_amount = models.FloatField(verbose_name='项目金额', default=0)
    consume_time = models.DateTimeField(verbose_name='消费时间', blank=True)
    consume_amount = models.FloatField(verbose_name='消费金额', default=0, help_text='余额支付的消费金额')
    discount_amount = models.FloatField(verbose_name='优惠金额', default=0)

    class Meta:
        verbose_name = '会员卡消费记录'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_card_consume_log'


class MemberChargeOrder(TimeStampedModel):
    """
    会员充值订单
    """
    id = models.CharField(primary_key=True, max_length=50, default=UUIDTools.uuid4, editable=False)
    # 用户会员卡
    card_instance_id = models.CharField(verbose_name='用户会员卡id', max_length=50, blank=True)
    # 商家会员卡
    card_id = models.CharField(verbose_name='商家会员卡id', max_length=50, blank=True)
    card_name = models.CharField(verbose_name='商家会员卡名字', max_length=128, blank=True)

    user_id = models.CharField(verbose_name='会员id', max_length=50, blank=True)
    user_name = models.CharField(verbose_name='会员名称', max_length=100, blank=True)
    user_phone = models.CharField(verbose_name='用户手机号', max_length=50, blank=True)
    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)

    amount = models.FloatField(verbose_name='金额', default=0)
    order_no = models.CharField(verbose_name='支付订单号', max_length=50, blank=True, null=True, help_text='调起微信支付本地生成的订单号')
    service_fee_no = models.CharField(verbose_name='服务费单号', max_length=50, blank=True, null=True)
    transaction_no = models.CharField(verbose_name='微信交易单号', max_length=50, blank=True, null=True,
                                      help_text='微信支付系统生成的订单号, 由微信支付返回')
    service_fee_status = models.IntegerField(verbose_name='服务费状态', choices=c.SERVICE_FEE_STATUS_CHOICES,
                                             default=c.SERVICE_FEE_STATUS_NO)
    status = models.IntegerField(verbose_name='状态', default=c.ORDER_STATUS_WAITING_PAY, choices=c.ORDER_STATUS_CHOICE,
                                 help_text='默认待支付')

    class Meta:
        verbose_name = '会员充值订单'
        verbose_name_plural = verbose_name
        db_table = 'yj_member_charge_order'
