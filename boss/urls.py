from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from boss import views

router = routers.DefaultRouter()
router.register(r'', views.BossViewSet)  # 老板账号 API  /

urlpatterns = [
    url(r'^', include(router.urls))
]
