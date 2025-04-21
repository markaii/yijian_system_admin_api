from django.shortcuts import render

from common.viewsets import BaseViewSet
from common.exceptions import ParamsError
from help import models, serializers
from help import constants as c

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter

from base import permissions, authentication


class HelpArticleViewSet(BaseViewSet):
    """
    帮助中心文章接口
    """
    queryset = models.HelpArticle.objects.filter()
    serializer_class = serializers.HelpArticleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    search_fields = ('title',)
    filter_fields = ('status', 'category_id', 'applet_type',)
    ordering_fields = ('created', 'sort',)
    ordering = ('sort',)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.HelpArticleSimpleSerializer
        return serializers.HelpArticleSerializer

    def perform_create(self, serializer):
        """
        创建文章接口
        """
        category_id = self.request.data.get('category_id', '')
        try:
            category = models.HelpCategory.objects.get(id=category_id)
        except models.HelpCategory.DoesNotExist:
            raise ParamsError('category_id参数错误')

        serializer.save(category_name=category.name)

    def get_queryset(self):
        """
        重写get_quertset方法，按日期筛选
        """
        start_date = self.request.GET.get('start_time', '')
        end_date = self.request.GET.get('end_time', '')

        start_time = "%s 00:00:00" % start_date
        end_time = "%s 23:59:59" % end_date

        if start_date and end_date:
            queryset = self.queryset.filter(created__range=(start_time, end_time))
            return queryset
        return self.queryset


class HelpCategoryViewSet(BaseViewSet):
    """
    文章分类接口
    """
    queryset = models.HelpCategory.objects.filter()
    serializer_class = serializers.HelpCategorySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    search_fields = ('name',)
    filter_fields = ('type',)
    ordering_fields = ('sort', 'created',)
    ordering = ('sort',)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.HelpCategorySimpleSerializer
        return serializers.HelpCategorySerializer


class HelpFeedbackViewSet(BaseViewSet):
    """
    问题反馈接口
    """
    queryset = models.HelpFeedback.objects.filter()
    serializer_class = serializers.HelpFeedbackSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)

    search_fields = ('title',)
    filter_fields = ('user_id', 'applet_type',)
    ordering_fields = ('sort', 'created',)
    ordering = ('-created',)

    def get_queryset(self):
        """
        问题已回复，修改status
        """
        comment_ids = models.HelpFeedbackComment.objects.filter().values_list('feedback_id', flat=True)
        models.HelpFeedback.objects.filter(id__in=comment_ids).update(status=c.FEEDBACK_STATUS_REPLIED)
        return self.queryset

    def perform_create(self, serializer):
        """
        创建问题反馈接口，如有附件，需创建附件
        """
        serializer.save()
        file_list = self.request.data.get('file_list', '')
        if file_list:
            for file in file_list:
                models.HelpFeedbackAttachment.objects.create(feedback_id=serializer.data['id'], file_url=file)


class HelpFeedbackCommentViewSet(BaseViewSet):
    """
    问题回复接口
    """
    queryset = models.HelpFeedbackComment.objects.filter()
    serializer_class = serializers.HelpFeedbackCommentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    permission_classes = (permissions.UserLoginRequire,)
    authentication_classes = (authentication.UserTokenAuthentication,)
    filter_fields = ('user_id', 'feedback_id')
    ordering_fields = ('created',)
    ordering = ('-created',)
