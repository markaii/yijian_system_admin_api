import json

from django.http import HttpResponsePermanentRedirect
from rest_framework import status, views
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from system import services
from system import models
from system import serializers

from project import constants as c

from common.response import JsonResponse
from common.viewsets import BaseViewSet

from base import permissions, authentication


# 给消费者发送短信通知
# 推送消息


class UploadSignature(views.APIView):
    """
    文件上传签名
    """

    def get(self, request):
        file_name = request.GET.get('file_name', '')
        signature, key = services.get_cos_sign(file_name)
        data = {'signature': signature, 'key': key}
        return JsonResponse(data=data, code=c.API_MESSAGE_OK, message='ok')


class GenTempSecret(views.APIView):
    """
    获取临时密钥
    """

    def get(self, request):
        resp = services.gen_temp_secret()
        return JsonResponse(data=resp, code=c.API_MESSAGE_OK, message='ok')


class SystemConfigViewSet(BaseViewSet):
    """
    系统配置接口
    """
    queryset = models.SystemConfig.objects.filter()
    serializer_class = serializers.SystemConfigSerializers
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    # permission_classes = (permissions.UserLoginRequire,)
    # authentication_classes = (authentication.UserTokenAuthentication,)
    filter_fields = ('value_type', 'name',)
    search_fields = ('name',)
    ordering = ('-created',)


class CreateMpMenu(views.APIView):
    """
    创建公众号菜单
    """

    def post(self, request):
        menu = request.data.get('menu', {})
        resp = services.create_mp_menu(menu)
        return JsonResponse(data=resp, code=c.API_MESSAGE_OK, message='ok')


class SystemSampleView(BaseViewSet):
    """
    系统样本接口
    """
    queryset = models.SystemSample.objects.filter()
    serializer_class = serializers.SystemSampleSerializers
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('type', 'status', 'role_type',)
    ordering_fields = ('sort', 'created',)
    ordering = ('-created',)


class GenUrlScheme(views.APIView):
    """
    生成小程序 scheme 码
    """

    def get(self, request):
        path = request.GET.get('path', '')
        query = request.GET.get('query', '')

        if not path or not query:
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)

        code, data = services.get_url_scheme(path=path, query=query)
        if not code:
            return JsonResponse(message=data, code=c.ErrorCode.ERROR_WECHAT_API)
        return HttpResponsePermanentRedirect(data)
