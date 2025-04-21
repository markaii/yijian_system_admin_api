from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter

from common.response import JsonResponse
from common.viewsets import BaseViewSet
from common.exceptions import ParamsError
from base import permissions, authentication

from coupon import serializers
from coupon import models


class CouponViewSet(BaseViewSet):
    queryset = models.Coupon.objects.filter()
    serializer_class = serializers.CouponSerializers

    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    filter_fields = ('status', 'type',)
    search_fields = ('code', 'name',)


class CouponVoucherViewSet(BaseViewSet):
    queryset = models.CouponVoucher.objects.filter()
    serializer_class = serializers.CouponVoucherSerializers

    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    filter_fields = ('coupon_id', 'user_id', 'status', 'shop_id')
    ordering = ('-created',)
