from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base Model Serializer
    """
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)


