from django.db import models
from uuid import uuid4

from activity import constants as c

from model_utils.models import TimeStampedModel


class Banner(TimeStampedModel):
    """
    小程序广告配置
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='广告名称', max_length=250, blank=True)
    cover = models.CharField(verbose_name='封面图', max_length=250)
    jump_path = models.CharField(verbose_name='跳转路径', max_length=100, blank=True, help_text='如果为空则不跳转')
    jump_type = models.IntegerField(verbose_name='跳转类型', default=c.BANNER_JUMP_TYPE_APPLET,
                                    choices=c.BANNER_JUMP_TYPE_CHOICE)
    position = models.CharField(verbose_name='页面路径', blank=True, max_length=100,
                                help_text='广告位展示位置，如首页为：pages/index/index，若为空则匹配所有广告展示页面')
    status = models.IntegerField(verbose_name='状态', default=c.STATUS_NORMAL, choices=c.STATUS_CHOICE)
    applet_type = models.IntegerField(verbose_name='小程序类型', default=c.BANNER_APPLET_TYPE_MERCHANT,
                                      choices=c.BANNER_APPLET_TYPE_CHOICE)
    third_appid = models.CharField(verbose_name='第三方小程序ID', max_length=50, blank=True)
    remark = models.CharField(verbose_name='备注', blank=True, max_length=250)
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '广告配置'
        verbose_name_plural = verbose_name
        db_table = 'yj_banner'


class ShopInviteActivity(TimeStampedModel):
    """
    店铺邀请入驻活动
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='扫码活动名', max_length=250, blank=True)
    code = models.CharField(verbose_name='唯一的活动编码', max_length=250, unique=True,
                            help_text='根据活动编码查询活动配置，自动生成10位随机数', blank=True)
    status = models.IntegerField(verbose_name='状态', default=c.ACTIVITY_STATUS_WAITING,
                                 choices=c.ACTIVITY_STATUS_CHOICE, help_text='默认是等待开始')
    desc = models.TextField(verbose_name='详细介绍', blank=True)
    applet_type = models.IntegerField(verbose_name='小程序类型', default=c.BANNER_APPLET_TYPE_MERCHANT,
                                      choices=c.BANNER_APPLET_TYPE_CHOICE)

    image = models.CharField(verbose_name='活动图片', blank=True, max_length=255)
    # 自动结束时间
    start_date = models.DateField(verbose_name='活动开始日期', null=True, blank=True,
                                  help_text='认为是当前日期的00:00:00')
    end_date = models.DateField(verbose_name='活动结束日期', null=True, blank=True,
                                help_text='认为是当天的23:59:59')
    # 奖励
    inviter_award_amount = models.IntegerField(verbose_name='邀请人奖励金额', default=0)
    boss_award_amount = models.IntegerField(verbose_name='老板奖励金额', default=0)

    award_limit = models.IntegerField(verbose_name='奖励人数限制', default=1)
    award_count = models.IntegerField(verbose_name='奖励数量', default=0, help_text='不能超过人数限制')

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        db_table = 'yj_shop_invite_activity'
        verbose_name_plural = verbose_name = '邀请入驻店铺活动'


class ShopInviteLog(TimeStampedModel):
    """
    店铺入驻邀请记录
    老板通过邀请链接申请入驻时创建
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)

    # 邀请人，可能是老板、理发师、用户
    inviter_id = models.CharField(verbose_name='邀请人id', max_length=50, blank=True)
    inviter_openid = models.CharField(verbose_name='邀请人公众号openid', max_length=50, blank=True)
    inviter_name = models.CharField(verbose_name='邀请人名', max_length=255, blank=True)
    inviter_type = models.CharField(verbose_name='邀请人类型', default=c.SHOP_INVITE_USER_TYPE_BOSS, blank=True,
                                    max_length=255)

    # 申请店铺
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺名', max_length=250, blank=True)

    # 老板
    boss_id = models.CharField(verbose_name='老板id', max_length=50, blank=True)
    boss_name = models.CharField(verbose_name='老板名', max_length=250, blank=True)
    boss_phone = models.CharField(verbose_name='老板手机号', max_length=50, blank=True)
    boss_openid = models.CharField(verbose_name='老板公众号openid', max_length=50, blank=True)

    # 奖励
    inviter_award_amount = models.IntegerField(verbose_name='邀请人奖励金额', default=0)
    boss_award_amount = models.IntegerField(verbose_name='老板奖励金额', default=0)
    # 状态
    status = models.IntegerField(verbose_name='邀请状态', default=c.SHOP_INVITE_STATUS_APPLIED,
                                 choices=c.SHOP_INVITE_STATUS_CHOICE, help_text='店铺入驻审核通过时改状态，完成订单后活动完成')

    class Meta:
        db_table = 'yj_shop_invite_log'
        verbose_name_plural = verbose_name = '邀请入驻活动日志'


class ShopPosterApply(TimeStampedModel):
    """
    店铺物料申请
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='收件人', max_length=128)
    phone = models.CharField(verbose_name='手机号', max_length=64, unique=True)

    # 所属门店
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)

    # 地址
    province = models.CharField(verbose_name='省份', max_length=64, blank=True)
    province_code = models.CharField(verbose_name='省份代号', max_length=32, blank=True)
    city = models.CharField(verbose_name='城市', max_length=64, blank=True)
    city_code = models.CharField(verbose_name='城市代号', max_length=32, blank=True)
    district = models.CharField(verbose_name='地区', max_length=128, blank=True)
    district_code = models.CharField(verbose_name='地区代号', max_length=32, blank=True)
    address = models.CharField(verbose_name='详细地址', help_text='详细地址', max_length=255, blank=True)

    status = models.IntegerField(verbose_name='状态', default=c.SHOP_POSTER_APPLY_STATUS_APPLIED,
                                 choices=c.SHOP_POSTER_APPLY_STATUS_CHOICE)

    remark = models.CharField(verbose_name='备注', max_length=50, blank=True)

    class Meta:
        db_table = 'yj_shop_poster_apply'
        verbose_name_plural = verbose_name = '店铺物料申请'


