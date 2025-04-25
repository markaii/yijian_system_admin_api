from __future__ import unicode_literals
from coupon import views
from django.conf.urls import url, include

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'voucher', views.CouponVoucherViewSet)  # 优惠券记录API /coupon/voucher/
router.register(r'', views.CouponViewSet)  # 优惠券API /coupon/

urlpatterns = [
    url(r'^', include(router.urls)),
]
