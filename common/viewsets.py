import time
import datetime
from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet

from base.models import Company
from common.pagination import PageNumberPaginationEx
from common.response import JsonResponse
from project import constants as c


class BaseReadOnlyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    Base API Interface
    """
    page_size_query_param = 'size'
    pagination_class = PageNumberPaginationEx

    def get_paginated_response(self, data):
        # 分页数据展示
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok', data=super().get_paginated_response(data))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 不分页列表数据展示
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok', data=serializer.data)

    def get_queryset(self):
        parent_id = self.request.query_params.get('parent_id', None)
        if parent_id == '':
            return self.queryset.filter(parent_id='')
        else:
            return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, code=c.API_MESSAGE_OK, message='ok', status=status.HTTP_200_OK)


class BaseViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  BaseReadOnlyViewSet,
                  GenericViewSet):

    # def perform_update(self, serializer):
    #     # 更新modify_date字段
    #     now = datetime.datetime.now()
    #     serializer.validated_data['modify_time'] = now
    #     serializer.validated_data['modify_user_name'] = self.request.user.realname
    #     serializer.validated_data['sync_time'] = int(time.time())
    #     super().perform_update(serializer)

    # def perform_create(self, serializer):
    #     # 更新操作人
    #     now = datetime.datetime.now()
    #     serializer.validated_data['create_time'] = now
    #     serializer.validated_data['modify_time'] = now
    #     serializer.validated_data['sync_time'] = int(time.time())
    #     serializer.validated_data['create_user_name'] = self.request.user.realname
    #     serializer.validated_data['modify_user_name'] = ''
    #     serializer.save()
        # 更新关联店铺信息
        # try:
        #     shop = shop_models.Shop.objects.get(shop_license=self.request.user)
        # except shop_models.Shop.DoesNotExist:
        #     raise LogicalError('Token未查询到店铺')
        # serializer.validated_data['shop_id'] = shop.id
        # serializer.validated_data['shop_name'] = shop.shop_name
        # serializer.validated_data['shop_license'] = shop.shop_license
        # serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, code=c.API_MESSAGE_OK, message='ok', status=status.HTTP_201_CREATED,
                            headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return JsonResponse(data=serializer.data, code=c.API_MESSAGE_OK, message='ok', status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(code=c.API_MESSAGE_OK, message='ok', status=status.HTTP_204_NO_CONTENT)
