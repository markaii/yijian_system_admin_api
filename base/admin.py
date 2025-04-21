from django.contrib import admin
from common.admin import BaseModelAdmin

from base import models
from import_export.admin import ImportExportModelAdmin
from import_export import resources


@admin.register(models.User)
class UserAdmin(BaseModelAdmin):
    """
    用户
    """
    list_display = ('id', 'account', 'password', 'salt', 'token', 'company_id', 'department_id', 'is_superuser')
    search_fields = ('account', 'company_id', 'department_id')
    list_filter = ('is_superuser', 'enable', 'deleted')


@admin.register(models.Role)
class RoleAdmin(BaseModelAdmin):
    """
    角色
    """
    list_display = ('id', 'name', 'code', 'sort', 'remark', 'create_user_id', 'create_user_name', 'modify_user_id',
                    'modify_user_name', 'enable', 'deleted',
                    )
    search_fields = ('name', 'code',)
    list_filter = ('enable', 'deleted')


# @admin.register(models.UserRole)
# class UserRoleAdmin(BaseModelAdmin):
#         """
#         用户角色
#         """
#         list_display = ('user', 'role', 'create_user_id', 'create_user_name',)
#         search_fields = ('user', 'role',)
#         list_filter = ('user', 'user',)

class CompanyResource(resources.ModelResource):
    """
    公司导入数据源
    """

    class Meta:

        model = models.Company
        fields = ('id', 'parent_id', 'name', 'short_name', 'code', 'ou_code', 'parent_ou_code', 'ou_level')


@admin.register(models.Company)
class CompanyAdmin(ImportExportModelAdmin):
    """
    组织构架 - 公司
    """
    list_display = ('id', 'name', 'code', 'short_name', 'phone', 'fax', 'email',
                    'manager', 'parent_id', 'province', 'province_code', 'city',
                    )
    search_fields = ('id', 'name', 'code', 'parent_id')
    list_filter = ('enable', 'deleted')
    resource_class = CompanyResource


@admin.register(models.Department)
class DepartmentAdmin(BaseModelAdmin):
    """
    组织构架 - 部门
    """
    list_display = ('id', 'name', 'code', 'phone', 'short_name', 'fax', 'email',
                    'address', 'manager', 'parent_id', 'company_id',)
    search_fields = ('name', 'code', 'parent_id', 'company_id')
    list_filter = ('enable', 'deleted',)


@admin.register(models.Post)
class PostAdmin(BaseModelAdmin):
    """
        组织架构 - 职位
        """
    list_display = ('id', 'name', 'parent_id', 'code', 'company_id', 'department_id', 'remark',
                    'sort', 'create_user_id', 'create_user_name', 'modify_user_id',)
    search_fields = ('name', 'parent_id', 'company_id', 'department_id')
    list_filter = ('enable', 'deleted')


@admin.register(models.Module)
class ModuleAdmin(BaseModelAdmin):
    """
         系统模块
        """
    list_display = ('id', 'name', 'code', 'icon', 'url', 'parent_id', 'is_menu',
                    'remark', 'sort',)
    search_fields = ('name', 'parent_id', 'code', 'url')
    list_filter = ('enable', 'deleted')


@admin.register(models.ModuleButton)
class ModuleButtonAdmin(BaseModelAdmin):
    """
         模块按钮
        """
    list_display = ('id', 'module_id', 'parent_id', 'name', 'icon', 'code', 'remark', 'sort',)
    search_fields = ('name', 'parent_id', 'code', 'module_id')
    list_filter = ('enable', 'deleted')


@admin.register(models.ModuleColumn)
class ModuleColumnAdmin(BaseModelAdmin):
    """
         模块列表视图
        """
    list_display = ('id', 'module_id', 'name', 'code', 'sort',)
    search_fields = ('name', 'code', 'module_id')
    list_filter = ('enable', 'deleted')


@admin.register(models.ModuleForm)
class ModuleFormAdmin(BaseModelAdmin):
    """
         模块表单视图
        """
    list_display = ('id', 'module_id', 'name', 'code', 'sort',)
    list_filter = ('name', 'code',)


@admin.register(models.Authorize)
class AuthorizeAdmin(BaseModelAdmin):
    """
         权限授权
        """
    list_display = ('object_type', 'object_id', 'item_type', 'item_id',)
    search_fields = ('object_id', 'item_id', 'code')
    list_filter = ('object_type', 'item_type', 'enable', 'deleted')


@admin.register(models.Log)
class LogAdmin(BaseModelAdmin):
    """
         系统日志
        """
    list_display = ('id', 'type', 'module_name', 'operate_user_id', 'operate_user', 'operate_time',
                    'operate_type', 'ip_address', 'ip_address_name', 'host', 'browser',
                    )
    search_fields = ('module_name', 'ip_address')
    list_filter = ('type', 'result_type', 'deleted')


@admin.register(models.IPBlackList)
class IPBlackListAdmin(BaseModelAdmin):
    """
         IP黑名单
        """
    list_display = ('start_ip', 'end_ip', 'description', 'sort',)
    search_fields = ('start_ip', 'end_ip',)
    list_filter = ('enable', 'deleted')


@admin.register(models.DataDict)
class DataDictAdmin(BaseModelAdmin):
    """
         数据字典
        """
    list_display = ('parent_id', 'name', 'code', 'remark', 'sort')
    search_fields = ('name', 'parent_id', 'code')
    list_filter = ('enable', 'deleted')


@admin.register(models.DataDictItem)
class DataDictItemAdmin(BaseModelAdmin):
    """
         数据字典详情
        """
    list_display = ('data_dict_id', 'parent_id', 'name', 'value', 'code', 'remark', 'sort')
    search_fields = ('data_dict_id', 'parent_id', 'code', 'name')
    list_filter = ('enable', 'deleted')
