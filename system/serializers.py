from common.serializers import BaseModelSerializer
from system import models


class SystemConfigSerializers(BaseModelSerializer):
    """系统配置序列化器"""

    class Meta:
        model = models.SystemConfig
        fields = "__all__"


class SystemSampleSerializers(BaseModelSerializer):
    """系统样本序列化器"""

    class Meta:
        model = models.SystemSample
        fields = "__all__"
