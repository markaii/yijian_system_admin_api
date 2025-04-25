from django.contrib import admin
from shop import models
from common.admin import BaseModelAdmin


@admin.register(models.Shop)
class ShopAdmin(BaseModelAdmin):
    """
    店铺后台管理
    """
    list_display = ('name', 'phone', 'image', 'license', 'score', 'open_time', 'close_time', 'days',
                    'business_status', 'province', 'province_code', 'city', 'city_code', 'district',
                    'district_code', 'address', 'longitude', 'latitude', 'status')
    search_fields = ('name',)


@admin.register(models.ShopFile)
class ShopFileAdmin(BaseModelAdmin):
    """
    店铺文件后台管理
    """
    list_display = ('shop_id', 'shop_name', 'file', 'type', 'sort')
    search_fields = ('shop_id',)
