import logging

from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from base import permissions, authentication
from user import serializers
from user import models
from common.viewsets import BaseViewSet

logger = logging.getLogger('user')


class UserViewSet(BaseViewSet):
    """
    用户接口
    """
    queryset = models.User.objects.filter()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend,)
    search_fields = ('name', 'phone',)
    filter_fields = ('status',)
    ordering_fields = ('created',)
    ordering = ('-created',)


class UserAddressViewSet(BaseViewSet):
    """
    用户地址 API
    1. 创建地址 post   /user/address/ 需要授权
    2. 获取地址列表 get /user/address/ 需要授权
    3. 修改地址 put    /user/address/<id>/ 需要授权
    4. 删除地址 delete /user/address/<id>/ 需要授权
    """
    serializer_class = serializers.AddressSerializer
    queryset = models.UserAddress.objects.filter()
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('default',)
    ordering = ('-default', '-created')


class CreditLogViewSet(BaseViewSet):
    """
    积分日志查询
    1.获取积分获取记录 get /credit/log/
    2.查询某个事件发生的次数 get /credit/log/?year=2019&month=4&event=xxx
    """
    serializer_class = serializers.CreditLogSerializer
    queryset = models.CreditLog.objects.filter()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    filter_fields = ('type', 'user_id')
    ordering_fields = ('credit', 'created')
    ordering = ('-created',)


class CollectionViewSet(BaseViewSet):
    """
    用户收藏记录接口
    """
    serializer_class = serializers.CollectionSerializer
    queryset = models.Collection.objects.filter()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_fields = ('type', 'user_id',)
    ordering_fields = ('created',)
    ordering = ('-created',)


class CustomerOrderViewSet(BaseViewSet):
    """
    用户订单接口
    """
    queryset = models.CustomerOrder.objects.filter()
    serializer_class = serializers.CustomerOrderSerializer
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)

    search_fields = ('user_name', 'user_phone', 'order_no',)
    filter_fields = ('status', 'type',)
    ordering_fields = ('created',)
    ordering = ('-created',)
