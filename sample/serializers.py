from rest_framework import serializers as rest_serializers
from rest_framework.serializers import SerializerMethodField
from common import serializers

from sample import models


class SampleTagSerializer(serializers.BaseModelSerializer):
    """
    作品标签Serializer
    """

    class Meta:
        model = models.SampleTag
        fields = '__all__'


class SampleSerializer(serializers.BaseModelSerializer):
    """
    作品标签Serializer
    """

    file = SerializerMethodField()

    def get_file(self, obj):
        file = models.SampleFile.objects.filter(sample_id=obj.id).first()
        if file:
            serializer = SampleFileSerializer(file)
            return serializer.data
        else:
            return None

    class Meta:
        model = models.Sample
        fields = '__all__'


class SampleDetailSerializer(serializers.BaseModelSerializer):
    """
    作品标签Serializer
    """
    file_list = SerializerMethodField()

    def get_file_list(self, obj):
        file = models.SampleFile.objects.filter(sample_id=obj.id)
        serializer = SampleFileSerializer(file, many=True)
        return serializer.data

    class Meta:
        model = models.Sample
        fields = '__all__'


class SampleFileSerializer(serializers.BaseModelSerializer):
    """
    作品标签Serializer
    """

    class Meta:
        model = models.SampleFile
        fields = '__all__'


class SampleReportSerializer(serializers.BaseModelSerializer):
    """
    作品举报Serializer
    """

    file = SerializerMethodField()

    def get_file(self, obj):
        file = models.SampleReportFile.objects.filter(report_id=obj.id).first()
        if file:
            serializer = SampleReportFileSerializer(file)
            return serializer.data
        else:
            return None

    class Meta:
        model = models.SampleReport
        fields = '__all__'


class SampleReportDetailSerializer(serializers.BaseModelSerializer):
    """
    作品举报Serializer
    """

    file_list = SerializerMethodField()

    def get_file_list(self, obj):
        file = models.SampleReportFile.objects.filter(report_id=obj.id)
        serializer = SampleReportFileSerializer(file, many=True)
        return serializer.data

    class Meta:
        model = models.SampleReport
        fields = '__all__'


class SampleReportFileSerializer(serializers.BaseModelSerializer):
    """
    举报文件标签Serializer
    """

    class Meta:
        model = models.SampleReportFile
        fields = '__all__'


class HairChangeLogSerializer(serializers.BaseModelSerializer):
    """
    变更发型记录Serializer
    """

    class Meta:
        model = models.HairChangeLog
        fields = '__all__'


class HairColorChangeLogSerializer(serializers.BaseModelSerializer):
    """
    变更发色记录Serializer
    """

    class Meta:
        model = models.HairColorChangeLog
        fields = '__all__'
