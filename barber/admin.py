from django.contrib import admin
from common.admin import BaseModelAdmin
from barber import models


@admin.register(models.Barber)
class BarberAdmin(BaseModelAdmin):
    """
    理发师账号后台管理
    """
    list_display = ('phone', 'name', 'password', 'salt', 'shop_id', 'shop_name', 'gender', 'avatar', 'work_year',
                    'title', 'score', 'business_status')
    search_fields = ('phone', 'name',)
    list_filter = ('shop_id',)


@admin.register(models.Example)
class ExampleAdmin(BaseModelAdmin):
    """
    作品后台管理
    """
    list_display = ('title', 'description', 'barber_id', 'barber_name', 'shop_id', 'shop_name', 'sort')
    search_fields = ('title',)


@admin.register(models.ExampleFile)
class ExampleFileAdmin(BaseModelAdmin):
    """
    作品文件后台管理
    """
    list_display = ('example_id', 'file', 'type', 'sort')
    search_fields = ('example_id',)


@admin.register(models.Service)
class ServiceAdmin(BaseModelAdmin):
    """
    服务项目后台管理
    """
    list_display = ('name', 'intro', 'duration', 'barber_id', 'barber_name', 'price', 'min_price', 'max_price',
                    'price_type')
    search_fields = ('name',)


@admin.register(models.SystemService)
class SystemServiceAdmin(BaseModelAdmin):
    """
    系统服务项目后台管理
    """
    list_display = ('name', 'intro', 'create_user_id', 'create_user_name', 'modify_user_id', 'modify_user_name')
    search_fields = ('name',)
