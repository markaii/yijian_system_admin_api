from rest_framework import serializers
from base import constants as c, models
from common.serializers import BaseModelSerializer


class UserSimpleSerializer(BaseModelSerializer):
    """
    用户简单序列化
    """
    department = serializers.SerializerMethodField()

    def get_department(self, obj):
        """用户所属的部门"""
        try:
            instance = models.Department.objects.get(id=obj.department_id)
            serializer = DepartmentSimpleSerializer(instance)
            return serializer.data
        except models.Department.DoesNotExist:
            return None

    class Meta:
        model = models.User
        fields = ('id', 'account', 'realname', 'code', 'department', 'avatar')


class UserSerializer(BaseModelSerializer):
    """
    用户序列化
    """

    class Meta:
        model = models.User
        fields = '__all__'
        ref_name = 'base_user_serializer'
        extra_kwargs = {
            'password': {'required': False},
            'token': {'read_only': True, 'required': False}
        }


class RoleSimpleSerializer(BaseModelSerializer):
    """
    角色简单序列化
    """

    class Meta:
        model = models.Role
        fields = ('id', 'name', 'code')


class RoleSerializer(BaseModelSerializer):
    """
    角色序列化
    """
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        qs = models.UserRole.objects.filter(role_id=obj.id)
        res = []
        for obj in qs:
            user = models.User.objects.get(id=obj.user_id)
            serializer = UserSimpleSerializer(user)
            res.append(serializer.data)
        return res

    class Meta:
        model = models.Role
        fields = '__all__'


class UserRoleSerializer(BaseModelSerializer):
    """
    用户角色序列化
    """

    class Meta:
        model = models.UserRole
        fields = '__all__'


class DepartmentSimpleSerializer(BaseModelSerializer):
    """
    部门简单序列化
    """

    class Meta:
        model = models.Department
        fields = ('id', 'name', 'code')


class DepartmentTreeSerializer(BaseModelSerializer):
    """部门树形结构序列化"""
    company = serializers.SerializerMethodField()

    def get_company(self, obj):
        try:
            instance = models.Company.objects.get(id=obj.company_id)
            serializer = CompanySimpleSerializer(instance)
            return serializer.data
        except models.Company.DoesNotExist:
            return None

    class Meta:
        model = models.Company
        fields = ('id', 'name', 'code', 'short_name', 'company')


class DepartmentSerializer(BaseModelSerializer):
    """
    组织构架 - 部门序列化
    """
    child_department = serializers.SerializerMethodField()  # 子部门

    def get_child_department(self, obj):
        try:
            instance = models.Department.objects.filter(parent_id=obj.id)
            serializer = DepartmentSimpleSerializer(instance, many=True)
            return serializer.data
        except models.Department.DoesNotExist:
            return None

    class Meta:
        model = models.Department
        fields = '__all__'


class CompanySimpleSerializer(BaseModelSerializer):
    """
    公司简单序列化
    """

    class Meta:
        model = models.Company
        fields = ('id', 'name', 'code')


class CompanySerializer(BaseModelSerializer):
    """
    组织构架 - 公司序列化
    """
    departments = serializers.SerializerMethodField()

    def get_departments(self, obj):
        qs = models.Department.objects.filter(company_id=obj.id)
        serializer = DepartmentSimpleSerializer(qs, many=True)
        return serializer.data

    class Meta:
        model = models.Company
        fields = '__all__'


class CompanyTreeSerializer(BaseModelSerializer):
    """
    公司树形结构序列化
    """
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        """
        获取子公司结构
        :param obj:
        :return:
        """
        qs = models.Company.objects.filter(parent_id=obj.id)
        serializer = CompanyTreeSerializer(qs, many=True)
        return serializer.data

    class Meta:
        model = models.Company
        fields = ('id', 'name', 'code', 'short_name', 'children')


class PostSimpleSerializer(BaseModelSerializer):
    """
    职位简单序列化
    """

    class Meta:
        model = models.Post
        fields = ('id', 'name', 'code')


