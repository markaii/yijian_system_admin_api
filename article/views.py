from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from common.response import JsonResponse
from rest_framework import status, views
from rest_framework.decorators import action
from common.viewsets import BaseViewSet
from common.exceptions import ParamsError
from article import models
from article import serializers
from article import constants as c
from base import authentication, permissions


class ArticleViewSet(BaseViewSet):
    """
    文章
    """
    queryset = models.Article.objects.filter()
    serializer_class = serializers.ArticleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('title',)
    filter_fields = ('author_id', 'category_id',)
    ordering_fields = ('created',)
    ordering = ("-created",)

    def get_permissions(self):
        """
        GET请求关闭鉴权
        """
        if self.request.META.get('REQUEST_METHOD') == 'GET':
            return [permission() for permission in (permissions.AllowAny,)]
        return [permission() for permission in self.permission_classes]

    def get_authenticators(self):
        """
        GET请求关闭认证
        """
        if self.request.META.get('REQUEST_METHOD') == 'GET':
            return [auth() for auth in (authentication.DummyAuthentication,)]
        return [auth() for auth in self.authentication_classes]

    def perform_create(self, serializer):
        user = self.request.user
        category_id = self.request.data.get("category_id", None)
        try:
            article_category = models.ArticleCategory.objects.get(id=category_id)
        except models.ArticleCategory.DoesNotExist:
            raise ParamsError("category_id无效")

        serializer.save(author_id=user.id, author_name=user.nickname, category_name=article_category.name,
                        publish_date=datetime.now(), create_user_id=user.id, create_user_name=user.nickname)

    def perform_update(self, serializer):
        user = self.request.user
        category_id = self.request.data.get("category_id", None)
        try:
            article_category = models.ArticleCategory.objects.get(id=category_id)
        except models.ArticleCategory.DoesNotExist:
            raise ParamsError("category_id无效")

        serializer.save(category_name=article_category.name, modify_user_id=user.id, modify_user_name=user.nickname)


class ArticleCategoryViewSet(BaseViewSet):
    """
    文章分类
    """
    queryset = models.ArticleCategory.objects.filter()
    serializer_class = serializers.ShareArticleCategorySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('name',)
    filter_fields = ('status',)
    ordering_fields = ('created',)
    ordering = ("-created",)

    def get_permissions(self):
        """
        GET请求关闭鉴权
        """
        if self.request.META.get('REQUEST_METHOD') == 'GET':
            return [permission() for permission in (permissions.AllowAny,)]
        return [permission() for permission in self.permission_classes]

    def get_authenticators(self):
        """
        GET请求关闭认证
        """
        if self.request.META.get('REQUEST_METHOD') == 'GET':
            return [auth() for auth in (authentication.DummyAuthentication,)]
        return [auth() for auth in self.authentication_classes]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(create_user_id=user.id, create_user_name=user.nickname)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(modify_user_id=user.id, modify_user_name=user.nickname)
