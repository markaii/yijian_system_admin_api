from rest_framework import routers
from django.conf.urls import url, include

from barber import views

router = routers.DefaultRouter()
router.register(r'service/category', views.ServiceCategoryViewSet)  # 服务项目分类 API /barber/service/category
router.register(r'systemservice', views.SystemServiceViewSet)  # 系统服务项目 API /systemservice
router.register(r'service', views.ServiceViewSet)  # 服务项目 API /service
router.register(r'example', views.ExampleViewSet)  # 作品 API /example
router.register(r'', views.BarberViewSet)  # 理发师账号 API  /

urlpatterns = [
    url(r'^', include(router.urls))
]
