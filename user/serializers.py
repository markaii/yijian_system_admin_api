from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from user import models, constants as c

from order import models as order_models, serializers as order_serializer

from common.serializers import BaseModelSerializer

from django.db.models import Q


class UserSerializer(BaseModelSerializer):
    """用户序列化"""

    class Meta:
        model = models.User
        fields = '__all__'

    extra_kwargs = {
        'birthday': {'required': False, 'allow_null': True}, }


class CollectTotalSerializer(BaseModelSerializer):
    """收藏总数序列化"""
    # 添加额外参数，关联订单，评论，收藏
    orders_total = SerializerMethodField()
    comments_total = SerializerMethodField()
    collects_total = SerializerMethodField()

    def get_orders_total(self, obj):
        orders_total = order_models.Order.objects.filter(user_id=obj.id).count()
        return orders_total

    def get_comments_total(self, obj):
        comments_total = order_models.Comment.objects.filter(user_id=obj.id).count()
        return comments_total

    def get_collects_total(self, obj):
        type = [c.COLLECT_TYPE_BARBER, c.COLLECT_TYPE_SHOP, c.COLLECT_TYPE_EXAMPLE]
        collects_total = models.Collection.objects.filter(Q(user_id=obj.id) & Q(type__in=type)).count()
        return collects_total

    class Meta:
        model = models.User
        fields = ('id', 'orders_total', 'comments_total', 'collects_total')


class AddressSerializer(BaseModelSerializer):
    """
    店铺收货地址序列化规则
    """

    class Meta:
        model = models.UserAddress
        fields = ('id', 'name', 'mobile', 'province', 'province_code', 'city', 'city_code',
                  'district', 'district_code', 'address', 'default', 'created')


class CreditLogSerializer(BaseModelSerializer):
    """
    积分变动记录序列化模型
    """

    class Meta:
        model = models.CreditLog
        fields = '__all__'


class CollectionSerializer(BaseModelSerializer):
    """
    用户收藏序列化
    """

    class Meta:
        model = models.Collection
        fields = '__all__'


class CustomerOrderSerializer(BaseModelSerializer):
    """
    用户订单序列化
    """

    class Meta:
        model = models.CustomerOrder
        fields = '__all__'
