from rest_framework import routers
from django.conf.urls import url, include

from order import views

router = routers.DefaultRouter()
router.register(r'comment', views.CommentViewSet)  # 评论 API order/comment
router.register(r'', views.OrderViewSet)  # 订单 API  order/

urlpatterns = [
    url(r'^', include(router.urls))
]
