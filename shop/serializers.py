from rest_framework.serializers import SerializerMethodField
from common import serializers
from shop import models


class ShopSerializer(serializers.BaseModelSerializer):
    """
    理发店Serializer
    ：关联店铺文件
    """
    # 带出店铺文件
    image_list = SerializerMethodField()

    def get_image_list(self, obj):
        image = models.ShopFile.objects.filter(shop_id=obj.id)
        serializer = ShopFileSerializer(image, many=True)
        return serializer.data

    class Meta:
        model = models.Shop
        fields = '__all__'


class ShopSimpleSerializer(serializers.BaseModelSerializer):
    """
    理发店简单Serializer
    """

    class Meta:
        model = models.Shop
        fields = '__all__'


class ShopFileSerializer(serializers.BaseModelSerializer):
    """
    理发店文件Serializer
    """

    class Meta:
        model = models.ShopFile
        fields = '__all__'


class PayApplyIndividualSerializers(serializers.BaseModelSerializer):
    """
    个体工商户进件序列化器
    """

    class Meta:
        model = models.PayApplyIndividual
        fields = '__all__'


class PayApplyEnterpriseSerializers(serializers.BaseModelSerializer):
    """
    企业进件序列化器
    """

    class Meta:
        model = models.PayApplyEnterprise
        fields = '__all__'


class ShopServiceSerializers(serializers.BaseModelSerializer):
    """
    店铺服务项目序列化器
    """

    class Meta:
        model = models.ShopService
        fields = '__all__'


class MerchantOrderSerializers(serializers.BaseModelSerializer):
    """
    商户订单序列化器
    """

    class Meta:
        model = models.MerchantOrder
        fields = '__all__'
