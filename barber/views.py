from django_filters.rest_framework import DjangoFilterBackend
from common.viewsets import BaseViewSet
from common.response import JsonResponse

from base import permissions, authentication

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework import status

from barber import models, serializers
from barber import constants as c


class BarberViewSet(BaseViewSet):
    """
    理发师账号基础接口
    GET:    barber/
    POST:   barber/
    PUT:    barber/<id>/
    DELETE: barber/<id>/
    """
    queryset = models.Barber.objects.filter()
    serializer_class = serializers.BarberSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('name', 'phone',)
    filter_fields = ('shop_id',)
    ordering_fields = ('created',)
    ordering = ('-created',)

    def get_serializer_class(self):
        # 重写get_serializer_class
        if self.action == 'list':
            return serializers.BarberSimpleSerializer
        return serializers.BarberSerializer


class ExampleViewSet(BaseViewSet):
    """
    作品基础接口
    GET:    barber/example/
    POST:   barber/example/
    PUT:    barber/example/<id>/
    DELETE: barber/example/<id>/
    通过barber_id获取
    GET:    barber/example/<barber_id>/
    """
    queryset = models.Example.objects.filter()
    serializer_class = serializers.ExampleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('title', 'barber_name',)
    filter_fields = ('barber_id', 'shop_id', 'status',)
    ordering_fields = ('sort', 'created',)
    ordering = ('-created',)

    def get_queryset(self):
        # 重写get_queryset，通过barber_id获取
        barber_id = self.request.GET.get('barber_id', '')
        if barber_id == '':
            return self.queryset
        return self.queryset.filter(barber_id=barber_id)

    @action(methods=['POST'], detail=False)
    def ban(self, request):
        """作品禁用接口"""
        example_id = request.data.get('id', '')
        example_status = request.data.get('status', '')
        example = self.queryset.filter(id=example_id).update(status=example_status)
        if not example:
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(message='ok', code=c.API_MESSAGE_OK)


class ServiceViewSet(BaseViewSet):
    """
    服务项目基础接口
    GET:    barber/service/
    POST:   barber/service/
    PUT:    barber/service/<id>/
    DELETE: barber/service/<id>/
    """
    queryset = models.Service.objects.filter()
    serializer_class = serializers.ServiceSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('name',)
    filter_fields = ('barber_id', 'shop_id',)
    ordering_fields = ('created',)
    ordering = ('-created',)


class SystemServiceViewSet(BaseViewSet):
    """
    系统服务项目基础接口
    :barber/systemservice/
    GET:    barber/systemservice/
    POST:   barber/systemservice/
    PUT:    barber/systemservice/<id>/
    DELETE: barber/systemservice/<id>/
    """
    queryset = models.SystemService.objects.filter()
    serializer_class = serializers.SystemServiceSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_fields = ('category_id',)
    search_fields = ('name',)
    ordering_fields = ('created',)
    ordering = ('-created',)


class ServiceCategoryViewSet(BaseViewSet):
    """
    服务项目分类接口
    """
    queryset = models.ServiceCategory.objects.filter()
    serializer_class = serializers.ServiceCategorySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    search_fields = ('name',)
    ordering_fields = ('sort',)

    # ordering = ('-created',)

    def perform_create(self, serializer):
        user = self.request.user
        # 创建时补充创建人
        serializer.save(create_user_id=user.id, create_user_name=user.realname)

    def perform_update(self, serializer):
        user = self.request.user
        # 修改时补充修改人
        serializer.save(modify_user_id=user.id, modify_user_name=user.realname)
