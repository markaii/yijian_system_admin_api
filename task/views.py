from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from base import permissions, authentication
from common.viewsets import BaseViewSet
from common.response import JsonResponse

from task import models
from task import serializers
from task import tasks
from task import constants as c


class ShopCollectTaskViewSet(BaseViewSet):
    """
    店铺采集任务接口
    """
    queryset = models.ShopCollectTask.objects.filter()
    serializer_class = serializers.ShopCollectTaskSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_fields = ('status', 'province', 'city', 'district',)
    ordering_fields = ('created',)
    ordering = ('-created',)

    @action(methods=['POST'], detail=True)
    def execute(self, request, pk=None):
        """
        执行任务接口
        :param request:
        :return:
        """
        instance = self.get_object()
        instance.status = c.SHOP_COLLECT_STATUS_RUNING
        instance.save()
        # 异步抓取店铺信息
        tasks.collect_shop_info.delay(instance.id)

        return JsonResponse(message="ok", code=c.API_MESSAGE_OK)


class ShopCollectLogViewSet(BaseViewSet):
    """
    店铺信息采集记录接口
    """
    queryset = models.ShopCollectLog.objects.filter()
    serializer_class = serializers.ShopCollectLogSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_fields = ('sms_status', 'task_id',)
    ordering_fields = ('created',)
    ordering = ('-created',)
