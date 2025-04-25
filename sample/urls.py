# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sample import views
from django.conf.urls import url, include

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'hair_color_change_log', views.HairColorChangeLogViewSet)  # 变更发色记录 API /hair_color_change_log
router.register(r'hair_change_log', views.HairChangeLogViewSet)  # 变更发型记录 API /hair_change_log
router.register(r'report', views.SampleReportViewSet)  # 举报 API /report
router.register(r'tag', views.SampleTagViewSet)  # 标签 API /tag
router.register(r'', views.SampleViewSet)  # 作品 API  /

urlpatterns = [
    url(r'^', include(router.urls))
]
