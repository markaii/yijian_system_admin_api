from django.contrib import admin
from common.admin import BaseModelAdmin
from task import models


# Register your models here.
# @admin.register(models.ShopCollectTask)
# class ShopFileAdmin(BaseModelAdmin):
#     """
#     采集店铺信息后台管理
#     """
#     list_display = ('name', 'execute_time', 'province', 'city', 'district', 'address', 'status',)
#     list_filter = ('status',)
