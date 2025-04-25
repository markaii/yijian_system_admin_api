import uuid
from django.db import models
from model_utils.models import TimeStampedModel
from base import services, constants as c


class User(TimeStampedModel):
    """
    用户: 后台管理员用户，登录的时候使用的
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    account = models.CharField(verbose_name='账号', max_length=50, unique=True)
    password = models.CharField(verbose_name='密码', max_length=100)
    salt = models.CharField(verbose_name='盐', max_length=50, blank=True)
    token = models.CharField(verbose_name='token', max_length=100, blank=True)
    code = models.CharField(verbose_name='工号', max_length=100, blank=True)
    company_id = models.CharField(verbose_name='公司ID', max_length=50, blank=True)
    department_id = models.CharField(verbose_name='部门ID', max_length=50, blank=True)
    realname = models.CharField(verbose_name='真实姓名', max_length=100, blank=True)
    nickname = models.CharField(verbose_name='昵称', max_length=100, blank=True)
    avatar = models.CharField(verbose_name='头像', max_length=250, blank=True)
    phone = models.CharField(verbose_name='手机号', max_length=50, blank=True)
    email = models.CharField(verbose_name='邮箱', max_length=50, blank=True)
    qq = models.CharField(verbose_name='qq', max_length=50, blank=True)
    wechat = models.CharField(verbose_name='微信号', max_length=50, blank=True)
    gender = models.IntegerField(verbose_name='性别', default=c.GENDER_TYPE_UNKNOWN, choices=c.GENDER_CHOICE)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    is_superuser = models.IntegerField(verbose_name='是否超级用户', default=c.BOOL_TYPE_FALSE, choices=c.BOOL_TYPE_CHOICE)

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    remark = models.CharField(verbose_name='备注', max_length=200, blank=True)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=50, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=50, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    # def save(self, *args, **kwargs):
    #     try:
    #         obj = User.objects.get(account=self.account)
    #         print("*" * 100)
    #     except:
    #         self.salt = services._generate_random_str(10)
    #         self.password = services.encrypt_password(self.salt, self.password)
    #         super(User, self).save(*args, **kwargs)
    #         return
    #     if self.password != obj.password:
    #         self.password = services.encrypt_password(self.salt, self.password)
    #     super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Role(TimeStampedModel):
    """
    组织架构 - 角色
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='角色名称', max_length=100)
    code = models.CharField(verbose_name='角色代号', max_length=100, blank=True)

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    remark = models.CharField(verbose_name='备注', max_length=200, blank=True)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class UserRole(TimeStampedModel):
    """
    用户角色
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)
    role_id = models.CharField(verbose_name='角色id', max_length=50, blank=True)

    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)

    class Meta:
        verbose_name = '用户角色关系'
        verbose_name_plural = verbose_name


class UserPost(TimeStampedModel):
    """
    用户岗位关系
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    user_id = models.CharField(verbose_name='用户id', max_length=50, blank=True)
    post_id = models.CharField(verbose_name='岗位id', max_length=50, blank=True)

    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)

    class Meta:
        verbose_name = '用户岗位关系'
        verbose_name_plural = verbose_name


class Company(TimeStampedModel):
    """
    组织构架 - 公司
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='公司名称', max_length=100)
    code = models.CharField(verbose_name='公司代号-组织机构编号', max_length=100, blank=True)
    short_name = models.CharField(verbose_name='公司简称', max_length=100, blank=True)
    phone = models.CharField(verbose_name='电话', max_length=50, blank=True)
    fax = models.CharField(verbose_name='传真', max_length=100, blank=True)
    email = models.CharField(verbose_name='邮箱', max_length=50, blank=True)
    manager = models.CharField(verbose_name='负责人', max_length=100, blank=True)
    parent_id = models.CharField(verbose_name='父ID', max_length=50, blank=True)
    province = models.CharField(verbose_name='省', max_length=50, blank=True)
    province_code = models.CharField(verbose_name='省编码', max_length=100, blank=True)
    city = models.CharField(verbose_name='市', max_length=50, blank=True)
    city_code = models.CharField(verbose_name='市编码', max_length=100, blank=True)
    district = models.CharField(verbose_name='区', max_length=100, blank=True)
    district_code = models.CharField(verbose_name='区编码', max_length=100, blank=True)
    address = models.CharField(verbose_name='详细地址', max_length=255, blank=True)
    url = models.CharField(verbose_name='主页', max_length=255, blank=True)

    remark = models.CharField(verbose_name='备注', max_length=200, blank=True)
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '公司'
        verbose_name_plural = verbose_name


class Department(TimeStampedModel):
    """
    组织构架 - 部门
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='部门名称', max_length=100)
    code = models.CharField(verbose_name='部门代码', max_length=100, blank=True)
    phone = models.CharField(verbose_name='电话', max_length=50, blank=True)
    short_name = models.CharField(verbose_name='简称', max_length=50, blank=True)
    fax = models.CharField(verbose_name='传真', max_length=100, blank=True)
    email = models.CharField(verbose_name='邮箱', max_length=50, blank=True)
    address = models.CharField(verbose_name='地址', max_length=255, blank=True)
    manager = models.CharField(verbose_name='负责人', max_length=100, blank=True)
    parent_id = models.CharField(verbose_name='父ID', max_length=50, blank=True)
    company_id = models.CharField(verbose_name='公司ID', max_length=50, blank=True)

    remark = models.CharField(verbose_name='备注', max_length=200, blank=True)
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name


