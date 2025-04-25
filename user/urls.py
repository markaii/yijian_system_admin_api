# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from user import views
from django.conf.urls import url, include

from rest_framework import routers

router = routers.DefaultRouter()
router.register('customer/order', views.CustomerOrderViewSet)  # 用户订单接口 /customer/order/
router.register('collect', views.CollectionViewSet)  # 用户收藏接口
router.register('address', views.UserAddressViewSet)
router.register('credit/log', views.CreditLogViewSet)  # 日志API接口 /credit/log/
router.register('', views.UserViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
]
