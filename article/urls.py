from __future__ import unicode_literals
from article import views
from django.conf.urls import url, include
from django.urls import path

from rest_framework import routers

router = routers.DefaultRouter()
router.register('category', views.ArticleCategoryViewSet)  # 文章分类接口    /article/category/
router.register('', views.ArticleViewSet)  # 文章接口       /article/

urlpatterns = [
    url(r'^', include(router.urls)),
]
