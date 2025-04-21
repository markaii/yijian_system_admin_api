import datetime
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework import status, views
from rest_framework.decorators import action

from base import authentication
from base import services, constants as c, forms, permissions, serializers, models

from common.response import JsonResponse
from common.viewsets import BaseViewSet
from common.exceptions import ServerError

from django.db.models import Q
from django_filters import rest_framework as filters
from datetime import datetime, timedelta


class UserViewSet(BaseViewSet):
    """
    用户接口
    """
    queryset = models.User.objects.filter()
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    search_fields = ('realname', 'nickname', 'code')
    filter_fields = ('department_id', 'company_id')
    ordering_fields = ('created',)
    ordering = ('-created',)

    def perform_create(self, serializer):
        salt = services._generate_random_str(10)
        password = 'shuyun'
        encrypt_password = services.encrypt_password(salt, password)
        user = serializer.save(salt=salt, password=encrypt_password)
        services.generate_user_token(user)

    @action(detail=False, methods=['post'], authentication_classes=[authentication.DummyAuthentication],
            permission_classes=(permissions.permissions.AllowAny,))
    def login(self, request):
        """
        登录接口
        :param request:
        :return:
        """
        # 1、获取参数
        form = forms.LoginForm(request.data)
        if not form.is_valid():
            # 不是有效数据
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        data = form.cleaned_data
        # 2、登录
        resp, code_or_user = services.login(data['account'], data['password'])
        # 3.创建登录日志
        meta = self.request.META
        if code_or_user != c.ERROR_PHONE_UNREGISTERED:
            services.login_log(data['account'], meta, resp, code_or_user)

        if not resp:
            return JsonResponse(message=c.ERROR_CHOICE[code_or_user], code=code_or_user)
        # 3、检查是否禁用
        if code_or_user.enable != c.ENABLE_TYPE_NORMAL:
            return JsonResponse(message=c.ERROR_CHOICE[c.ERROR_ACCOUNT_DISABLED], code=c.ERROR_ACCOUNT_DISABLED)

        user_serializer = self.get_serializer(code_or_user)
        return JsonResponse(data=user_serializer.data, code=c.API_MESSAGE_OK, message='ok')

    @action(detail=False, methods=['post'])
    def check_password(self, request):
        """
        检查当前密码接口
        :param request:
        :return:
        """
        # 1、获取参数
        form = forms.PasswordForm(request.data)
        if not form.is_valid():
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        data = form.cleaned_data
        resp = services.check_user_password(request.user, data['password'])
        if not resp:
            # 原来的密码错误
            return JsonResponse(message=c.ERROR_CHOICE[c.ERROR_ACCOUNT_PASSWORD_ERROR],
                                code=c.ERROR_ACCOUNT_PASSWORD_ERROR)
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok')

    @action(detail=False, methods=['post'])
    def modify_password(self, request):
        """
        修改用户自身密码
        :param request:
        :return:
        """
        # 1、获取参数
        form = forms.ModifyPasswordForm(request.data)
        if not form.is_valid():
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        data = form.cleaned_data
        # 2、修改密码
        resp, code_or_user = services.modify_password(request.user, data['new_password'])
        if not resp:
            # 原来的密码错误
            return JsonResponse(message=c.ERROR_CHOICE[code_or_user], code=code_or_user)
        user_serializer = self.get_serializer(code_or_user)
        return JsonResponse(data=user_serializer.data, code=c.API_MESSAGE_OK, message='ok')

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        """
        重置密码接口(管理员可以对其他人员重置密码)
        """
        form = forms.ResetPasswordForm(request.data)
        if not form.is_valid():
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        data = form.cleaned_data

        # 2、修改密码
        resp, code_or_user = services.reset_password(data["user_id"], data['password'])
        user_serializer = self.get_serializer(code_or_user)
        return JsonResponse(data=user_serializer.data, code=c.API_MESSAGE_OK, message='ok')

    @action(detail=False, methods=['get'])
    def info(self, request):
        """
        获取用户自身信息
        :param request:
        :return:
        """
        user_serializer = self.get_serializer(request.user)
        return JsonResponse(data=user_serializer.data, code=c.API_MESSAGE_OK, message='ok')

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        """
        禁用指定的用户接口
        禁用后无登陆权限
        TODO 考虑权限问题，目前应该是前端根据用户按钮权限控制
        :param request:
        :return:
        """
        try:
            user = models.User.objects.get(pk)
            user.enable = c.ENABLE_TYPE_ABNORMAL
            user.save()
        except models.User.DoesNotExist:
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok')

    @action(detail=True, methods=['post'])
    def enable(self, request, pk):
        """
        启动指定的用户接口
        考虑权限问题，目前应该是前端根据用户按钮权限控制
        :param request:
        :return:
        """
        try:
            user = models.User.objects.get(pk)
            user.enable = c.ENABLE_TYPE_NORMAL
            user.save()
        except models.User.DoesNotExist:
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok')

    @action(detail=False, methods=['post'])
    def authorize(self, request):
        """
        用户功能授权接口
        """
        data = request.data
        resp = services.user_authorize(data["user_id"], data)
        if resp:
            return JsonResponse(code=c.API_MESSAGE_OK, message='ok')
        return JsonResponse(code=c.API_MESSAGE_OK, message='fail')


