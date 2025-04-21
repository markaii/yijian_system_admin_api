from django.db import models
from model_utils.models import TimeStampedModel
from uuid import uuid4
from order import constants as c


class Order(TimeStampedModel):
    """
    订单
    """
    id = models.CharField(verbose_name='pk', max_length=50, primary_key=True, default=uuid4, editable=False)

    order_no = models.CharField(verbose_name='订单号', max_length=50, blank=True, null=True)
    transaction_no = models.CharField(verbose_name='微信交易单号', max_length=50, blank=True, null=True,
                                      help_text='微信支付系统生成的订单号, 由微信支付返回')
    refund_no = models.CharField(verbose_name='退款单号', max_length=50, blank=True, null=True)
    service_fee_no = models.CharField(verbose_name='服务费单号', max_length=50, blank=True, null=True)
    serial = models.IntegerField(verbose_name='订单编号', default=1, help_text='每天每个店铺编号自增')
    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)  # 所属用户
    user_name = models.CharField(verbose_name='用户名', max_length=256, blank=True)
    user_phone = models.CharField(verbose_name='用户手机号', max_length=50, blank=True)
    user_avatar = models.CharField(verbose_name='用户头像', max_length=255, blank=True)
    service_address_id = models.CharField(verbose_name='服务地址id', max_length=50, blank=True, null=True)
    service_address = models.CharField(verbose_name='服务地址', max_length=255, blank=True, null=True)
    barber_id = models.CharField(verbose_name='理发师id', max_length=50, blank=True)
    barber_name = models.CharField(verbose_name='理发师名字', max_length=128, blank=True)
    barber_avatar = models.CharField(verbose_name='理发师头像', max_length=255, blank=True)
    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)
    shop_phone = models.CharField(verbose_name='门店手机号', max_length=50, blank=True)
    service_id = models.CharField(verbose_name='服务id', max_length=50, blank=True)
    service_name = models.CharField(verbose_name='服务名字', max_length=128, blank=True)
    # 价格
    price = models.FloatField(verbose_name='预估价格', default=0)
    discount_amount = models.FloatField(verbose_name='优惠金额', default=0)
    real_amount = models.FloatField(verbose_name='实付金额', default=0)
    min_price = models.FloatField(verbose_name='最低价格', default=0)
    max_price = models.FloatField(verbose_name='最高价格', default=0)
    price_type = models.IntegerField(verbose_name='价格类型', default=c.PRICE_TYPE_FIXED,
                                     choices=c.PRICE_TYPE_CHOICE)
    # 排序&时间
    sort = models.IntegerField(verbose_name='排序值', default=1, help_text='每天每个店铺编号自增')
    start_time = models.DateTimeField(verbose_name='开始时间', blank=True, null=True)
    service_time = models.IntegerField(verbose_name='服务时间，单位分钟', default=0, help_text='默认是当前服务的时间，可以延时')
    booking_time = models.DateTimeField(verbose_name='预约时间', blank=True, null=True)
    # 补充订单取消类型（理发师/用户取消）
    cancel_type = models.IntegerField(verbose_name='订单取消类型', choices=c.CANCEL_TYPE_CHOICE, default=c.CANCEL_TYPE_USER)
    type = models.IntegerField(verbose_name='类型', default=c.ORDER_TYPE_FORTHWITH, choices=c.ORDER_TYPE_CHOICE)
    pay_type = models.IntegerField(verbose_name='支付类型', choices=c.ORDER_PAY_TYPE_CHOICES, default=c.ORDER_PAY_TYPE_NET,
                                   help_text="线上支付/线下支付")
    pay_amount_type = models.IntegerField(verbose_name='付款金额类型', choices=c.ORDER_PAY_AMOUNT_TYPE_CHOICES,
                                          default=c.ORDER_PAY_AMOUNT_TYPE_REALITY, help_text='付款金额类型，默认现金支付')
    refund_status = models.IntegerField(verbose_name='退款状态', choices=c.REFUND_STATUS_CHOICES,
                                        default=c.REFUND_STATUS_NO)
    pay_status = models.IntegerField(verbose_name='支付状态', choices=c.PAY_STATUS_CHOICES, default=c.PAY_STATUS_NO)
    service_fee_status = models.IntegerField(verbose_name='服务费状态', choices=c.SERVICE_FEE_STATUS_CHOICES,
                                             default=c.SERVICE_FEE_STATUS_NO)
    status = models.IntegerField(verbose_name='订单状态', choices=c.ORDER_STATUS_CHOICE,
                                 default=c.ORDER_STATUS_WAITING_CONFIRM)
    remark = models.CharField(verbose_name='备注', max_length=255, blank=True)

    class Meta:
        db_table = 'yj_order'
        verbose_name = '订单模型'
        verbose_name_plural = verbose_name


class Comment(TimeStampedModel):
    """
    评论
    """
    id = models.CharField(verbose_name='pk', max_length=50, primary_key=True, default=uuid4, editable=False)

    order_id = models.CharField(verbose_name='订单id', max_length=50)

    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)  # 所属用户
    user_name = models.CharField(verbose_name='用户名', max_length=256, blank=True)
    user_avatar = models.CharField(verbose_name='用户头像', max_length=255, blank=True)

    barber_id = models.CharField(verbose_name='理发师id', max_length=50, blank=True)
    barber_name = models.CharField(verbose_name='理发师名字', max_length=128, blank=True)

    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)

    # 补充冗余存储服务名
    service_id = models.CharField(verbose_name='服务id', max_length=50, blank=True)
    service_name = models.CharField(verbose_name='服务名字', max_length=128, blank=True)

    score = models.FloatField(verbose_name='订单评分', default=0)
    content = models.CharField(verbose_name='评论内容', max_length=256, blank=True)

    class Meta:
        db_table = 'yj_order_comment'
        verbose_name = '订单评论模型'
        verbose_name_plural = verbose_name


class CommentFile(TimeStampedModel):
    """
    评论文件
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    comment_id = models.CharField(verbose_name='评论id', max_length=50)
    file = models.CharField(verbose_name='文件地址', max_length=256, blank=True)
    type = models.IntegerField(verbose_name='文件类型', default=c.FILE_TYPE_IMG, choices=c.FILE_TYPE_CHOICE)
    sort = models.IntegerField(verbose_name='排序码', default=0, help_text='升序排序')

    image = models.CharField(verbose_name='视频头图', max_length=255, blank=True)

    class Meta:
        db_table = 'yj_order_comment_file'
        verbose_name = '订单评论文件模型'
        verbose_name_plural = verbose_name


class CommentTag(TimeStampedModel):
    """
    评论标签
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    comment_id = models.CharField(verbose_name='评论id', max_length=50)
    text = models.CharField(verbose_name='标签内容', max_length=100, blank=True)

    class Meta:
        db_table = 'yj_order_comment_tag'
        verbose_name = '订单评论标签模型'
        verbose_name_plural = verbose_name
