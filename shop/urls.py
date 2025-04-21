from rest_framework import routers
from django.conf.urls import url,include

from shop import views

router = routers.DefaultRouter()
router.register(r'pay_apply/enterprise', views.PayApplyEnterpriseViewSet)  # 企业进件API /shop/pay_apply/enterprise/
router.register(r'pay_apply/individual', views.PayApplyIndividualViewSet)  # 个体工商户进件API /shop/pay_apply/individual/
router.register(r'merchant_order', views.MerchantOrderViewSet)  # 商户订单 API /shop/merchant_order/
router.register(r'service', views.ShopServiceViewSet)  # 店铺服务项目API /shop/service/
router.register(r'',views.ShopViewSet)  #店铺 API  /

urlpatterns = [
    url(r'^',include(router.urls)),
]