class ShopPosterApplyLog(TimeStampedModel):
    """
    店铺物料申请记录
    申请时创建
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    user_id = models.CharField(verbose_name='申请人id', max_length=50, blank=True)
    apply_id = models.CharField(verbose_name='物料申请id', max_length=50, blank=True)

    name = models.CharField(verbose_name='收件人', max_length=128)
    phone = models.CharField(verbose_name='手机号', max_length=64, unique=True)

    # 所属门店
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)

    status = models.IntegerField(verbose_name='状态', default=c.SHOP_POSTER_APPLY_STATUS_APPLIED,
                                 choices=c.SHOP_POSTER_APPLY_STATUS_CHOICE)

    remark = models.CharField(verbose_name='备注', max_length=50, blank=True, help_text='审核时不通过的备注')

    class Meta:
        db_table = 'yj_shop_poster_apply_Log'
        verbose_name_plural = verbose_name = '店铺物料申请记录'


############### 老板自定义的营销活动（派券）################
class ShopCouponActivity(TimeStampedModel):
    """
    店铺优惠券活动
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='活动名', max_length=250, blank=True)
    code = models.CharField(verbose_name='唯一的活动编码', max_length=250, unique=True,
                            help_text='根据活动编码查询活动配置，自动生成16位随机数', blank=True)
    status = models.IntegerField(verbose_name='状态', default=c.ACTIVITY_STATUS_WAITING,
                                 choices=c.ACTIVITY_STATUS_CHOICE, help_text='默认是等待开始')

    # 所属门店
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)

    # 限制
    is_limit_delivery_count = models.IntegerField(verbose_name='是否限制发券数量', default=c.BOOL_TYPE_FALSE,
                                                  choices=c.BOOL_TYPE_CHOICE)
    is_limit_amount = models.IntegerField(verbose_name='是否限制返券金额', default=c.BOOL_TYPE_FALSE,
                                          choices=c.BOOL_TYPE_CHOICE)
    is_share = models.IntegerField(verbose_name='是否分享', default=c.BOOL_TYPE_FALSE, choices=c.BOOL_TYPE_CHOICE)
    delivery_count = models.IntegerField(verbose_name='发券数量', default=0)
    amount = models.IntegerField(verbose_name='消费金额', default=0)

    type = models.IntegerField(verbose_name='活动类型', default=c.COUPON_ACTIVITY_TYPE_CONSUME,
                               choices=c.COUPON_ACTIVITY_TYPE_CHOICE, help_text='默认是消费返券')
    # 拼团
    pin_expired_time = models.IntegerField(verbose_name='拼团过期时间', default=24, help_text='单位（小时）')
    pin_required_num = models.IntegerField(verbose_name='需要的人数', default=5, help_text='成功成功所需次数')
    pin_succeed_limit_num = models.IntegerField(verbose_name='每人开团成功限制数', default=1, help_text='每个人可开团成功的次数')
    pin_join_limit_num = models.IntegerField(verbose_name='每人参与拼团限制数', default=3, help_text='每个人可参与拼团的次数')

    # 自动结束时间
    start_date = models.DateField(verbose_name='活动开始日期', null=True, blank=True,
                                  help_text='认为是当前日期的00:00:00')
    end_date = models.DateField(verbose_name='活动结束日期', null=True, blank=True,
                                help_text='认为是当天的23:59:59')

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        db_table = 'yj_shop_coupon_activity'
        verbose_name_plural = verbose_name = '店铺优惠券活动'


