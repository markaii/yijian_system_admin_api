from rest_framework import serializers
from help import models
from common.serializers import BaseModelSerializer


class HelpArticleSimpleSerializer(BaseModelSerializer):
    """帮助中心文章简单序列化器"""

    class Meta:
        model = models.HelpArticle
        fields = ('id', 'status', 'category_id', 'category_name', 'title', 'content', 'sort', 'applet_type', 'created',)


class HelpArticleSerializer(BaseModelSerializer):
    """帮助中心文章"""

    class Meta:
        model = models.HelpArticle
        fields = '__all__'


class HelpCategorySimpleSerializer(BaseModelSerializer):
    """文章分类简单序列化器"""

    class Meta:
        model = models.HelpCategory
        fields = ('id', 'name', 'sort', 'type',)


class HelpCategorySerializer(BaseModelSerializer):
    """文章分类序列化器"""

    class Meta:
        model = models.HelpCategory
        fields = '__all__'


class HelpFeedbackSimpleSerializer(BaseModelSerializer):
    """反馈模型简单序列化器"""

    class Meta:
        model = models.HelpFeedback
        fields = ('id', 'title', 'user_id', 'user_name', 'content', 'category_name',
                  'rank', 'status', 'type', 'sort', 'created', 'applet_type',)
        extra_kwargs = {
            'user_id': {'required': False},

        }


class HelpFeedbackSerializer(BaseModelSerializer):
    """反馈模型序列化器"""
    comment_list = serializers.SerializerMethodField()
    file_list = serializers.SerializerMethodField()

    def get_comment_list(self, obj):
        qs = models.HelpFeedbackComment.objects.filter(feedback_id=obj.id).order_by("created")
        serializer = HelpFeedbackCommentSimpleSerializer(qs, many=True)
        return serializer.data

    def get_file_list(self, obj):
        print(obj.id)
        qs = models.HelpFeedbackAttachment.objects.filter(feedback_id=obj.id)
        serializer = HelpFeedbackAttachmentSerializer(qs, many=True)
        return serializer.data

    class Meta:
        model = models.HelpFeedback
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'required': False},
        }


class HelpFeedbackAttachmentSerializer(BaseModelSerializer):
    """反馈附件序列化器"""

    class Meta:
        model = models.HelpFeedbackAttachment
        fields = ('id', 'feedback_id', 'feedback_title', 'file_url')


class HelpFeedbackCommentSimpleSerializer(BaseModelSerializer):
    """问题回复简单序列化器"""

    class Meta:
        model = models.HelpFeedbackComment
        fields = ('id', 'feedback_id', 'feedback_title', 'user_id', 'user_name', 'user_avatar', 'comment', 'created')


class HelpFeedbackCommentSerializer(BaseModelSerializer):
    """问题回复序列化器"""

    class Meta:
        model = models.HelpFeedbackComment
        fields = '__all__'
