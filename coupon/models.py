from django.db import models
from uuid import uuid4

from coupon import constants as c
from activity import constants as activity_c

from model_utils.models import TimeStampedModel


class Coupon(TimeStampedModel):
    """
    优惠券 - 包括统建券和异业券
    字段：优惠券名称、优惠券备注（副标题）、业务类型（）、优惠券类型（代金券、满减、满折）、面额（固定金额、动态金额）、有效期（固定有效期、动态有效期）
    面值、用券规则、发券单位、成本价、积分兑换价、记账编码、
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='优惠券名称', blank=False, max_length=100)
    code = models.CharField(verbose_name='优惠券码', max_length=100,
                            help_text="唯一标识，随机生成20位随机数", blank=True)
    remark = models.CharField(verbose_name='备注', max_length=255, help_text='副标题', blank=True)
    # 规则
    intro = models.TextField(verbose_name='使用规则介绍', blank=True)
    cover = models.CharField(verbose_name='封面图片', max_length=255, blank=True)

    # 异业券关联的商铺信息
    shop_id = models.CharField(verbose_name='关联店铺', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺名', max_length=255, blank=True)

    # 优惠券类型
    # 1. 代金券（无门槛）：直接设置固定面额/随机面额
    # 2. 满减券：满XX元减少固定金额/随机金额
    # 3. 折扣券：满XX元打YY折，最多抵扣KK元
    type = models.IntegerField(verbose_name='优惠券类型', default=c.COUPON_TYPE_CASH,
                               choices=c.COUPON_TYPE_CHOICE)
    order_amount = models.FloatField(verbose_name='满XX元', default=0, help_text='最低消费金额')
    discount = models.FloatField(verbose_name='折扣', default=100, help_text='折扣，如95折，不能超过100')
    # 面额
    value_type = models.IntegerField(verbose_name='面额类型', default=c.COUPON_VALUE_TYPE_FIXED,
                                     choices=c.COUPON_VALUE_TYPE_CHOICE)
    value_min = models.FloatField(verbose_name='面额下限', default=0)
    value_max = models.FloatField(verbose_name='面额上线', default=100)
    value = models.FloatField(verbose_name='面额', default=0)

    # 有效期
    validity_type = models.IntegerField(verbose_name='有效期类型', default=c.COUPON_VALIDITY_TYPE_FIXED,
                                        choices=c.COUPON_VALIDITY_TYPE_CHOICE,
                                        help_text='固定有效期：选择有效期起止时间；浮动有效期：选择优惠券发放后的有效期长度')
    validity_days = models.IntegerField(verbose_name='有效时长', default=0, help_text="按照天数")
    validity_start = models.DateTimeField(verbose_name='有效期始', null=True, blank=True)
    validity_end = models.DateTimeField(verbose_name='有效期止', null=True, blank=True)
    # 优惠券数量
    total_count = models.IntegerField(verbose_name='总数', help_text='可投券数量', default=0)
    # 投券voucher数量
    delivered_count = models.IntegerField(verbose_name='已投券数量', default=0)

    status = models.IntegerField(verbose_name='状态', default=c.STATUS_NORMAL, choices=c.STATUS_CHOICE)

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '优惠券'
        verbose_name_plural = verbose_name
        db_table = 'yj_coupon'


class CouponVoucher(TimeStampedModel):
    """
    优惠券记录
    用户领取优惠券之后生成一条优惠券记录
    用户根据这个优惠券记录进行核销
    描述：用户领取优惠券后生成，支持异业券
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    # 根据来源类型关联不同的优惠券模型
    coupon_id = models.CharField(verbose_name='优惠券id', blank=False, max_length=50)
    coupon_name = models.CharField(verbose_name='优惠券名称', blank=False, max_length=100)
    # 用户
    user_id = models.CharField(verbose_name='用户id', blank=False, max_length=50)
    user_name = models.CharField(verbose_name='用户名字', blank=False, max_length=50)
    # 随机生成的核销码
    voucher = models.CharField(verbose_name='核销编码', blank=False, max_length=50)
    # 面额，根据面额类型计算出来的最终面额
    value = models.FloatField(verbose_name='面额', default=0)
    # 开始时间
    start_time = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    # 过期时间
    expired_time = models.DateTimeField(verbose_name='过期时间', null=True, blank=True)
    # 核销时间
    verify_time = models.DateTimeField(verbose_name='核销时间', null=True, blank=True)
    # 状态
    status = models.IntegerField(verbose_name='状态', default=c.VOUCHER_STATUS_WAITING,
                                 choices=c.VOUCHER_STATUS_CHOICE)

    # 活动
    order_id = models.CharField(verbose_name='订单id', blank=True, max_length=50, null=True)
    activity_id = models.CharField(verbose_name='活动配置id', blank=True, max_length=50, null=True,
                                   help_text='不同的活动来源对应不同的id')
    activity_name = models.CharField(verbose_name='活动名', max_length=100, blank=True, null=True)
    activity_type = models.IntegerField(verbose_name='活动类型', default=activity_c.COUPON_ACTIVITY_TYPE_CONSUME,
                                        choices=activity_c.COUPON_ACTIVITY_TYPE_CHOICE)
    # 商铺id
    shop_id = models.CharField(verbose_name='商铺id', blank=True, max_length=50)
    shop_name = models.CharField(verbose_name='商铺名字', blank=True, max_length=50)
    # 理发师
    barber_id = models.CharField(verbose_name='理发师id', blank=True, max_length=50, null=True)
    barber_name = models.CharField(verbose_name='理发师名字', blank=True, max_length=50, null=True)

    amount = models.FloatField(verbose_name='核销订单的总金额（元）', default=0, null=True)

    def __str__(self):
        return self.coupon_name

    class Meta:
        verbose_name = '优惠券-领券记录'
        verbose_name_plural = verbose_name
        db_table = 'yj_coupon_voucher'


class CouponDailyStatis(TimeStampedModel):
    """
    优惠券每日数据汇总
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)

    # 活动
    activity_id = models.CharField(verbose_name='活动配置id', blank=True, max_length=50,
                                   help_text='不同的活动来源对应不同的id')
    activity_name = models.CharField(verbose_name='活动名', max_length=100, blank=True)

    delivery_count = models.IntegerField(verbose_name='派发数量', default=0, help_text='根据voucher的数量计算')
    verify_count = models.IntegerField(verbose_name='核销次数', default=0)

    date = models.DateField(verbose_name='日期', null=True)
    create_year = models.IntegerField(verbose_name='年', blank=True, null=True)  # 冗余存年、月、日，便于筛选
    create_month = models.IntegerField(verbose_name='月', blank=True, null=True)
    create_day = models.IntegerField(verbose_name='日', blank=True, null=True)

    class Meta:
        db_table = 'yj_coupon_daily_statis'
        verbose_name = '优惠券数据统计'
        verbose_name_plural = verbose_name
