from django.db import models
from model_utils.models import TimeStampedModel
import uuid
from help import constants as c


class HelpArticle(TimeStampedModel):
    """
    帮助中心文章
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    status = models.IntegerField(verbose_name="状态", default=c.STATUS_NORMAL, choices=c.STATUS_CHOICE)
    category_id = models.CharField(verbose_name='分类ID', max_length=50)
    category_name = models.CharField(verbose_name='分类名称', max_length=64, blank=True)
    # 判断是商户端还是小程序端的文章
    applet_type = models.IntegerField(verbose_name='小程序类型', default=c.BANNER_APPLET_TYPE_MERCHANT,
                                      choices=c.BANNER_APPLET_TYPE_CHOICE)

    title = models.CharField(verbose_name='文章标题', max_length=100)
    content = models.TextField(verbose_name='内容', blank=True)

    # 控制字段
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        db_table = 'yj_help_article'
        verbose_name_plural = verbose_name = '帮助中心-帮助文章'
        app_label = 'marketing'


class HelpCategory(TimeStampedModel):
    """
    文章分类
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='名称', max_length=64, help_text='分类名称')
    type = models.IntegerField(verbose_name='反馈类型', default=c.FEEDBACK_TYPE_ADVICE, choices=c.FEEDBACK_TYPE_HELP)

    # merchant_id = models.CharField(verbose_name='关联商户id', max_length=50, blank=True)
    # app_id = models.CharField(verbose_name='应用id', max_length=50, blank=True)
    # app_name = models.CharField(verbose_name='应用名称', max_length=50, blank=True)

    # 控制字段
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        db_table = 'yj_help_category'
        verbose_name_plural = verbose_name = '帮助中心-帮助分类'
        app_label = 'marketing'


class HelpFeedback(TimeStampedModel):
    """
    反馈模型
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name="标题", max_length=100, blank=True)
    user_id = models.CharField(verbose_name='用户ID', max_length=50)
    user_name = models.CharField(verbose_name='用户名字', max_length=100, blank=True)
    phone = models.CharField(verbose_name='电话', max_length=64)
    content = models.CharField(verbose_name="内容", max_length=255)
    category_id = models.CharField(verbose_name='分类ID', max_length=50)
    category_name = models.CharField(verbose_name='分类名称', max_length=100, blank=True)
    rank = models.IntegerField(verbose_name="评价打分", choices=c.FEEDBACK_RANK_CHOICE, null=True, blank=True)
    status = models.IntegerField(verbose_name="状态", default=c.FEEDBACK_STATUS_WAITING, choices=c.FEEDBACK_STATUS_CHOICE)
    type = models.IntegerField(verbose_name='反馈类型', default=c.FEEDBACK_TYPE_ADVICE, choices=c.FEEDBACK_TYPE_HELP)
    comment = models.CharField(verbose_name='评价内容', max_length=255, blank=True)
    # 判断是商户端还是小程序端的文章
    applet_type = models.IntegerField(verbose_name='小程序类型', default=c.BANNER_APPLET_TYPE_MERCHANT,
                                      choices=c.BANNER_APPLET_TYPE_CHOICE)

    # 控制字段
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        db_table = 'yj_help_feedback'
        verbose_name_plural = verbose_name = '帮助中心-问题反馈'
        app_label = 'marketing'


class HelpFeedbackAttachment(TimeStampedModel):
    """反馈附件"""
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    feedback_id = models.CharField(verbose_name='反馈id', max_length=50, blank=True)
    feedback_title = models.CharField(verbose_name="标题", max_length=100, blank=True)
    file_url = models.CharField(verbose_name='文件地址', max_length=255, blank=True)

    class Meta:
        db_table = 'yj_help_feedback_attachment'
        verbose_name_plural = verbose_name = '帮助中心-反馈附件'
        app_label = 'marketing'


class HelpFeedbackComment(TimeStampedModel):
    """问题回复"""
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    user_id = models.CharField(verbose_name='用户ID', max_length=50, blank=True)
    user_name = models.CharField(verbose_name='用户名', max_length=100, blank=True)
    user_avatar = models.CharField(verbose_name='用户头像', max_length=255, blank=True)
    user_type = models.IntegerField(verbose_name='用户类型', default=c.FEEDBACK_COMMENT_USER_TYPE_CUSTOMER,
                                    choices=c.FEEDBACK_COMMENT_USER_TYPE_CHOICE)
    feedback_id = models.CharField(verbose_name='反馈id', max_length=50, blank=True)
    feedback_title = models.CharField(verbose_name="标题", max_length=100, blank=True)
    comment = models.CharField(verbose_name='评论内容', max_length=255, blank=True)

    class Meta:
        db_table = 'yj_help_feedback_comment'
        verbose_name_plural = verbose_name = '帮助中心-问题回复'
        app_label = 'marketing'