class Post(TimeStampedModel):
    """
    组织架构 - 职位
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='职位名称', max_length=100)
    parent_id = models.CharField(verbose_name='父ID', max_length=50, blank=True)
    code = models.CharField(verbose_name='职位代码', max_length=100, blank=True)
    company_id = models.CharField(verbose_name='公司ID', max_length=50, blank=True)
    department_id = models.CharField(verbose_name='部门ID', max_length=50, blank=True)

    remark = models.CharField(verbose_name='备注', max_length=200, blank=True)
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '职位'
        verbose_name_plural = verbose_name


#########################################################
# 权限相关
#########################################################
class Module(TimeStampedModel):
    """
    系统模块
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='模块名称', max_length=100)
    code = models.CharField(verbose_name='模块代号', max_length=100, blank=True, unique=True)
    icon = models.CharField(verbose_name='模块图标', help_text='font-awesome图标css id', max_length=100, blank=True)
    url = models.CharField(verbose_name='模块地址', max_length=255, blank=True)
    parent_id = models.CharField(verbose_name='父ID', max_length=50, blank=True)
    is_menu = models.IntegerField(verbose_name='是否是菜单', default=c.BOOL_TYPE_FALSE, choices=c.BOOL_TYPE_CHOICE)
    level = models.IntegerField(verbose_name='模块等级', default=0)

    remark = models.CharField(verbose_name='备注', max_length=200, blank=True)
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)
    is_hide = models.IntegerField(verbose_name='是否隐藏', default=c.BOOL_TYPE_FALSE, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '系统模块'
        verbose_name_plural = verbose_name


class ModuleButton(TimeStampedModel):
    """
    按钮：
        系统中每一个模块对应的功能按钮
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    module_id = models.CharField(verbose_name='所属系统模块ID', max_length=50, blank=True)
    parent_id = models.CharField(verbose_name='父ID', max_length=50, blank=True)
    name = models.CharField(verbose_name='按钮名称', max_length=100)
    icon = models.CharField(verbose_name='按钮图标', help_text='font-awesome图标css id', max_length=100, blank=True)
    code = models.CharField(verbose_name='按钮代号', max_length=100, blank=True)

    remark = models.CharField(verbose_name='备注', max_length=200, blank=True)
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '模块按钮'
        verbose_name_plural = verbose_name


class ModuleColumn(TimeStampedModel):
    """
    模块列表视图
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    module_id = models.CharField(verbose_name='所属系统模块ID', max_length=50, blank=True)
    name = models.CharField(verbose_name='列名', max_length=100)
    code = models.CharField(verbose_name='按钮代号', max_length=100, blank=True)

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '模块列表'
        verbose_name_plural = verbose_name


class ModuleForm(TimeStampedModel):
    """
    模块表单视图
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    module_id = models.CharField(verbose_name='所属系统模块ID', max_length=50, blank=True)
    name = models.CharField(verbose_name='列名', max_length=100)
    code = models.CharField(verbose_name='按钮代号', max_length=100, blank=True)

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '模块表单'
        verbose_name_plural = verbose_name


class Authorize(TimeStampedModel):
    """
    功能权限授权表
        将「菜单」、「按钮」、「视图」、「表单」等授权给「角色」或「用户」
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    object_type = models.IntegerField(verbose_name='授权对象类型', default=0, choices=c.AUTHORIZE_OBJECT_TYPE_CHOICE,
                                      help_text='对象分类:0-用户 1-角色')
    object_id = models.CharField(verbose_name='授权对象主键', max_length=50, blank=True)
    item_type = models.IntegerField(verbose_name='授权项目类型', default=0, choices=c.AUTHORIZE_ITEM_TYPE_CHOICE,
                                    help_text='项目类型:0-菜单 1-按钮 2-视图 3-表单')
    item_id = models.CharField(verbose_name='授权项目主键', max_length=50)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '权限授权'
        verbose_name_plural = verbose_name


#########################################################
# 系统功能
#########################################################


class Log(TimeStampedModel):
    """
    系统日志
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    type = models.IntegerField(verbose_name='日志分类', help_text='1：登陆，2：访问，3：操作，4：异常',
                               default=c.LOG_TYPE_UNKNOWN, choices=c.LOG_TYPE_CHOICE)
    module_name = models.CharField(verbose_name='模块', max_length=100, blank=True)

    operate_user_id = models.CharField(verbose_name='操作用户id', max_length=50, blank=True)
    operate_user = models.CharField(verbose_name='操作用户', max_length=100, blank=True)
    operate_time = models.DateTimeField(verbose_name='操作时间', blank=True, null=True)
    operate_type = models.CharField(verbose_name='操作类型', blank=True, max_length=100)

    ip_address = models.CharField(verbose_name='操作IP', max_length=100, blank=True)
    ip_address_name = models.CharField(verbose_name='IP所在地', max_length=200, blank=True)
    host = models.CharField(verbose_name='主机', max_length=100, blank=True)
    browser = models.CharField(verbose_name='浏览器', max_length=255, blank=True)

    result_type = models.IntegerField(verbose_name='执行结果类型', default=c.LOG_RESULT_SUCCESS,
                                      choices=c.LOG_RESULT_CHOICE)
    result_desc = models.CharField(verbose_name='操作结果描述', max_length=255,
                                   help_text='例如：登录失败：账号密码错误', blank=True)
    deleted = models.IntegerField(verbose_name='删除', default=0, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '系统日志'
        verbose_name_plural = verbose_name


class IPBlackList(TimeStampedModel):
    """
    IP黑名单
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    start_ip = models.CharField(verbose_name='起始IP地址', max_length=100, blank=True)
    end_ip = models.CharField(verbose_name='结束IP地址', max_length=100, blank=True)
    description = models.CharField(verbose_name='描述', max_length=200, blank=True)

    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = 'IP黑名单'
        verbose_name_plural = verbose_name


class DataDict(TimeStampedModel):
    """
    数据字典
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    parent_id = models.CharField(verbose_name='父节点ID', max_length=50, blank=True)
    name = models.CharField(verbose_name='节点名称', max_length=100)
    code = models.CharField(verbose_name='节点编码', max_length=100, blank=True)

    remark = models.CharField(verbose_name='备注', max_length=200, blank=True)
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '数据字典'
        verbose_name_plural = verbose_name


class DataDictItem(TimeStampedModel):
    """
    数据字典详情
    """
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    data_dict_id = models.CharField(verbose_name='所属数据字典', max_length=50, blank=True)  # FK
    parent_id = models.CharField(verbose_name='父节点ID', max_length=50, blank=True)
    name = models.CharField(verbose_name='名字', max_length=100)
    value = models.CharField(verbose_name='值', max_length=100)
    code = models.CharField(verbose_name='编码', max_length=100, blank=True)

    remark = models.CharField(verbose_name='备注', max_length=200, blank=True)
    sort = models.IntegerField(verbose_name='排序码', help_text='从小到大排序', default=0)
    create_user_id = models.CharField(verbose_name='创建用户Id', max_length=50, blank=True)
    create_user_name = models.CharField(verbose_name='创建用户', max_length=100, blank=True)
    modify_user_id = models.CharField(verbose_name='修改用户Id', max_length=50, blank=True)
    modify_user_name = models.CharField(verbose_name='修改用户', max_length=100, blank=True)
    enable = models.IntegerField(verbose_name='有效标记', default=c.ENABLE_TYPE_NORMAL, choices=c.ENABLE_CHOICE)
    deleted = models.IntegerField(verbose_name='删除标记', default=c.DELETE_TYPE_NORMAL, choices=c.DELETE_CHOICE)

    class Meta:
        verbose_name = '数据字典详情'
        verbose_name_plural = verbose_name
