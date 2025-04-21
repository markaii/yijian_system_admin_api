from rest_framework import routers
from django.conf.urls import url, include

from task import views

router = routers.DefaultRouter()
router.register(r'log', views.ShopCollectLogViewSet)  # 店铺采集记录 API  /task/log
router.register(r'', views.ShopCollectTaskViewSet)  # 店铺采集任务 API  /task/

urlpatterns = [
    url(r'^', include(router.urls)),
]
