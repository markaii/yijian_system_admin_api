from activity import views

from django.conf.urls import url, include

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'coupon/pin_log', views.ShopPinLogViewSet)  # 拼团记录API /activity/coupon/pin_log/
router.register(r'coupon', views.ShopCouponActivityViewSet)  # 店铺优惠券活动API /activity/coupon/
router.register(r'poster/log', views.ShopPosterApplyLogViewSet)  # 店铺物料申请记录API /activity/poster/log/
router.register(r'poster', views.ShopPosterApplyViewSet)  # 店铺物料申请API /activity/poster/
router.register(r'invite/config', views.ShopInviteActivityViewSet)  # 入驻活动广告配置API /activity/invite/config/
router.register(r'invite/log', views.ShopInviteLogViewSet)  # 入驻邀请记录API /activity/invite/log/
router.register(r'banner', views.BannerViewSet)  # 小程序广告配置API  /activity/banner/config/

urlpatterns = [
    url(r'^', include(router.urls)),
]
