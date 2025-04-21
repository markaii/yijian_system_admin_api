from rest_framework.serializers import SerializerMethodField
from common import serializers
from barber import models


class BarberSerializer(serializers.BaseModelSerializer):
    """
    理发师Serializer
    ：关联作品，服务项目
    """
    # 带出作品，服务项目
    example_list = SerializerMethodField()
    service_list = SerializerMethodField()

    def get_example_list(self, obj):
        example = models.Example.objects.filter(barber_id=obj.id)
        serializer = ExampleSerializer(example, many=True)
        return serializer.data

    def get_service_list(self, obj):
        service = models.Service.objects.filter(barber_id=obj.id)
        serializer = ServiceSerializer(service, many=True)
        return serializer.data

    class Meta:
        model = models.Barber
        fields = '__all__'


class BarberSimpleSerializer(serializers.BaseModelSerializer):
    """
    理发师简单Serializer
    """

    class Meta:
        model = models.Barber
        fields = '__all__'


class ExampleSerializer(serializers.BaseModelSerializer):
    """
    作品Serializer
    ：关联理发师，门店
    """
    # 带出作品集文件
    file_list = SerializerMethodField()

    def get_file_list(self, obj):
        file = models.ExampleFile.objects.filter(example_id=obj.id)
        serializer = ExampleFileSerializer(file, many=True)
        return serializer.data

    class Meta:
        model = models.Example
        fields = '__all__'


class ExampleSimpleSerializer(serializers.BaseModelSerializer):
    """
    作品简单Serializer
    """

    class Meta:
        model = models.Example
        fields = '__all__'


class ExampleFileSerializer(serializers.BaseModelSerializer):
    """
    作品集文件Serializer
    """

    class Meta:
        model = models.ExampleFile
        fields = '__all__'


class ServiceSerializer(serializers.BaseModelSerializer):
    """
    服务项目Serializer
    ：关联理发师
    """

    class Meta:
        model = models.Service
        fields = '__all__'


class SystemServiceSerializer(serializers.BaseModelSerializer):
    """
    系统项目Serializer
    """

    class Meta:
        model = models.SystemService
        fields = '__all__'


class ServiceCategorySerializer(serializers.BaseModelSerializer):
    """
    服务项目分类序列化器
    """

    class Meta:
        model = models.ServiceCategory
        fields = '__all__'
