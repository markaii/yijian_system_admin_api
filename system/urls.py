# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from system import views

router = routers.DefaultRouter()
router.register('sample', views.SystemSampleView)
router.register(r'config', views.SystemConfigViewSet)  # 系统配置API

urlpatterns = [
    url(r'^gen_url_scheme/$', views.GenUrlScheme.as_view(), name='gen_url_scheme'),
    url(r'^upload/signature/$', views.UploadSignature.as_view(), name='get_upload_upload_token'),
    url(r'^temp/secret/$', views.GenTempSecret.as_view(), name='get_temp_secret'),
    url(r'^mp/menu/$', views.CreateMpMenu.as_view(), name='create_mp_menu'),
    url(r'^', include(router.urls)),
]
