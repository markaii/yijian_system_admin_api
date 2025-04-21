from common import serializers
from task import models


class ShopCollectTaskSerializer(serializers.BaseModelSerializer):
    """
    店铺采集任务Serializer
    """

    class Meta:
        model = models.ShopCollectTask
        fields = '__all__'


class ShopCollectLogSerializer(serializers.BaseModelSerializer):
    """
    采集店铺信息记录Serializer
    """

    class Meta:
        model = models.ShopCollectLog
        fields = '__all__'