class PostSerializer(BaseModelSerializer):
    """
    组织架构 - 职位序列化
    """

    member = serializers.SerializerMethodField()

    def get_member(self, obj):
        """
        当前岗位的所有成员信息
        """
        post_qs = models.UserPost.objects.filter(post_id=obj.id)
        for post in post_qs:
            qs = models.User.objects.filter(id=post.user_id)
            serializer = UserSimpleSerializer(qs, many=True)
            return serializer.data

    class Meta:
        model = models.Post
        fields = '__all__'


class ModuleSimpleSerializer(BaseModelSerializer):
    """
    模块简单序列化
    """

    class Meta:
        model = models.Module
        fields = ('id', 'name', 'code')


class ModuleSerializer(BaseModelSerializer):
    """
    模块序列化
    """

    class Meta:
        model = models.Module
        fields = '__all__'


class ModuleTreeSerializer(BaseModelSerializer):
    """
    模块树形结构序列化
    """
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        """
        获取子数据字典结构
        :param obj:
        :return:
        """
        qs = models.Module.objects.filter(parent_id=obj.id).order_by("sort")
        serializer = ModuleTreeSerializer(qs, many=True)
        return serializer.data

    class Meta:
        model = models.Module
        fields = ('id', 'name', 'code', 'parent_id', 'children')


class ModuleButtonTreeSerializer(ModuleTreeSerializer):
    """
    模块按钮树形结构序列化
    """
    children = serializers.SerializerMethodField()
    buttons = serializers.SerializerMethodField()

    def get_children(self, obj):
        """
        获取子数据字典结构
        :param obj:
        :return:
        """
        qs = models.Module.objects.filter(parent_id=obj.id)
        serializer = ModuleButtonTreeSerializer(qs, many=True)
        return serializer.data

    def get_buttons(self, obj):
        """
        获取按钮列表
        :param obj:
        :return:
        """
        qs = models.ModuleButton.objects.filter(module_id=obj.id)
        serializer = ModuleButtonSimpleSerializer(qs, many=True)
        return serializer.data

    class Meta:
        model = models.Module
        fields = ('id', 'name', 'code', 'parent_id', 'children', 'buttons')


class ModuleColumnTreeSerializer(BaseModelSerializer):
    """
    模块列表（字段）树形结构序列化
    """
    children = serializers.SerializerMethodField()
    columns = serializers.SerializerMethodField()

    def get_children(self, obj):
        """
        获取子数据字典结构
        :param obj:
        :return:
        """
        qs = models.Module.objects.filter(parent_id=obj.id)
        serializer = ModuleColumnTreeSerializer(qs, many=True)
        return serializer.data

    def get_columns(self, obj):
        """
        获取模块列表（字段）
        :param obj:
        :return:
        """
        qs = models.ModuleColumn.objects.filter(module_id=obj.id)
        serializer = ModuleColumnSimpleSerializer(qs, many=True)
        return serializer.data

    class Meta:
        model = models.Module
        fields = ('id', 'name', 'code', 'parent_id', 'children', 'columns')


class ModuleFormTreeSerializer(BaseModelSerializer):
    """
    模块表单（字段）树形结构序列化
    """
    children = serializers.SerializerMethodField()
    forms = serializers.SerializerMethodField()

    def get_children(self, obj):
        """
        获取子数据字典结构
        :param obj:
        :return:
        """
        qs = models.Module.objects.filter(parent_id=obj.id)
        serializer = ModuleFormTreeSerializer(qs, many=True)
        return serializer.data

    def get_forms(self, obj):
        """
        获取模块列表（字段）
        :param obj:
        :return:
        """
        qs = models.ModuleForm.objects.filter(module_id=obj.id)
        serializer = ModuleFormSimpleSerializer(qs, many=True)
        return serializer.data

    class Meta:
        model = models.Module
        fields = ('id', 'name', 'code', 'parent_id', 'children', 'forms')