class RoleFilter(filters.FilterSet):
    """
    角色搜索过滤器
    """
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')  # icontains代表模糊匹配
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')

    class Meta:
        model = models.Role
        fields = ['name', 'code']


class RoleViewSet(BaseViewSet):
    """
    角色接口
    """
    queryset = models.Role.objects.filter()
    serializer_class = serializers.RoleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    filter_fields = ('name', 'code',)
    ordering_fields = ('created',)
    ordering = ('-created',)
    filter_class = RoleFilter

    @action(detail=False, methods=['post'])
    def add_member(self, request):
        """
        添加成员
        把角色和用户关联起来
        """
        role_id = self.request.data.get("role_id", '')
        user_list = self.request.data.get("user_list", [])
        try:
            user = models.Role.objects.get(id=role_id)
        except models.Role.DoesNotExist:
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        for user_id in user_list:
            models.UserRole.objects.create(user_id=user_id, role_id=role_id)
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok')

    # @action(detail=False, methods=['get'])
    # def user_info(self, request):
    #     """
    #     查看该角色下关联的用户
    #     param: role_id
    #     """
    #     form = forms.UserRole(request.GET)
    #     if not form.is_valid():
    #         # 不是有效数据
    #         return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
    #                             status=status.HTTP_400_BAD_REQUEST)
    #     data = form.cleaned_data
    #     qs = models.UserRole.objects.filter(role_id=data['role_id'])
    #     print(qs)
    #     res = []
    #     for user_role_obj in qs:
    #         user = models.User.objects.filter(id=user_role_obj.user_id)
    #         serializer = serializers.UserSimpleSerializer(user, many=True)
    #         res.append(serializer.data)
    #     return JsonResponse(code=c.API_MESSAGE_OK, message='ok', data=res)

    @action(detail=False, methods=['post'])
    def authorize(self, request):
        """
        角色功能授权接口
        """
        # form = forms.AuthorizeForm(request.data)
        # if not form.is_valid():
        #     # 不是有效数据
        #     return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
        #                         status=status.HTTP_400_BAD_REQUEST)
        # data = form.cleaned_data
        data = request.data
        print(data)
        resp = services.role_authorize(data["role_id"], data)
        if resp:
            return JsonResponse(code=c.API_MESSAGE_OK, message='ok')
        return JsonResponse(code=c.API_MESSAGE_OK, message='fail')


class CompanyFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')  # icontains代表模糊匹配
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    manager = filters.CharFilter(field_name='manager', lookup_expr='icontains')

    class Meta:
        model = models.Company
        fields = ['name', 'code', 'manager']


