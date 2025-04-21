import uuid
from django.db import models
from model_utils.models import TimeStampedModel
from article import constants as c


class ArticleCategory(TimeStampedModel):
    """
    文章分类
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    status = models.IntegerField(verbose_name="状态", default=c.STATUS_NORMAL, choices=c.STATUS_CHOICE)
    name = models.CharField(verbose_name='名称', max_length=100, blank=True)

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        db_table = 'yj_article_category'
        verbose_name_plural = verbose_name = '文章分类'


class Article(TimeStampedModel):
    """
    文章
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    author_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)
    author_name = models.CharField(verbose_name='用户名', max_length=100, blank=True)
    category_id = models.CharField(verbose_name='类别id', max_length=50, blank=True)
    category_name = models.CharField(verbose_name='类别名', max_length=100, blank=True)
    # 文章内容
    title = models.CharField(verbose_name='文章标题', max_length=255, blank=True)
    content = models.TextField(verbose_name='内容', blank=True, help_text='富文本')

    publish_date = models.DateTimeField(verbose_name='发布日期', null=True, blank=True)
    status = models.IntegerField(verbose_name='状态', default=c.ARTICLE_STATUS_WAITING,
                                 choices=c.ARTICLE_STATUS_CHOICE)

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        db_table = 'yj_article'
        verbose_name_plural = verbose_name = '文章'