class ModuleButtonSimpleSerializer(BaseModelSerializer):
    """
    按钮简单序列化
    """

    class Meta:
        model = models.ModuleButton
        fields = ('id', 'name', 'code')


class ModuleButtonSerializer(BaseModelSerializer):
    """
    按钮序列化
    """

    class Meta:
        model = models.ModuleButton
        fields = '__all__'


class ModuleColumnSimpleSerializer(BaseModelSerializer):
    """
    列表简单序列化
    """

    class Meta:
        model = models.ModuleColumn
        fields = ('id', 'name', 'code')


class ModuleColumnSerializer(BaseModelSerializer):
    """
    模块列表序列化
    """

    class Meta:
        model = models.ModuleColumn
        fields = '__all__'


class ModuleFormSimpleSerializer(BaseModelSerializer):
    """
    表单简单序列化
    """

    class Meta:
        model = models.ModuleForm
        fields = ('id', 'name', 'code')


class ModuleFormSerializer(BaseModelSerializer):
    """
    表单序列化
    """

    class Meta:
        model = models.ModuleForm
        fields = '__all__'


class DataDictSerializer(BaseModelSerializer):
    """
    数据字典序列化
    """

    class Meta:
        model = models.DataDict
        fields = ('id', 'name', 'code', 'remark', 'sort', 'enable', 'parent_id')


class DataDictTreeSerializer(BaseModelSerializer):
    """
    数据字典树形结构序列化
    """
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        """
        获取子数据字典结构
        :param obj:
        :return:
        """
        qs = models.DataDict.objects.filter(parent_id=obj.id)
        serializer = DataDictTreeSerializer(qs, many=True)
        return serializer.data

    class Meta:
        model = models.DataDict
        fields = ('id', 'name', 'code', 'remark', 'sort', 'enable', 'parent_id', 'children')


class DataDictItemSerializer(BaseModelSerializer):
    """
       数据字典详情序列化
    """

    class Meta:
        model = models.DataDictItem
        fields = '__all__'


class AuthorizeSerializer(BaseModelSerializer):
    """
    功能权限授权序列化
    """

    item = serializers.SerializerMethodField()

    def get_item(self, obj):
        """
        获取item实例，分4种类型
        :param obj:
        :return:
        """
        if obj.item_type == c.AUTHORIZE_ITEM_TYPE_MODULE:
            try:
                instance = models.Module.objects.get(id=obj.item_id)
                print(instance)
                serializer = ModuleSimpleSerializer(instance)
                return serializer.data
            except models.Module.DoesNotExist:
                return None
        elif obj.item_type == c.AUTHORIZE_ITEM_TYPE_BUTTON:
            try:
                instance = models.ModuleButton.objects.get(id=obj.item_id)
                serializer = ModuleButtonSimpleSerializer(instance)
                return serializer.data
            except models.ModuleButton.DoesNotExist:
                return None
        elif obj.item_type == c.AUTHORIZE_ITEM_TYPE_VIEW:
            try:
                instance = models.ModuleColumn.objects.get(id=obj.item_id)
                serializer = ModuleColumnSimpleSerializer(instance)
                return serializer.data
            except models.ModuleColumn.DoesNotExist:
                return None
        elif obj.item_type == c.AUTHORIZE_ITEM_TYPE_FORM:
            try:
                instance = models.ModuleForm.objects.get(id=obj.item_id)
                serializer = ModuleFormSimpleSerializer(instance)
                return serializer.data
            except models.ModuleForm.DoesNotExist:
                return None
        else:
            return None

    class Meta:
        model = models.Authorize
        fields = ('object_type', 'object_id', 'item_type', 'item_id', 'item',)


class LogSerializer(BaseModelSerializer):
    """
    系统日志序列化
    """
    operate_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True,
                                             allow_null=True)

    class Meta:
        model = models.Log
        fields = '__all__'
