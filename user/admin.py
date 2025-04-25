from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.utils.safestring import mark_safe

from common.admin import BaseModelAdmin

from import_export import resources

from user import models


@admin.register(models.User)
class UserAdmin(BaseModelAdmin):
    """
    用户管理
    """
    list_display = ('id', 'phone', 'openid', 'mp_openid', 'unionid', 'avatar', 'name', 'session_key',
                    'gender', 'birthday', 'email', 'credit', 'status', 'last_login_time','created')
    list_filter = ('created',)
    search_fields = ('nickname', 'mobile')

    def avatar_img(self, obj):
        return mark_safe(
            '<a href="%s" target="_blank"><img src="%s" width="50px" height="50px" /></a>' % (obj.avatar, obj.avatar))


@admin.register(models.UserAddress)
class UserAddressAdmin(BaseModelAdmin):
    """
    用户收货地址管理
    """
    list_display = ('id', 'user_id', 'phone', 'name', 'province', 'city', 'district', 'address', 'default', 'created')
    list_filter = ('created',)
    search_fields = ('name', 'mobile')


@admin.register(models.CreditLog)
class CreditLogAdmin(BaseModelAdmin):
    """
    积分获取日志
    """
    search_fields = ('user_id', 'user_name', 'remark')
    list_display = ('id', 'user_name', 'credit', 'remain', 'remark', 'created',)
    list_filter = ('type', 'created')
    ordering = ('-created',)


@admin.register(models.Collection)
class ColllectionAdmin(BaseModelAdmin):
    """
    收藏记录
    """
    search_fields = ('user_id',)
    list_display = ('id', 'user_id', 'shop_id', 'shop_name', 'barber_id', 'barber_name',
                    'example_id', 'example_name', 'type',)
    list_filter = ('type', 'created')
    ordering = ('-created',)
