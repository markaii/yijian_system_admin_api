from __future__ import unicode_literals
from member import views
from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'charge/order', views.MemberChargeOrderViewSet)  # 会员卡充值订单API  /member/charge/order/
router.register(r'consume/log', views.MemberCardConsumeLogViewSet)  # 用户会员卡消费记录API  /member/consume/log/
router.register(r'charge/log', views.MemberCardChargeLogViewSet)  # 用户会员卡充值记录API  /member/charge/log/
router.register(r'card/instance', views.MemberCardInstanceViewSet)  # 用户会员卡API  /member/card/instance/
router.register(r'card', views.MemberCardViewSet)  # 商家会员卡API  /member/card/

urlpatterns = [
    url(r'^', include(router.urls)),
]
