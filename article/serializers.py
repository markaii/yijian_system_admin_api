from rest_framework import serializers
from common.serializers import BaseModelSerializer
from article import models


class ArticleSerializer(BaseModelSerializer):
    """文章序列化器"""
    publish_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = models.Article
        fields = '__all__'


class ShareArticleCategorySerializer(BaseModelSerializer):
    """文章分类序列化器"""

    class Meta:
        model = models.ArticleCategory
        fields = '__all__'
