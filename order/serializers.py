from rest_framework.serializers import SerializerMethodField
from common import serializers
from order import models
from barber import models as barber_models
from shop import models as shop_models
from barber import serializers as barber_serializers
from shop import serializers as shop_serializers


class OrderSerializer(serializers.BaseModelSerializer):
    """
    订单Serializer
    """

    class Meta:
        model = models.Order
        fields = '__all__'


class CommentSerializer(serializers.BaseModelSerializer):
    """
    评论Serializer
    ：关联评论文件，评论标签
    """
    file_list = SerializerMethodField()
    # comment_tag_list = SerializerMethodField()

    def get_file_list(self, obj):
        file = models.CommentFile.objects.filter(comment_id=obj.id)
        serializer = CommentFileSerializer(file, many=True)
        return serializer.data

    # def get_comment_tag_list(self, obj):
    #     tag = models.CommentTag.objects.filter(comment_id=obj.id)
    #     serializer = CommentTagSerializer(tag, many=True)
    #     return serializer.data

    class Meta:
        model = models.Comment
        fields = '__all__'


class CommentSimpleSerializer(serializers.BaseModelSerializer):
    """
    评论简单Serializer
    """

    class Meta:
        model = models.Comment
        fields = '__all__'


class CommentFileSerializer(serializers.BaseModelSerializer):
    """
    评论文件Serializer
    """

    class Meta:
        model = models.CommentFile
        fields = '__all__'


class CommentTagSerializer(serializers.BaseModelSerializer):
    """
    评论标签Serializer
    """

    class Meta:
        model = models.CommentTag
        fields = '__all__'
