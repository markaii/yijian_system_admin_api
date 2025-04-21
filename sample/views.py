from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend

from common.response import JsonResponse
from common.viewsets import BaseViewSet

from base import permissions, authentication

from sample import models, serializers


class SampleTagViewSet(BaseViewSet):
    """
    作品标签基础接口
    GET:    sample/tag/
    POST:   sample/tag/
    PUT:    sample/tag/<id>/
    DELETE: sample/tag/<id>/
    """
    queryset = models.SampleTag.objects.filter()
    serializer_class = serializers.SampleTagSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('name',)
    ordering_fields = ('created', 'sort')
    ordering = ('sort',)


class SampleViewSet(BaseViewSet):
    """
    作品基础接口
    GET:    sample/
    POST:   sample/
    PUT:    sample/<id>/
    DELETE: sample/<id>/
    """
    queryset = models.Sample.objects.filter()
    serializer_class = serializers.SampleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('title',)
    filter_fields = ('user_id', 'barber_id', 'shop_id', 'type', 'status',)
    ordering_fields = ('created', 'sort')
    ordering = ('sort',)

    def get_serializer_class(self):
        # 重写get_serializer_class
        if self.action == 'list':
            return serializers.SampleSerializer
        return serializers.SampleDetailSerializer

    def perform_create(self, serializer):
        file_list = self.request.data.get("file_list", [])
        obj = serializer.save()
        for item in file_list:
            file = item['file'] if 'file' in item else ''
            type = item['type'] if 'type' in item else 0
            sort = item['sort'] if 'sort' in item else 0
            poster = item['poster'] if 'poster' in item else ''
            models.SampleFile.objects.create(sample_id=obj.id, file=file,
                                             type=type, sort=sort, poster=poster)

    def perform_update(self, serializer):
        file_list = self.request.data.get("file_list", [])
        obj = serializer.save()
        # 先删除原有的
        models.SampleFile.objects.filter(sample_id=obj.id).delete()
        for item in file_list:
            file = item['file'] if 'file' in item else ''
            type = item['type'] if 'type' in item else 0
            sort = item['sort'] if 'sort' in item else 0
            poster = item['poster'] if 'poster' in item else ''
            models.SampleFile.objects.create(sample_id=obj.id, file=file,
                                             type=type, sort=sort, poster=poster)


class SampleReportViewSet(BaseViewSet):
    """
    作品举报接口
    GET:    sample/repost/
    POST:   sample/report/
    PUT:    sample/report/<id>/
    DELETE: sample/report/<id>/
    """
    queryset = models.SampleReport.objects.filter()
    serializer_class = serializers.SampleReportSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('phone', 'sample_title')
    filter_fields = ('user_id', 'sample_id')
    ordering_fields = ('created',)

    def get_serializer_class(self):
        # 重写get_serializer_class
        if self.action == 'list':
            return serializers.SampleReportSerializer
        return serializers.SampleReportDetailSerializer


class HairChangeLogViewSet(BaseViewSet):
    """
    变更发型记录接口
    GET:    sample/hair_change_log/
    POST:   sample/hair_change_log/
    PUT:    sample/hair_change_log/<id>/
    DELETE: sample/hair_change_log/<id>/
    """
    queryset = models.HairChangeLog.objects.filter()
    serializer_class = serializers.HairChangeLogSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    search_fields = ('user_name',)
    filter_fields = ('user_id',)
    ordering_fields = ('created',)
    ordering = ('-created')


class HairColorChangeLogViewSet(BaseViewSet):
    """
    变更发色记录接口
    GET:    sample/hair_color_change_log/
    POST:   sample/hair_color_change_log/
    PUT:    sample/hair_color_change_log/<id>/
    DELETE: sample/hair_color_change_log/<id>/
    """
    queryset = models.HairColorChangeLog.objects.filter()
    serializer_class = serializers.HairColorChangeLogSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    search_fields = ('user_name',)
    filter_fields = ('user_id',)
    ordering_fields = ('created',)
    ordering = ('-created')