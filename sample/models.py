from django.db import models
from model_utils.models import TimeStampedModel
from uuid import uuid4

from sample import constants as c


class SampleTag(TimeStampedModel):
    """
    作品标签
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    name = models.CharField(verbose_name='标签名', max_length=256, blank=True)
    count = models.IntegerField(verbose_name='关联作品数', default=0)
    sort = models.IntegerField(verbose_name='排序码', default=0, help_text='升序排序')

    class Meta:
        db_table = 'yj_sample_tag'
        verbose_name = '作品文件模型'
        verbose_name_plural = verbose_name


class Sample(TimeStampedModel):
    """
    作品
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)

    title = models.CharField(verbose_name='作品标题', max_length=100)
    description = models.TextField(verbose_name='作品描述', blank=True)

    barber_id = models.CharField(verbose_name='理发师id', max_length=50, blank=True)
    barber_name = models.CharField(verbose_name='理发师名字', max_length=128, blank=True)
    barber_avatar = models.CharField(verbose_name='理发师头像', max_length=255, blank=True)

    shop_id = models.CharField(verbose_name='门店id', max_length=50, blank=True)
    shop_name = models.CharField(verbose_name='门店名字', max_length=128, blank=True)

    # 消费者信息（后面做消费者上传时用）
    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)
    user_name = models.CharField(verbose_name='姓名', max_length=255, blank=True)

    tags = models.CharField(verbose_name='作品标签集', max_length=512, blank=True, help_text='多个标签以,分隔')

    source = models.IntegerField(verbose_name='来源', default=c.SAMPLE_SOURCE_SYSTEM,
                                 choices=c.SAMPLE_SOURCE_CHOICE, help_text='系统上传，理发师上传，用户上传')
    like_count = models.IntegerField(verbose_name='收藏/点赞数量', default=0)

    sort = models.IntegerField(verbose_name='排序值', default=0, help_text='升序排序')
    status = models.IntegerField(verbose_name='状态', choices=c.STATUS_CHOICE, default=c.STATUS_NORMAL)
    type = models.IntegerField(verbose_name='状态', choices=c.SAMPLE_TYPE_CHOICE, default=c.SAMPLE_TYPE_FEMALE)
    is_hide = models.IntegerField(verbose_name='是否隐藏', choices=c.BOOL_TYPE_CHOICE, default=c.BOOL_TYPE_FALSE)

    class Meta:
        db_table = 'yj_sample'
        verbose_name = '作品模型'
        verbose_name_plural = verbose_name


class SampleFile(TimeStampedModel):
    """
    作品集文件
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    sample_id = models.CharField(verbose_name='作品id', max_length=50)
    file = models.CharField(verbose_name='文件地址', max_length=256, blank=True)
    type = models.IntegerField(verbose_name='文件类型', default=c.FILE_TYPE_IMG, choices=c.FILE_TYPE_CHOICE)
    sort = models.IntegerField(verbose_name='排序码', default=0, help_text='升序排序')

    # 冗余存储视频头图字段
    poster = models.CharField(verbose_name='视频头图', max_length=255, blank=True)

    class Meta:
        db_table = 'yj_sample_file'
        verbose_name = '作品文件模型'
        verbose_name_plural = verbose_name


class SampleReport(TimeStampedModel):
    """
    作品举报
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)

    # 作品
    sample_id = models.CharField(verbose_name='作品id', max_length=50)
    sample_title = models.CharField(verbose_name='作品标题', max_length=100, blank=True)

    # 举报人
    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)
    user_name = models.CharField(verbose_name='姓名', max_length=255, blank=True)

    status = models.IntegerField(verbose_name='状态', default=c.SAMPLE_REPORT_STATUS_WAITING,
                                 choices=c.SAMPLE_REPORT_STATUS_CHOICE)

    phone = models.CharField(verbose_name='手机号', max_length=64, blank=True)
    description = models.TextField(verbose_name='举报描述', blank=True)

    class Meta:
        db_table = 'yj_sample_report'
        verbose_name = '作品举报'
        verbose_name_plural = verbose_name


class SampleReportFile(TimeStampedModel):
    """
    举报文件
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    report_id = models.CharField(verbose_name='作品id', max_length=50)
    file = models.CharField(verbose_name='文件地址', max_length=256, blank=True)

    class Meta:
        db_table = 'yj_sample_report_file'
        verbose_name = '举报文件模型'
        verbose_name_plural = verbose_name


class HairChangeLog(TimeStampedModel):
    """
    变更发型记录（使用换发型功能时创建）
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    # 操作人
    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)
    user_name = models.CharField(verbose_name='姓名', max_length=255, blank=True)
    original_image = models.CharField(verbose_name='原图片URL', max_length=255, blank=True)
    hair_image = models.CharField(verbose_name='发型图片URL', max_length=255, blank=True)
    new_image = models.CharField(verbose_name='合成后的图片URL', max_length=255, blank=True)

    class Meta:
        db_table = 'yj_sample_hair_change_log'
        verbose_name = '变更发型记录'
        verbose_name_plural = verbose_name


class HairColorChangeLog(TimeStampedModel):
    """
    变更发色记录（使用换发色功能时创建）
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    # 操作人
    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)
    user_name = models.CharField(verbose_name='姓名', max_length=255, blank=True)
    original_image = models.CharField(verbose_name='原图片URL', max_length=255, blank=True)
    new_image = models.CharField(verbose_name='合成后的图片URL', max_length=255, blank=True)
    color = models.CharField(verbose_name='颜色', max_length=50, blank=True)

    class Meta:
        db_table = 'yj_sample_hair_color_change_log'
        verbose_name = '变更发色记录'
        verbose_name_plural = verbose_name