class CompanyViewSet(BaseViewSet):
    """
    组织架构-公司接口
    """
    queryset = models.Company.objects.filter()
    serializer_class = serializers.CompanySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)

    search_fields = ('name', 'code', 'manager')
    ordering = ('-created',)
    filter_class = CompanyFilter

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        获取树形列表
        :param request:
        :return:
        """
        qs = models.Company.objects.filter(parent_id=c.DEFAULT_BLANK_PARENT_ID)
        tree_serializer = serializers.CompanyTreeSerializer(qs, many=True)
        return JsonResponse(data=tree_serializer.data, code=c.API_MESSAGE_OK, message='ok')


class DepartmentFilter(filters.FilterSet):
    """
    部门过滤器
    """
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')  # icontains代表模糊匹配
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    manager = filters.CharFilter(field_name='manager', lookup_expr='icontains')
    company_id = filters.CharFilter(field_name='company_id', lookup_expr='icontains')

    class Meta:
        model = models.Department
        fields = ['name', 'code', 'manager', 'company_id']


class DepartmentViewSet(BaseViewSet):
    """
    组织构架 - 部门接口
    """
    queryset = models.Department.objects.filter()
    serializer_class = serializers.DepartmentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    search_fields = ('name', 'code', 'manager', 'company_id')
    ordering = ('-created',)
    filter_class = DepartmentFilter

    # @action(detail=False, methods=['get'])
    # def info(self, request):
    #     """
    #     根据公司id获取相应的部门
    #     param: company_id
    #     """
    #     company_id = request.GET.get("company_id", "")
    #     try:
    #         instance = models.Department.objects.filter(company_id=company_id)
    #     except models.Department.DoesNotExist:
    #         return JsonResponse(message=c.EMPTY_DEPARTMENT, code=status.HTTP_400_BAD_REQUEST,
    #                             status=status.HTTP_400_BAD_REQUEST)
    #     serializer = serializers.DepartmentSerializer(instance, many=True)
    #     return JsonResponse(data=serializer.data, code=c.API_MESSAGE_OK, message='ok')
    #
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return JsonResponse(data=serializer.data, code=c.API_MESSAGE_OK, message='ok', status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        获取树形列表
        :param request:
        :return:
        """
        qs = models.Department.objects.filter(parent_id=c.DEFAULT_BLANK_PARENT_ID)
        tree_serializer = serializers.DepartmentTreeSerializer(qs, many=True)
        return JsonResponse(data=tree_serializer.data, code=c.API_MESSAGE_OK, message='ok')


class PostFilter(filters.FilterSet):
    """
    岗位过滤器
    查询字段
    """
    company_id = filters.CharFilter(field_name='company_id', lookup_expr='icontains')
    department_id = filters.CharFilter(field_name='department_id', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')

    class Meta:
        model = models.Post
        fields = ['name', 'code']


class PostViewSet(BaseViewSet):
    """
    组织架构 - 岗位接口
    """
    queryset = models.Post.objects.filter()
    serializer_class = serializers.PostSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    search_fields = ('name', 'code',)
    filter_fields = ('company_id', 'department_id',)  # 筛选字段
    ordering_fields = ('created',)
    ordering = ('-created',)
    filter_class = PostFilter

    @action(detail=False, methods=['post'])
    def add_member(self, request):
        """
        添加成员
        把职位和用户关联起来
        """
        # form = forms.PostAddMember(request.data)
        # if not form.is_valid():
        #     # 不是有效数据
        #     return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
        #                         status=status.HTTP_400_BAD_REQUEST)
        # data = form.cleaned_data
        post_id = self.request.data.get("post_id", '')
        person_list = self.request.data.get("person_list", [])
        try:
            post_obj = models.Post.objects.get(id=post_id)
        except models.Post.DoesNotExist:
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        for person_id in person_list:
            models.UserPost.objects.create(user_id=person_id, post_id=post_id)
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok')

    @action(detail=False, methods=['get'])
    def user_info(self, request):
        """
        查看该岗位下关联的用户
        param: post_id
        """
        form = forms.UserPost(request.GET)
        if not form.is_valid():
            # 不是有效数据
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        data = form.cleaned_data
        qs = models.UserPost.objects.filter(post_id=data['post_id'])
        print(qs)
        res = []
        for user_post_obj in qs:
            user = models.User.objects.get(id=user_post_obj.user_id)
            serializer = serializers.UserSimpleSerializer(user)
            res.append(serializer.data)
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok', data=res)


class DataDictFilter(filters.FilterSet):
    """
    数据字典过滤器
    """
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')

    class Meta:
        model = models.DataDict
        fields = ['name', 'code']


class DataDictViewSet(BaseViewSet):
    """
    数据字典接口
    """
    queryset = models.DataDict.objects.filter()
    serializer_class = serializers.DataDictSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    ordering_fields = ('created',)
    ordering = ('-created',)
    filter_class = DataDictFilter
    filter_fields = ('parent_id',)

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        获取树形列表
        :param request:
        :return:
        """
        qs = models.DataDict.objects.filter(parent_id=c.DEFAULT_BLANK_PARENT_ID)
        tree_serializer = serializers.DataDictTreeSerializer(qs, many=True)
        return JsonResponse(data=tree_serializer.data, code=c.API_MESSAGE_OK, message='ok')


class DataDictDetailViewSet(BaseViewSet):
    """
    数据字典详情
    """
    queryset = models.DataDictItem.objects.filter()
    serializer_class = serializers.DataDictItemSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    ordering_fields = ('created',)
    ordering = ('-created',)
    filter_fields = ('parent_id', 'data_dict_id')


class ModuleViewSet(BaseViewSet):
    """
    系统模块接口
    """
    queryset = models.Module.objects.filter()
    serializer_class = serializers.ModuleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    ordering_fields = ('created', 'sort')
    ordering = ('sort',)
    search_fields = ('name', 'code',)
    filter_fields = ('parent_id', 'is_menu', 'deleted', 'code')

    def perform_create(self, serializer):
        button_list = self.request.data.get('button_list', '[]')
        column_list = self.request.data.get('column_list', '[]')
        form_list = self.request.data.get('form_list', '[]')
        parent_id = self.request.data.get('parent_id', "")
        module = serializer.save()
        try:
            parent = models.Module.objects.get(id=parent_id)
        except models.Module.DoesNotExist:
            return None
        module.level = parent.level + 1
        module.save()
        # 关联其他模块
        services.create_sub_modules(module, button_list, column_list, form_list)

    def perform_update(self, serializer):
        button_list = self.request.data.get('button_list', '[]')
        column_list = self.request.data.get('column_list', '[]')
        form_list = self.request.data.get('form_list', '[]')
        parent_id = self.request.data.get('parent_id', "")

        module = serializer.save()
        # 先移除原来的子模块
        try:
            parent = models.Module.objects.get(id=parent_id)
        except models.Module.DoesNotExist:
            return None
        module.level = parent.level + 1
        module.save()
        services.remove_sub_modules(module)
        services.create_sub_modules(module, button_list, column_list, form_list)

    def perform_destroy(self, instance):
        services.remove_sub_modules(instance)
        super().perform_destroy(instance)

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        获取树形列表
        :param request:
        :return:
        """
        qs = models.Module.objects.filter(parent_id=c.DEFAULT_BLANK_PARENT_ID)
        tree_serializer = serializers.ModuleTreeSerializer(qs, many=True)
        return JsonResponse(data=tree_serializer.data, code=c.API_MESSAGE_OK, message='ok')

    @action(detail=False, methods=['get'])
    def button_tree(self, request):
        """
        获取带按钮的树形模块列表
        :param request:
        :return:
        """
        qs = models.Module.objects.filter(parent_id=c.DEFAULT_BLANK_PARENT_ID)
        tree_serializer = serializers.ModuleButtonTreeSerializer(qs, many=True)
        return JsonResponse(data=tree_serializer.data, code=c.API_MESSAGE_OK, message='ok')

    @action(detail=False, methods=['get'])
    def column_tree(self, request):
        """
        获取带列表的树形模块列表
        :param request:
        :return:
        """
        qs = models.Module.objects.filter(parent_id=c.DEFAULT_BLANK_PARENT_ID)
        tree_serializer = serializers.ModuleColumnTreeSerializer(qs, many=True)
        return JsonResponse(data=tree_serializer.data, code=c.API_MESSAGE_OK, message='ok')

    @action(detail=False, methods=['get'])
    def form_tree(self, request):
        """
        获取带按钮的树形模块列表
        :param request:
        :return:
        """
        qs = models.Module.objects.filter(parent_id=c.DEFAULT_BLANK_PARENT_ID)
        tree_serializer = serializers.ModuleFormTreeSerializer(qs, many=True)
        return JsonResponse(data=tree_serializer.data, code=c.API_MESSAGE_OK, message='ok')


class ModuleButtonViewSet(BaseViewSet):
    """
    按钮控制接口
    """
    queryset = models.ModuleButton.objects.filter()
    serializer_class = serializers.ModuleButtonSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    ordering_fields = ('created', 'sort')
    ordering = ('sort',)
    search_fields = ('name', 'code',)
    filter_fields = ('parent_id', 'module_id', 'deleted',)

    def get_queryset(self):
        module_code = self.request.GET.get("module_code", None)
        if module_code:
            module = models.Module.objects.get(code=module_code)
            return self.queryset.filter(module_id=module.id)
        else:
            return self.queryset.filter()


class ModuleColumnViewSet(BaseViewSet):
    """
    列表接口
    """
    queryset = models.ModuleColumn.objects.filter()
    serializer_class = serializers.ModuleColumnSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    ordering_fields = ('created', 'sort')
    ordering = ('sort',)
    search_fields = ('name', 'code',)
    filter_fields = ('module_id', 'deleted')

    def get_queryset(self):
        module_code = self.request.GET.get("module_code", None)
        if module_code:
            module = models.Module.objects.get(code=module_code)
            return self.queryset.filter(module_id=module.id)
        else:
            return self.queryset.filter()


class ModuleFormViewSet(BaseViewSet):
    """
    表单接口
    """
    queryset = models.ModuleForm.objects.filter()
    serializer_class = serializers.ModuleFormSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    ordering_fields = ('created', 'sort')
    ordering = ('sort',)
    search_fields = ('name', 'code',)
    filter_fields = ('module_id', 'deleted')

    def get_queryset(self):
        module_code = self.request.GET.get("module_code", None)
        if module_code:
            module = models.Module.objects.get(code=module_code)
            return self.queryset.filter(module_id=module.id)
        else:
            return self.queryset.filter()


class AuthorizeViewSet(BaseViewSet):
    """
    功能权限授权接口
    """
    queryset = models.Authorize.objects.filter()
    serializer_class = serializers.AuthorizeSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    ordering_fields = ('created',)
    ordering = ('-created',)
    filter_fields = ('object_type', 'object_id', 'item_type', 'enable')

    @action(detail=False, methods=['get'], permission_classes=[permissions.UserLoginRequire],
            authentication_classes=[authentication.UserTokenAuthentication])
    def own(self, request):
        """
        获取当前用户自身的所有权限，包括所属的角色的
        :param request:
        :return:
        """
        item_type = request.GET.get('item_type', None)
        # 获取所属的全部角色数组
        roles = models.UserRole.objects.filter(user_id=request.user.id).values_list('role_id', flat=True)
        condition1 = Q(object_id=request.user.id) | Q(object_id__in=roles)
        if item_type:
            condition2 = Q(item_type=item_type)
            qs = models.Authorize.objects.filter(condition1, condition2)
        else:
            qs = models.Authorize.objects.filter(condition1)
        serializer = serializers.AuthorizeSerializer(qs, many=True)
        return JsonResponse(data=serializer.data, code=c.API_MESSAGE_OK, message='ok')


class LogViewSet(BaseViewSet):
    """
    系统日志接口
    """
    queryset = models.Log.objects.filter()
    serializer_class = serializers.LogSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    search_fields = ("module_name",)
    ordering_fields = ('created',)
    ordering = ('-created',)
    filter_fields = ('type', 'operate_user_id')

    def get_queryset(self):
        start_time = self.request.GET.get('start_time')
        end_time = self.request.GET.get('end_time')
        if start_time and end_time:
            start_time = datetime.strptime(start_time, "%Y-%m-%d")
            end_time = datetime.strptime(end_time, "%Y-%m-%d")
            final_time = end_time + timedelta(days=1)
            return self.queryset.filter(created__range=(start_time, final_time))
        return self.queryset.filter()

    @action(detail=False, methods=['delete'])
    def empty(self, request):
        """清空选中日志类型和时间范围的数据"""
        form = forms.LogDeleteForm(request.data)
        if not form.is_valid():
            # 不是有效数据
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        data = form.cleaned_data
        start = datetime.datetime.strptime(data['start_time'], '%Y-%m-%d')
        end = datetime.datetime.strptime(data['end_time'], '%Y-%m-%d')
        final = end + datetime.timedelta(days=1)
        objs = models.Log.objects.filter(operate_time__range=(start, final), type=data['type'])
        objs.delete()
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok')


class AliyunUploadToken(views.APIView):
    """
    获取阿里云上传凭证Token
    """

    @action(detail=False, methods=["get"])
    def get(self, request, *args, **kwargs):
        """
        参数：文件类型、回调URL、业务系统中
        url:string 回调的url
        file_type:
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_name = request.GET.get("file_name")
        token, key = services.gen_aliyun_uptoken(file_name)
        if not token:
            raise ServerError()
        data = {'token': token, 'key': key}
        return JsonResponse(data=data, code=c.API_MESSAGE_OK, message='ok')
