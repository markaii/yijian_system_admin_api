from django.contrib import admin
from common.admin import BaseModelAdmin
from activity import models


# Register your models here.

@admin.register(models.Banner)
class SystemServiceAdmin(BaseModelAdmin):
    """
    系统服务项目后台管理
    """
    list_display = (
        'name', 'cover', 'jump_path', 'jump_type', 'position', 'status', 'applet_type', 'remark', 'sort','create_user_id',
        'create_user_name', 'modify_user_id', 'modify_user_name', 'enable', 'deleted',)
    search_fields = ('name', 'jump_type', 'status', 'applet_type',)
