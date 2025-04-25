from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from common.viewsets import BaseViewSet
from base import permissions, authentication

from member import models
from member import serializers


class MemberCardViewSet(BaseViewSet):
    """
    商家会员卡接口
    """
    queryset = models.MemberCard.objects.filter()
    serializer_class = serializers.MemberCardSimpleSerializers
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('shop_name', 'name',)
    filter_fields = ('shop_id', 'level', 'expire_type', 'status',)
    ordering_fields = ('created', 'sort',)
    ordering = ('-created',)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.MemberCardSerializers
        return super().get_serializer_class()


class MemberCardInstanceViewSet(BaseViewSet):
    """
    用户会员卡接口
    """
    queryset = models.MemberCardInstance.objects.filter()
    serializer_class = serializers.MemberCardInstanceSerializers
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('shop_name', 'user_phone', 'user_name',)
    filter_fields = ('level', 'shop_id', 'card_id', 'status',)
    ordering_fields = ('created',)
    ordering = ('-created',)


class MemberCardChargeLogViewSet(BaseViewSet):
    """
    用户会员卡充值记录接口
    """
    queryset = models.MemberCardChargeLog.objects.filter()
    serializer_class = serializers.MemberCardChargeLogSerializers
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('shop_name',)
    filter_fields = ('user_id', 'level', 'shop_id',)
    ordering_fields = ('created',)
    ordering = ('-created',)


class MemberCardConsumeLogViewSet(BaseViewSet):
    """
    用户会员卡消费记录接口
    """
    queryset = models.MemberCardConsumeLog.objects.filter()
    serializer_class = serializers.MemberCardConsumeLogSerializers
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('shop_name',)
    filter_fields = ('user_id', 'level', 'shop_id',)
    ordering_fields = ('created',)
    ordering = ('-created',)


class MemberChargeOrderViewSet(BaseViewSet):
    """
    用户会员卡充值订单接口
    """
    queryset = models.MemberChargeOrder.objects.filter()
    serializer_class = serializers.MemberChargeOrderSerializers
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('shop_name', 'card_name',)
    filter_fields = ('shop_id', 'user_id', 'service_fee_status', 'status',)
    ordering_fields = ('created',)
    ordering = ('-created',)
