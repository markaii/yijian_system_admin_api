from django_filters.rest_framework import DjangoFilterBackend
from common.viewsets import BaseViewSet
from common.response import JsonResponse

from base import permissions, authentication

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework import status
from shop import models, serializers, services
from shop import constants as c

import json


class ShopViewSet(BaseViewSet):
    """
    店铺基础接口
    GET:    shop/
    POST:   shop/
    PUT:    shop/<id>/
    DELETE: shop/<id>/
    筛选店铺状态接口
    GET:    shop/?status=[0,1]
    店铺批量修改状态接口
    POST:   shop/modify_shop_status/
    """
    queryset = models.Shop.objects.filter()
    serializer_class = serializers.ShopSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('name',)
    filter_fields = (
    'business_status', 'district', 'province', 'city', 'booking_type', 'pay_service_status', 'business_type',)
    ordering_fields = ('created',)
    ordering = ('-created',)

    def get_queryset(self):
        # 重写get_queryset方法，如果没传status，返回所有数据
        get_status = self.request.query_params.get('status')
        if get_status is None:
            return self.queryset
        shop_status = json.loads(get_status)  # 字符串转换列表
        queryset = models.Shop.objects.filter(status__in=shop_status)
        return queryset

    @action(methods=['POST'], detail=False)
    def modify_shop_status(self, request):
        """
        店铺审核接口
        :param request:
        :return:
        """
        shop_id = request.data.get('shop_id', '')
        shop_status = request.data.get('status', '')
        remark = request.data.get('remark', '')
        if shop_status == c.SHOP_STATUS_DISABLED or shop_status == c.SHOP_STATUS_APPROVE:  # 禁用时需要补充remark
            if remark == '':
                return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                    status=status.HTTP_400_BAD_REQUEST)
        elif shop_status == c.SHOP_STATUS_NOT or shop_status == c.SHOP_STATUS_ENABLED:  # 有效时无需补充remark
            remark = ''

        # 修改审核状态
        resp, obj = services.modify_shop_status(shop_id=shop_id, shop_status=shop_status, remark=remark)

        if not resp:
            return JsonResponse(message=obj, code=obj, status=status.HTTP_400_BAD_REQUEST)

        # 发送微信订阅消息
        services.send_subscribe_message(obj)
        return JsonResponse(message='ok', code=c.API_MESSAGE_OK)

    @action(methods=['POST'], detail=False)
    def batch_approve(self, request):
        """
        批量审核店铺
        :param request:
        :return:
        """
        shop_ids = request.data.get('shop_ids', '')
        shop_status = request.data.get('status', '')
        remark = request.data.get('remark', '')
        if shop_status == c.SHOP_STATUS_DISABLED or shop_status == c.SHOP_STATUS_APPROVE:  # 禁用时需要补充remark
            if remark == '':
                return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                    status=status.HTTP_400_BAD_REQUEST)
        elif shop_status == c.SHOP_STATUS_NOT or shop_status == c.SHOP_STATUS_ENABLED:  # 有效时无需补充remark
            remark = ''

        resp, message = services.batch_approve(shop_ids=shop_ids, shop_status=shop_status, remark=remark)

        if not resp:
            return JsonResponse(message=message, code=c.API_MESSAGE_PARAM_ERROR, status=status.HTTP_400_BAD_REQUEST)

        if not resp:
            return JsonResponse(message=c.ERROR_TABLE[message], code=message, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(message='ok', code=c.API_MESSAGE_OK)


class PayApplyIndividualViewSet(BaseViewSet):
    """
    个体工商户进件接口
    """
    queryset = models.PayApplyIndividual.objects.filter()
    serializer_class = serializers.PayApplyIndividualSerializers
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('status',)
    search_fields = ('boss_name', 'shop_name',)
    ordering = ('-created',)


class PayApplyEnterpriseViewSet(BaseViewSet):
    """
    企业进件接口
    """
    queryset = models.PayApplyEnterprise.objects.filter()
    serializer_class = serializers.PayApplyEnterpriseSerializers
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('status',)
    search_fields = ('boss_name', 'shop_name',)
    ordering = ('-created',)


class ShopServiceViewSet(BaseViewSet):
    """
    店铺服务项目接口
    """
    queryset = models.ShopService.objects.filter()
    serializer_class = serializers.ShopServiceSerializers
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = ('shop_name',)
    filter_fields = ('shop_id',)
    ordering_fields = ('created',)
    ordering = ('-created',)


class MerchantOrderViewSet(BaseViewSet):
    """
    商户订单接口
    """
    queryset = models.MerchantOrder.objects.filter()
    serializer_class = serializers.MerchantOrderSerializers
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('shop_id', 'status',)
    ordering_fields = ('created',)
    ordering = ('-created',)