class ShopCouponActivityCoupon(TimeStampedModel):
    """
    店铺营销活动关联优惠券
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    # 优惠券模型
    coupon_id = models.CharField(verbose_name='优惠券id', blank=False, max_length=50)
    coupon_name = models.CharField(verbose_name='优惠券名称', blank=False, max_length=100)
    # 活动
    activity_id = models.CharField(verbose_name='活动id', blank=False, max_length=50)
    activity_name = models.CharField(verbose_name='活动名称', blank=False, max_length=100)

    class Meta:
        db_table = 'yj_shop_coupon_activity_coupon'
        verbose_name_plural = verbose_name = '店铺优惠券活动'


class ShopPin(TimeStampedModel):
    """
    拼团
    字段：谁（团长）、发起了拼团、拼团号是多少、开始时间，结束时间，成团状态
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    activity_id = models.CharField(verbose_name='拼团活动id', max_length=50, blank=True)
    activity_name = models.CharField(verbose_name='拼团活动名', max_length=250, blank=True)
    activity_code = models.CharField(verbose_name='唯一的活动编码', max_length=100, blank=True)
    required_num = models.IntegerField(verbose_name='需要的人数', default=5, help_text='成功成功所需次数')

    # 拼团号
    serial = models.CharField(verbose_name='拼团号', max_length=36, unique=True, help_text='10位数字', blank=True)

    # 所属店铺
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)

    # 发起人（团长）
    sponsor_id = models.CharField(verbose_name='发起人ID', max_length=50, blank=True)
    sponsor_name = models.CharField(verbose_name='发起人名称', max_length=100, blank=True)

    status = models.IntegerField(verbose_name='拼团状态', default=c.PIN_STATUS_ING, choices=c.PIN_STATUS_CHOICE)

    start_time = models.DateTimeField(verbose_name='开始时间', blank=True, null=True)
    expired_time = models.DateTimeField(verbose_name='过期时间', blank=True, null=True)

    class Meta:
        db_table = 'yj_shop_pin'
        verbose_name_plural = verbose_name = '拼团-拼团'


class ShopPinLog(TimeStampedModel):
    """
    字段：谁（团员）参与了哪一个拼团，拼团号是多少
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    activity_id = models.CharField(verbose_name='拼团活动id', max_length=50, blank=True)
    activity_name = models.CharField(verbose_name='拼团活动名', max_length=250, blank=True)
    serial = models.CharField(verbose_name='拼团号', max_length=36, blank=True, help_text='10位数字')

    # 拼团id
    pin_id = models.CharField(verbose_name='拼团id', max_length=50)

    # 所属店铺
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)

    # 参与人（团长）
    user_id = models.CharField(verbose_name='参与人ID', max_length=50)
    user_name = models.CharField(verbose_name='参与人名称', max_length=100, blank=True)
    user_avatar = models.CharField(verbose_name='头像', max_length=250, blank=True)
    is_sponsor = models.IntegerField(verbose_name='是否是团长', default=c.BOOL_TYPE_FALSE, choices=c.BOOL_TYPE_CHOICE)
    remark = models.CharField(verbose_name='备注', max_length=250, blank=True)

    class Meta:
        db_table = 'yj_shop_pin_log'
        verbose_name_plural = verbose_name = '拼团-拼团记录'


class ShopPinAwardRules(TimeStampedModel):
    """
    拼团奖励规则
    描述：
    字段：拼团成功后，团长获取什么奖励（优惠券）、团员获取什么奖励（优惠券）
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    activity_id = models.CharField(verbose_name='拼团活动id', max_length=50, blank=True)
    activity_name = models.CharField(verbose_name='拼团活动名', max_length=250, blank=True)
    coupon_id = models.CharField(verbose_name='优惠券id', max_length=50, blank=True)
    coupon_name = models.CharField(verbose_name='优惠券名', max_length=250, blank=True)

    # 所属店铺
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)
    award_type = models.IntegerField(verbose_name='领奖类型', default=c.PIN_AWARD_RULES_TYPE_ALL,
                                     choices=c.PIN_AWARD_RULES_TYPE_CHOICE, help_text='指定可领奖人')

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)

    class Meta:
        db_table = 'yj_shop_pin_award_rules'
        verbose_name_plural = verbose_name = '拼团-奖励规则'


class ShopPinAwardLog(TimeStampedModel):
    """
    拼团领奖记录
    字段：谁（团员）领取了哪一个拼团的奖励
    领取之后，还要创建一个优惠券记录（用户）
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    # 拼团id
    pin_id = models.CharField(verbose_name='拼团id', max_length=50)
    rule_id = models.CharField(verbose_name='奖励规则id', max_length=50)
    activity_id = models.CharField(verbose_name='拼团活动id', max_length=50, blank=True)
    activity_name = models.CharField(verbose_name='拼团活动名', max_length=250, blank=True)
    serial = models.CharField(verbose_name='拼团号', max_length=36, blank=True, help_text='10位数字')
    # 优惠券
    coupon_id = models.CharField(verbose_name='优惠券id', max_length=50)
    coupon_name = models.CharField(verbose_name='优惠券名', max_length=250, blank=True)
    coupon_value = models.FloatField(verbose_name='面额', default=0)
    # 所属店铺
    shop_id = models.CharField(verbose_name='店铺id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='店铺', max_length=100, blank=True)
    # 领奖人
    user_id = models.CharField(verbose_name='参与人ID', max_length=50)
    user_name = models.CharField(verbose_name='参与人名称', max_length=100, blank=True)
    remark = models.CharField(verbose_name='备注', max_length=250, blank=True)

    class Meta:
        db_table = 'yj_shop_pin_award_log'
        verbose_name_plural = verbose_name = '拼团-领奖记录'
