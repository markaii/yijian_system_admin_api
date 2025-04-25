from django_filters.rest_framework import DjangoFilterBackend
from common.viewsets import BaseViewSet
from common.response import JsonResponse

from base import permissions, authentication

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status

from order import serializers, models
from order import constants as c


class OrderViewSet(BaseViewSet):
    """
    订单基础接口
    GET:    order/
    POST:   order/
    PUT:    order/<id>/
    DELETE: order/<id>/
    """
    queryset = models.Order.objects.filter()
    serializer_class = serializers.OrderSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('serial',)
    filter_fields = ('user_id', 'barber_id', 'shop_id', 'service_id', 'status', 'type',)
    ordering_fields = ('created',)
    ordering = ('-created',)

    def get_queryset(self):
        """按日期筛选"""
        start_time = self.request.GET.get('start_time', '')
        end_time = self.request.GET.get('end_time', '')

        if start_time and end_time:
            queryset = self.queryset.filter(created__range=(start_time, end_time,))
            return queryset
        return self.queryset


class CommentViewSet(BaseViewSet):
    """
    评论基础接口
    GET:    order/comment/<id>/
    POST:   order/comment/
    PUT:    order/comment/<id>/
    DELETE: order/comment/<id>/
    """
    queryset = models.Comment.objects.filter()
    serializer_class = serializers.CommentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_fields = ('user_id', 'barber_id', 'shop_id',)
    ordering_fields = ('created',)
    ordering = ('-created',)

    def get_queryset(self):
        """按日期筛选"""
        start_time = self.request.GET.get('start_time', '')
        end_time = self.request.GET.get('end_time', '')

        if start_time and end_time:
            queryset = self.queryset.filter(created__range=(start_time, end_time,))
            return queryset
        return self.queryset
