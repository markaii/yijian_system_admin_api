from common.serializers import BaseModelSerializer
from common.response import JsonResponse

from boss import models
from boss import constants as c
from shop import models as shop_models
from shop import serializers as shop_serializers

from rest_framework.serializers import SerializerMethodField


class BossSerializer(BaseModelSerializer):
    """
    老板账号Serizlizer
    ：关联店铺
    """

    class Meta:
        model = models.Boss
        fields = '__all__'
