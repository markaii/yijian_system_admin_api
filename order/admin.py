from django.contrib import admin
from order import models
from common.admin import BaseModelAdmin


@admin.register(models.Order)
class OrderAdmin(BaseModelAdmin):
    """
    订单后台管理
    """
    list_display = ('serial', 'user_id', 'user_name', 'user_phone', 'barber_id', 'barber_name', 'shop_id', 'shop_name',
                    'service_id', 'service_name', 'price', 'min_price', 'max_price', 'price_type',
                    'status', 'remark',)
    search_fields = ('serial',)
    list_filter = ('price_type', 'status',)


@admin.register(models.Comment)
class CommentAdmin(BaseModelAdmin):
    """
    评论后台管理
    """
    list_display = (
        'order_id', 'user_id', 'user_name', 'barber_id', 'barber_name', 'shop_id', 'shop_name', 'score', 'content')
    search_fields = ('order_id', 'user_id', 'barber_id', 'shop_id',)
    list_filter = ('score',)


@admin.register(models.CommentFile)
class CommentFileAdmin(BaseModelAdmin):
    """
    评论文件后台管理
    """
    list_display = ('comment_id', 'file', 'type', 'sort')
    search_fields = ('comment_id',)


@admin.register(models.CommentTag)
class CommentTagAdmin(BaseModelAdmin):
    """
    评论标签后台管理
    """
    list_display = ('comment_id', 'text')
    search_fields = ('comment_id',)
