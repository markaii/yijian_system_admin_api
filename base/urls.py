from __future__ import unicode_literals
from base import views
from django.conf.urls import url, include

from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)  # 用户
router.register('role', views.RoleViewSet)  # 角色
router.register('company', views.CompanyViewSet)  # 公司
router.register('department', views.DepartmentViewSet)  # 部门
router.register('post', views.PostViewSet)  # 职位

router.register('module/button', views.ModuleButtonViewSet)  # 按钮
router.register('module/column', views.ModuleColumnViewSet)  # 按列表
router.register('module/form', views.ModuleFormViewSet)  # 表单
router.register('module', views.ModuleViewSet)  # 模块

router.register('datadict/detail', views.DataDictDetailViewSet)  # 数据字典详情
router.register('datadict', views.DataDictViewSet)  # 数据字典

router.register('authorize', views.AuthorizeViewSet)  # 功能授权

router.register('log', views.LogViewSet)  # 系统日志

# router.register('token', views.AliyunUploadToken)  # 上传文件token

urlpatterns = [
    #TODO 我们是腾讯云
    url(r'^token/$', views.AliyunUploadToken.as_view(), name='aliyun_upload_token'),  # 上传文件token
    url(r'^', include(router.urls)),

]
