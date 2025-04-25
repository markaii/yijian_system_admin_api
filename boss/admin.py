from django.contrib import admin
from common.admin import BaseModelAdmin
from boss import models


@admin.register(models.Boss)
class BossAdmin(BaseModelAdmin):
    """
    老板账号后台管理
    """
    list_display = ('phone', 'name', 'password', 'salt', 'gender','avatar','shop_id','shop_name')
    search_fields = ('phone', 'name',)
    list_filter = ('shop_id',)

