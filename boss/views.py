from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework import status

from common.viewsets import BaseViewSet
from common.response import JsonResponse

from boss import models, serializers
from boss import constants as c
from base import permissions, authentication


class BossViewSet(BaseViewSet):
    """
    老板账号基础接口
    GET:    boss/
    POST:   boss/
    PUT:    boss/<id>/
    DELETE: boss/<id>/
    """

    queryset = models.Boss.objects.filter()
    serializer_class = serializers.BossSerializer
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', 'phone',)
    filter_fields = ('shop_id','status',)
    ordering_fields = ('created',)
    ordering = ('-created',)

    @action(methods=['POST'], detail=False)
    def ban(self, request):
        """禁用账号接口"""
        boss_id = request.data.get('id', '')
        boss_status = request.data.get('status', '')
        boss = self.queryset.filter(id=boss_id).update(status=boss_status)
        if not boss:
            return JsonResponse(message=c.API_MESSAGE_PARAM_ERROR, code=status.HTTP_400_BAD_REQUEST,
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(message='ok', code=c.API_MESSAGE_OK)
