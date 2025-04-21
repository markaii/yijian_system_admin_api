from common.viewsets import BaseViewSet
from base import authentication, permissions
from common.response import JsonResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from rest_framework import status
from activity import serializers
from activity import models
from activity import services
from activity import constants as c


# Create your views here.

class BannerViewSet(BaseViewSet):
    """
    小程序广告配置接口
    """
    queryset = models.Banner.objects.filter()
    serializer_class = serializers.BannerSerializers
    authentication_classes = (authentication.UserTokenAuthentication,)
    permission_classes = (permissions.UserLoginRequire,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filter_fields = ('jump_type', 'status', 'applet_type',)
    search_fields = ('name',)
    ordering_fields = ('sort', 'created',)
    ordering = ('sort',)

    def get_queryset(self):
        """
        重写get_quertset方法，按日期筛选
        """
        start_date = self.request.GET.get('start_time', '')
        end_date = self.request.GET.get('end_time', '')

        start_time = "%s 00:00:00" % start_date
        end_time = "%s 23:59:59" % end_date

        if start_date and end_date:
            queryset = self.queryset.filter(created__range=(start_time, end_time))
            return queryset
        return self.queryset


class ShopInviteActivityViewSet(BaseViewSet):
    """
    入驻活动广告配置接口
    """
    serializer_class = serializers.ShopInviteActivitySerializers
    queryset = models.ShopInviteActivity.objects.filter()
    authentication_classes = (authentication.UserTokenAuthentication,)
    permission_classes = (permissions.UserLoginRequire,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filter_fields = ('code', 'applet_type', 'status', 'applet_type',)
    search_fields = ('name',)
    ordering_fields = ('sort', 'created',)
    ordering = ('sort',)

    def perform_create(self, serializer):
        """活动配置接口"""
        # 生成code
        code = services._generate_random_str(10)
        serializer.save(code=code)


class ShopInviteLogViewSet(BaseViewSet):
    """
    入驻邀请记录接口
    """
    serializer_class = serializers.ShopInviteLogSerializers
    queryset = models.ShopInviteLog.objects.filter()
    authentication_classes = (authentication.UserTokenAuthentication,)
    permission_classes = (permissions.UserLoginRequire,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filter_fields = ('inviter_openid', 'shop_id', 'boss_id', 'status',)


class ShopPosterApplyViewSet(BaseViewSet):
    """
    店铺物料申请接口
    """
    serializer_class = serializers.ShopPosterApplySerializers
    queryset = models.ShopPosterApply.objects.filter()
    authentication_classes = (authentication.UserTokenAuthentication,)
    permission_classes = (permissions.UserLoginRequire,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('name', 'phone',)
    filter_fields = ('status',)

    @action(detail=False, methods=['post'])
    def approval(self, request):
        """
        物料申请审核接口
        """
        apply_id = self.request.data.get('id', '')
        apply_status = self.request.data.get('status', '')
        remark = self.request.data.get('remark', '')

        try:
            apply = models.ShopPosterApply.objects.get(id=apply_id)
        except models.ShopPosterApply.DoesNotExist:
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=c.API_MESSAGE_PARAM_ERROR,
                                status=status.HTTP_400_BAD_REQUEST)

        if not apply_status or not apply_id:
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=c.API_MESSAGE_PARAM_ERROR,
                                status=status.HTTP_400_BAD_REQUEST)

        # 修改申请状态
        apply.status = apply_status
        apply.remark = remark
        apply.save()

        # 修改关联记录状态
        log = models.ShopPosterApplyLog.objects.filter(apply_id=apply_id).first()
        if log:
            log.status = apply_status
            log.remark = remark
            log.save()
        return JsonResponse(message=c.API_MESSAGE_OK, code=c.API_MESSAGE_OK, status=status.HTTP_200_OK)


class ShopPosterApplyLogViewSet(BaseViewSet):
    """
    店铺物料申请记录接口
    """
    serializer_class = serializers.ShopPosterApplyLogSerializers
    queryset = models.ShopPosterApplyLog.objects.filter()
    authentication_classes = (authentication.UserTokenAuthentication,)
    permission_classes = (permissions.UserLoginRequire,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('name', 'phone', 'user_id',)
    filter_fields = ('status',)


class ShopCouponActivityViewSet(BaseViewSet):
    """
    店铺优惠券活动接口
    """
    serializer_class = serializers.ShopCouponActivitySerializers
    queryset = models.ShopCouponActivity.objects.filter()
    authentication_classes = (authentication.UserTokenAuthentication,)
    permission_classes = (permissions.UserLoginRequire,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('code', 'name',)
    filter_fields = ('status', 'type',)
    ordering_fields = ('sort', 'created',)

    def get_queryset(self):
        """重写此方法，补充活动开始、结束时间筛选"""
        start_time = self.request.GET.get('start_time', '')
        end_time = self.request.GET.get('end_time', '')

        if start_time and end_time:
            queryset = self.queryset.filter(start_date__gte=start_time, end_date__lte=end_time)

            return self.filter_queryset(queryset)
        return super().get_queryset()


class ShopPinLogViewSet(BaseViewSet):
    """
    拼团记录接口
    """
    serializer_class = serializers.ShopPinLogSerializers
    queryset = models.ShopPinLog.objects.filter()
    authentication_classes = (authentication.UserTokenAuthentication,)
    permission_classes = (permissions.UserLoginRequire,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("activity_id", "pin_id", "shop_id", "user_id",)
    # search_fields = ()
    # ordering_fields = ()
