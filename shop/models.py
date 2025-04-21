from django.db import models

from model_utils.models import TimeStampedModel
from uuid import uuid4

from shop import constants as c


class Shop(TimeStampedModel):
    """
    理发店模型
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    sn = models.CharField(verbose_name='店铺唯一编号', max_length=30, unique=True, editable=False,
                          help_text='8位数字字符串')
    # 基本信息
    name = models.CharField(verbose_name='店铺名字', max_length=100)
    phone = models.CharField(verbose_name='店铺电话', max_length=50)
    image = models.CharField(verbose_name='店铺头图', max_length=255, blank=True)
    license = models.CharField(verbose_name='营业执照', max_length=255)
    booking_type = models.IntegerField(verbose_name='取号类型', default=c.SHOP_BOOKING_TYPE_FORTHWITH,
                                       choices=c.SHOP_BOOKING_TYPE_CHOICES)
    # 身份证
    id_card_no = models.CharField(verbose_name='身份证号', max_length=100, blank=True, null=True)
    id_card_portrait_image = models.CharField(verbose_name='身份证人像面图片', max_length=255, blank=True, null=True)
    id_card_national_image = models.CharField(verbose_name='身份证国徽面图片', max_length=255, blank=True, null=True)
    # 店铺评分
    score = models.FloatField(verbose_name='评分', default=5, help_text='根据用户评价动态计算')
    # 营业时间
    open_time = models.TimeField(verbose_name='开业时间', null=True, blank=True)
    close_time = models.TimeField(verbose_name='打烊时间', null=True, blank=True)
    days = models.CharField(verbose_name="营业日期", max_length=7, help_text='示例：1111100，7位字符串，1代表选择')
    business_status = models.IntegerField(verbose_name='营业状态', default=c.SHOP_BUSINESS_STATUS_CLOSED,
                                          choices=c.SHOP_BUSINESS_STATUS_CHOICES)
    business_type = models.IntegerField(verbose_name='营业类型', default=c.SHOP_BUSINESS_TYPE_REAL,
                                        choices=c.SHOP_BUSINESS_TYPE_CHOICES)
    # 地址
    province = models.CharField(verbose_name='省份', max_length=64, blank=True)
    province_code = models.CharField(verbose_name='省份代号', max_length=32, blank=True)
    city = models.CharField(verbose_name='城市', max_length=64, blank=True)
    city_code = models.CharField(verbose_name='城市代号', max_length=32, blank=True)
    district = models.CharField(verbose_name='地区', max_length=128, blank=True)
    district_code = models.CharField(verbose_name='地区代号', max_length=32, blank=True)
    address = models.CharField(verbose_name='详细地址', help_text='详细地址', max_length=255, blank=True)
    # 经纬度
    longitude = models.CharField(verbose_name='经度', max_length=50, blank=True)
    latitude = models.CharField(verbose_name='纬度', max_length=50, blank=True)
    # 状态
    pay_service_status = models.IntegerField(verbose_name='支付服务开通状态', default=c.SHOP_PAY_SERVICE_STATUS_NOT,
                                             choices=c.SHOP_PAY_SERVICE_STATUS_CHOICES)
    status = models.IntegerField(verbose_name='状态', default=c.SHOP_STATUS_NOT, choices=c.SHOP_STATUS_CHOICE)
    is_true_shop = models.IntegerField(verbose_name='是否真实店铺', default=c.BOOL_TYPE_TRUE, choices=c.BOOL_TYPE_CHOICE)
    # 版本
    version = models.IntegerField(verbose_name='店铺版本', default=c.SHOP_VERSION_FREE, choices=c.SHOP_VERSION_CHOICES,
                                  help_text='默认免费版')
    version_status = models.IntegerField(verbose_name='版本状态', default=c.STATUS_DISABLED, choices=c.STATUS_CHOICE,
                                         help_text='默认禁用')
    # 过期类型
    expire_type = models.IntegerField(verbose_name='过期类型', default=c.SHOP_EXPIRE_TYPE_ONE_YEAR,
                                      choices=c.SHOP_EXPIRE_TYPE_CHOICES, help_text='默认一年')
    validity_start = models.DateField(verbose_name='开始时间', blank=True, null=True)
    validity_end = models.DateField(verbose_name='结束时间', blank=True, null=True)
    sub_mchid = models.CharField(verbose_name='子商户号', max_length=100, blank=True, help_text='进件申请成功微信生成的商户号')
    service_fee_rate = models.FloatField(verbose_name='服务费率', default=0.002, help_text='免费版费率千分之二，高级版费率千分之一')
    is_add_receiver = models.IntegerField(verbose_name='是否添加分账接收方', default=c.BOOL_TYPE_FALSE,
                                          choices=c.BOOL_TYPE_CHOICE)
    remark = models.CharField(verbose_name='备注', max_length=50, blank=True)

    class Meta:
        db_table = 'yj_shop'
        verbose_name = '店铺模型'
        verbose_name_plural = verbose_name


class ShopFile(TimeStampedModel):
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)

    shop_id = models.CharField(verbose_name='店铺id', max_length=50)
    shop_name = models.CharField(verbose_name='店铺名字', max_length=100, blank=True)
    file = models.CharField(verbose_name='店铺文件', max_length=256, )
    type = models.IntegerField(verbose_name='文件类型', default=c.FILE_TYPE_IMG, choices=c.FILE_TYPE_CHOICE)
    sort = models.IntegerField(verbose_name='排序码', default=0, help_text='升序，排序值小的在前面')

    class Meta:
        db_table = 'yj_shop_file'
        verbose_name = '店铺文件模型'
        verbose_name_plural = verbose_name


class PayApplyIndividual(TimeStampedModel):
    """
    个体工商户进件模型
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    # 老板
    boss_id = models.CharField(verbose_name='老板id', max_length=50, blank=True)
    boss_name = models.CharField(verbose_name='老板名', max_length=100, blank=True)
    boss_mobile = models.CharField(verbose_name='手机号', max_length=50, blank=True)
    # 身份证
    id_card_no = models.CharField(verbose_name='身份证号', max_length=100, blank=True)
    id_card_valid_type = models.IntegerField(verbose_name='证件有效期类型', choices=c.ID_CARD_VALID_TYPE_CHOICES,
                                             default=c.ID_CARD_VALID_TYPE_FIXED_DATE)
    id_card_start_date = models.CharField(verbose_name='证件生效日期', max_length=100, blank=True)
    id_card_end_date = models.CharField(verbose_name='证件失效日期', max_length=100, blank=True)
    id_card_portrait_image = models.CharField(verbose_name='身份证人像面图片', max_length=255, blank=True)
    id_card_national_image = models.CharField(verbose_name='身份证国徽面图片', max_length=255, blank=True)
    # 银行
    bank_name = models.CharField(verbose_name='银行名称', max_length=100, blank=True)
    bank_area = models.CharField(verbose_name='银行所属地区', max_length=100, blank=True)
    bank_card_no = models.CharField(verbose_name='银行卡号', max_length=100, blank=True)
    branch_bank_name = models.CharField(verbose_name='银行支行名称', max_length=100, blank=True, null=True)
    # 店铺
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺名称', max_length=100, blank=True)
    shop_image = models.CharField(verbose_name='店铺头图', max_length=255, blank=True)
    shop_context_image = models.CharField(verbose_name='店铺环境图片', max_length=255, blank=True)
    # 地址
    province = models.CharField(verbose_name='省份', max_length=64, blank=True)
    province_code = models.CharField(verbose_name='省份代号', max_length=32, blank=True)
    city = models.CharField(verbose_name='城市', max_length=64, blank=True)
    city_code = models.CharField(verbose_name='城市代号', max_length=32, blank=True)
    district = models.CharField(verbose_name='地区', max_length=128, blank=True)
    district_code = models.CharField(verbose_name='地区代号', max_length=32, blank=True)
    address = models.CharField(verbose_name='详细地址', help_text='详细地址', max_length=255, blank=True)
    # 个体户信息
    individual_name = models.CharField(verbose_name='个体户名称', max_length=100, blank=True)
    license_number = models.CharField(verbose_name='营业执照注册号', max_length=100, blank=True)
    org_code = models.CharField(verbose_name='组织机构代码', max_length=100, blank=True)
    license_image = models.CharField(verbose_name='营业执照扫描件', max_length=255, blank=True)
    email = models.CharField(verbose_name='联系邮箱', max_length=100, blank=True)
    # 微信API返回信息
    pay_apply_id = models.CharField(verbose_name='进件申请微信返回的id', max_length=255, blank=True,
                                    help_text='微信进件申请接口返回的id, 用于查看申请状态')
    sign_url = models.CharField(verbose_name='商户签约链接', max_length=255, blank=True, help_text='审核通过后，商户签约的链接')
    # 业务申请编号
    business_code = models.CharField(verbose_name='业务申请编号', max_length=100, blank=True, help_text='用于修改申请单信息')
    # 状态
    status = models.IntegerField(verbose_name='状态', default=c.PAY_APPLY_STATUS_APPLYING,
                                 choices=c.PAY_APPLY_STATUS_CHOICES)
    remark = models.CharField(verbose_name='备注', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'yj_shop_pay_apply_individual'
        verbose_name = '个体工商户进件模型'
        verbose_name_plural = verbose_name


class PayApplyEnterprise(TimeStampedModel):
    """
    企业进件模型
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    # 老板
    boss_id = models.CharField(verbose_name='老板id', max_length=50, blank=True)
    boss_name = models.CharField(verbose_name='老板名', max_length=100, blank=True)
    boss_mobile = models.CharField(verbose_name='手机号', max_length=50, blank=True)
    # 身份证
    id_card_no = models.CharField(verbose_name='身份证号', max_length=100, blank=True)
    id_card_valid_type = models.IntegerField(verbose_name='证件有效期类型', choices=c.ID_CARD_VALID_TYPE_CHOICES,
                                             default=c.ID_CARD_VALID_TYPE_FIXED_DATE)
    id_card_start_date = models.CharField(verbose_name='证件生效日期', max_length=100, blank=True)
    id_card_end_date = models.CharField(verbose_name='证件失效日期', max_length=100, blank=True)
    id_card_portrait_image = models.CharField(verbose_name='身份证人像面图片', max_length=255, blank=True)
    id_card_national_image = models.CharField(verbose_name='身份证国徽面图片', max_length=255, blank=True)
    # 银行
    bank_name = models.CharField(verbose_name='银行名称', max_length=100, blank=True)
    bank_area = models.CharField(verbose_name='银行所属地区', max_length=100, blank=True)
    bank_card_no = models.CharField(verbose_name='银行卡号', max_length=100, blank=True)
    branch_bank_name = models.CharField(verbose_name='银行支行名称', max_length=100, blank=True, null=True)
    # 店铺
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺名称', max_length=100, blank=True)
    shop_image = models.CharField(verbose_name='店铺头图', max_length=255, blank=True)
    shop_context_image = models.CharField(verbose_name='店铺环境图片', max_length=255, blank=True)
    # 地址
    province = models.CharField(verbose_name='省份', max_length=64, blank=True)
    province_code = models.CharField(verbose_name='省份代号', max_length=32, blank=True)
    city = models.CharField(verbose_name='城市', max_length=64, blank=True)
    city_code = models.CharField(verbose_name='城市代号', max_length=32, blank=True)
    district = models.CharField(verbose_name='地区', max_length=128, blank=True)
    district_code = models.CharField(verbose_name='地区代号', max_length=32, blank=True)
    address = models.CharField(verbose_name='详细地址', help_text='详细地址', max_length=255, blank=True)
    # 企业信息
    enterprise_name = models.CharField(verbose_name='企业名称', max_length=100, blank=True)
    license_number = models.CharField(verbose_name='营业执照注册号', max_length=100, blank=True)
    org_code = models.CharField(verbose_name='组织机构代码', max_length=100, blank=True)
    license_image = models.CharField(verbose_name='营业执照扫描件', max_length=255, blank=True)
    email = models.CharField(verbose_name='联系邮箱', max_length=100, blank=True)
    # 微信API返回信息
    pay_apply_id = models.CharField(verbose_name='进件申请微信返回的id', max_length=255, blank=True,
                                    help_text='微信进件申请接口返回的id, 用于查看申请状态')
    sign_url = models.CharField(verbose_name='商户签约链接', max_length=255, blank=True, help_text='审核通过后，商户签约的链接')
    # 业务申请编号
    business_code = models.CharField(verbose_name='业务申请编号', max_length=100, blank=True, help_text='用于修改申请单信息')
    # 状态
    status = models.IntegerField(verbose_name='状态', default=c.PAY_APPLY_STATUS_APPLYING,
                                 choices=c.PAY_APPLY_STATUS_CHOICES)
    remark = models.CharField(verbose_name='备注', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'yj_shop_pay_apply_enterprise'
        verbose_name = '企业进件模型'
        verbose_name_plural = verbose_name


class ShopService(TimeStampedModel):
    """
    店铺服务项目
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='服务名', max_length=100, blank=True)
    intro = models.CharField(verbose_name='服务介绍', max_length=255, blank=True)
    duration = models.IntegerField(verbose_name='服务时长', default=30, help_text='单位分钟')
    # 所属门店
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)
    # 价格
    price = models.FloatField(verbose_name='预估价格', default=0)
    min_price = models.FloatField(verbose_name='最低价格', default=0)
    max_price = models.FloatField(verbose_name='最高价格', default=0)
    price_type = models.IntegerField(verbose_name='价格类型', default=c.PRICE_TYPE_FIXED,
                                     choices=c.PRICE_TYPE_CHOICE)
    is_secrecy = models.IntegerField(verbose_name='是否保密', default=c.SERVICE_PRICE_SECRECY_NO,
                                     choices=c.SERVICE_PRICE_SECRECY_TABLE)

    sort = models.IntegerField(verbose_name='排序值', default=0, help_text='升序排序')

    class Meta:
        db_table = 'yj_shop_service'
        verbose_name = '店铺服务项目模型'
        verbose_name_plural = verbose_name


class MerchantOrder(TimeStampedModel):
    """
    商户订单
    """
    id = models.CharField(verbose_name='pk', max_length=50, primary_key=True, default=uuid4, editable=False)
    order_no = models.CharField(verbose_name='订单号', max_length=50, blank=True, null=True, help_text='微信支付返回的订单号')
    # 店铺
    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)
    shop_phone = models.CharField(verbose_name='门店手机号', max_length=50, blank=True)
    # 价格
    price = models.FloatField(verbose_name='预估价格', default=0)
    discount_amount = models.FloatField(verbose_name='优惠金额', default=0)
    real_amount = models.FloatField(verbose_name='实付金额', default=0)
    status = models.IntegerField(verbose_name='订单状态', choices=c.ORDER_STATUS_CHOICE,
                                 default=c.ORDER_STATUS_WAITING_PAY, help_text='默认待支付')
    remark = models.CharField(verbose_name='备注', max_length=255, blank=True)

    class Meta:
        db_table = 'yj_shop_merchant_order'
        verbose_name = '商户订单模型'
        verbose_name_plural = verbose_name
