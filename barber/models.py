from django.db import models
from model_utils.models import TimeStampedModel
from uuid import uuid4
from barber import constants as c


# Create your models here.
class Barber(TimeStampedModel):
    """
    商户理发师端账号
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    sn = models.CharField(verbose_name='理发师唯一编号', max_length=30, unique=True, editable=False,
                          help_text='10位数字字符串')
    phone = models.CharField(verbose_name='手机号', max_length=64, unique=True)
    name = models.CharField(verbose_name='用户名', max_length=128, blank=True)
    password = models.CharField(verbose_name='密码', max_length=50)
    salt = models.CharField(verbose_name='加密盐', max_length=50)

    # 所属门店
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)

    # 关联店主账号（如果是）
    boss_id = models.CharField(verbose_name='店主id', max_length=50, blank=True)
    boss_name = models.CharField(verbose_name='店主', max_length=100, blank=True)

    gender = models.IntegerField(verbose_name='性别', default=c.USER_GENDER_UNKNOWN, choices=c.USER_GENDER_CHOICE)
    avatar = models.CharField(verbose_name='头像', blank=True, max_length=255)
    work_year = models.IntegerField(verbose_name='从业年数', default=c.BARBER_WORK_LITTLE, choices=c.BARBER_WORK_TABLE)

    # 补充冗余存储入驻年数
    enter_year = models.IntegerField(verbose_name='入驻年数', default=0)
    title = models.CharField(verbose_name='头衔', max_length=100, blank=True)

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    score = models.FloatField(verbose_name='评分', default=5, help_text='根据用户评价动态计算')
    business_status = models.IntegerField(verbose_name='营业状态', default=c.BARBER_BUSINESS_STATUS_REST,
                                          choices=c.BARBER_BUSINESS_STATUS_CHOICE)
    status = models.IntegerField(verbose_name='状态', choices=c.STATUS_CHOICE, default=c.STATUS_DISABLED)

    # 理发师和老板都可以通过openid直接登陆
    session_key = models.CharField(verbose_name='小程序session_key', blank=True, max_length=100)
    openid = models.CharField(verbose_name='小程序openid', max_length=64, blank=True)
    unionid = models.CharField(verbose_name='微信unionid', max_length=64, blank=True)

    class Meta:
        db_table = 'yj_barber'
        verbose_name = '理发师账号模型'
        verbose_name_plural = verbose_name


class Example(TimeStampedModel):
    """
    作品(针对于理发师的账户)
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)

    title = models.CharField(verbose_name='作品标题', max_length=50)
    description = models.TextField(verbose_name='作品描述', blank=True)

    barber_id = models.CharField(verbose_name='理发师id', max_length=50, blank=True)
    barber_name = models.CharField(verbose_name='理发师名字', max_length=128, blank=True)

    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)
    sort = models.IntegerField(verbose_name='排序值', default=0, help_text='升序排序')
    status = models.IntegerField(verbose_name='状态', choices=c.STATUS_CHOICE, default=c.STATUS_NORMAL)

    # 冗余存储性别字段
    gender = models.IntegerField(verbose_name='性别', default=c.EXAMPLE_GENDER_UNKNOWN, choices=c.EXAMPLE_GENDER_CHOICE)

    class Meta:
        db_table = 'yj_barber_example'
        verbose_name = '理发师作品模型'
        verbose_name_plural = verbose_name


class ExampleFile(TimeStampedModel):
    """
    作品集文件(针对于理发师的账户)
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    example_id = models.CharField(verbose_name='作品id', max_length=50)
    file = models.CharField(verbose_name='文件地址', max_length=256, blank=True)
    type = models.IntegerField(verbose_name='文件类型', default=c.FILE_TYPE_IMG, choices=c.FILE_TYPE_CHOICE)
    sort = models.IntegerField(verbose_name='排序码', default=0, help_text='升序排序')

    # 冗余存储视频头图字段
    image = models.CharField(verbose_name='视频头图', max_length=255, blank=True)

    class Meta:
        db_table = 'yj_barber_example_file'
        verbose_name = '理发师作品集文件模型'
        verbose_name_plural = verbose_name


class Service(TimeStampedModel):
    """
    理发师服务项目
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='服务名', max_length=100, blank=True)
    intro = models.CharField(verbose_name='服务介绍', max_length=255, blank=True)
    duration = models.IntegerField(verbose_name='服务时长', default=30, help_text='单位分钟')
    # 理发师
    barber_id = models.CharField(verbose_name='理发师id', blank=True, max_length=50)
    barber_name = models.CharField(verbose_name='理发师名字', max_length=128, blank=True)
    # 所属门店
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)
    # 关联店铺服务项目
    shop_service_id = models.CharField(verbose_name='店铺服务id', max_length=50, blank=True)
    shop_service_name = models.CharField(verbose_name='店铺服务名字', max_length=128, blank=True)
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
        db_table = 'yj_barber_service'
        verbose_name = '服务项目模型'
        verbose_name_plural = verbose_name


class SystemService(TimeStampedModel):
    """
    系统服务项目，供理发师选择
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='服务名', max_length=100, blank=True)
    intro = models.CharField(verbose_name='服务介绍', max_length=255, blank=True)
    category_id = models.CharField(verbose_name='分类id', max_length=50, blank=True)

    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)

    class Meta:
        db_table = 'yj_barber_systemService'
        verbose_name = '系统服务项目模型'
        verbose_name_plural = verbose_name


class ServiceCategory(TimeStampedModel):
    """
    服务项目分类
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='类型名', max_length=100, blank=True)
    sort = models.IntegerField(verbose_name='排序', help_text='越小越靠前', default=0)

    # 控制字段
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)

    class Meta:
        db_table = 'yj_barber_service_category'
        verbose_name = '服务项目分类模型'
        verbose_name_plural = verbose_name
